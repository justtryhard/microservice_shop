from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PaymentRequest(BaseModel):
    order_id: int
    cost: float


@app.post("/api/v1/payments")
async def process_payment(payment: PaymentRequest):
    # имитирую успешный платёж
    return {"status": "ok", "order_id": payment.order_id, "amount": payment.cost}
