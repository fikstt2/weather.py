# Weather CLI Tool (Утилита для получения погоды)

Простая консольная утилита на Python, которая показывает текущую температуру и погодные условия в указанном городе, используя OpenWeatherMap API.

## 🚀 Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/fikstt2/weather.py.git weather
   cd weather
   ```

2. Установите необходимые зависимости:
   ```bash
   python -m pip install -r requirements.txt
   ```

## ⚙️ Настройка

1. Зайдите в `.env.example` и переименуйте в `.env`.
2. Вставьте ваш персональный API ключ от OpenWeatherMap в переменную `OPENWEATHER_API_KEY`.
   > Получить ключ можно бесплатно на сайте [openweathermap.org](https://openweathermap.org/api).

## 💻 Использование

Запустите скрипт, передав название города в качестве аргумента:

```bash
python weather.py Москва
```

Или для городов из нескольких слов:
```bash
python weather.py "Saint Petersburg"
```

## 📁 Структура проекта
- `weather.py` — основной код программы.
- `.env.example` — шаблон для настроек.
- `requirements.txt` — список библиотек (requests, python-dotenv).
- `.gitignore` — исключение лишних файлов (`.env` с вашим ключом и кэш).
