Создание venv (1 раз при установке проекта)
`py -m venv .venv`

Активация venv (Windows)
`.venv\Scripts\activate`

Установить зависимости
`pip install -r requirements.txt`

Запуск проекта в режиме разработчика
`py -m fastapi dev main.py`

Запуск проекта в режиме prod
`py -m fastapi run main.py`