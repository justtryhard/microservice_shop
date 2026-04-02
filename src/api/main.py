from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.api.routes import orders, users, products, exchange
import time


app = FastAPI(
    title="Order Service",
    description="Микросервис для обработки заказов с интеграцией payment-service",
    version="1.0.0"
)


app.include_router(orders.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(exchange.router, prefix="/api/v1")


templates = Jinja2Templates(directory="templates")



@app.middleware("http")
async def request_log(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    total = time.time() - start
    print(request.method, request.url, total)
    return response

@app.get("/test")
async def service_check():
    return {"status": "ok"}

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


