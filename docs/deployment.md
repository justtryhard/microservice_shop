# Развертывание проекта SFMShop

### 1. Локальное развертывание
1. Склонировать репозиторий:
```
git clone https://github.com/justtryhard/microservice_shop.git
cd microservice_shop
```
2. Создать и активировать виртуальное окружение:  
```
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
3. Установить зависимости:  
```
pip install -r requirements.txt
```
4. Настроить переменные окружения - создать .env на основе .env.example
5. Запуск проекта локально:
```
 python -m uvicorn src.api.main:app --reload  
```

### Развертывание через Docker
1. Сделать билд контейнеров:
```
docker-compose build
```
2. Запустить сервисы:
```
docker-compose up -d
```

Логи приложения:  
```
docker-compose logs -f   
```

Остановка и удаление контейнеров:  
```
docker-compose down  
```