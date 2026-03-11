from fastapi import FastAPI
from src.api.routes import orders

app = FastAPI(
    title="Order Service",
    description="Микросервис для обработки заказов с интеграцией payment-service",
    version="1.0.0"
)

app.include_router(orders.router)


@app.get("/test")
async def service_check():
    return {"status": "ok"}
