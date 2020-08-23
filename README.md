# Материалы по исследованию пользователей и приложение рекомендаций для почты России

### Запуск приложения рекомендаций:
Перед запуском необходимо скачать данные 
https://yadi.sk/d/O3E0gdeBlh1_JQ
и распаковать их в папку data

Запуск через системный python:
```
pip install -r requirements.txt
python ./main/manage.py runserver
```

Запуск через Docker:
```
docker-compose up -d —build
```

### Анализ данных
Анализ данных частично производился в файле Analize.ipynb

Анализ расстояний между точкой отправки и получения производился в файле Geo.ipynb
