import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
        
    if not api_key:
        print("Ошибка: Ключ API не найден. Убедитесь, что он прописан в файле .env")
        return

    # Параметры запроса (версия 2.5)
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        
        print(f"Текущая температура в {city}: {temp}°C, {description}")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Ошибка: Город '{city}' не найден. Проверьте правильность названия.")
        elif response.status_code == 401:
            print("Ошибка 401: Неверный API ключ.")
            print("Пожалуйста, подождите 1-2 часа после создания ключа или проверьте подтверждение почты.")
        else:
            print(f"Ошибка API: {http_err}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python weather.py [Название города]")
    else:
        city = " ".join(sys.argv[1:])
        get_weather(city)
