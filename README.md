# Установка
## Склонировать проект и перейти в папку
```
git clone https://github.com/justtryhard/microservice_shop/
cd microservice_shop
```

# Настройка окружения

## Создание виртуального окружения
```
python -m venv venv
```

## Активация виртуального окружения
```
source venv/bin/activate
```

## Установка зависимостей
```
pip install requirements.txt
```

## Обновление requirements.txt
```
pip freeze > requirements.txt
```



# Запуск
```
python -m uvicorn src.api.main:app --reload
```

