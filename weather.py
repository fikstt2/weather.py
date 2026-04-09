import os
import sys
import asyncio
import logging
import aiohttp
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Модели данных (Pydantic)
class WeatherDescription(BaseModel):
    description: str

class MainData(BaseModel):
    temp: float

class WeatherResponse(BaseModel):
    name: str
    weather: list[WeatherDescription]
    main: MainData

    @property
    def current_temp(self) -> float:
        return self.main.temp

    @property
    def condition(self) -> str:
        return self.weather[0].description if self.weather else "нет описания"

# Логика работы с API
async def get_weather(city: str):
    """
    Получает данные о погоде асинхронно через OpenWeather Map API 
    с валидацией данных через Pydantic.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()

    if not api_key:
        logger.error("Ключ API не найден. Убедитесь, что он прописан в файле .env")
        return
    # Параметры запроса
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    # Создание сессии
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, params=params, timeout=10) as response: 
                if response.status == 404:
                    logger.error(f"Город '{city}' не найден. Проверьте название.")
                    return
                elif response.status == 401:
                    logger.error("Ошибка 401: Неверный API ключ.")
                    return
                
                response.raise_for_status()
                data = await response.json()

                # Валидация данных через Pydantic
                weather_data = WeatherResponse.model_validate(data)
                   
                print(f"Текущая температура в городе {weather_data.name}: {weather_data.current_temp}°C, {weather_data.condition}")
        # Обработка исключений
        except aiohttp.ClientConnectorError:
            logger.error("Ошибка подключения: проверьте интернет-соединение.")
        except asyncio.TimeoutError:
            logger.error("Превышено время ожидания ответа от сервера.")
        except ValidationError as e:
            logger.error(f"Ошибка валидации данных от API: {e}")
        except Exception as e:
            logger.error(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python weather.py [Название города]")
    else:
        city = " ".join(sys.argv[1:])
        try:
            asyncio.run(get_weather(city))
        except KeyboardInterrupt:
            pass