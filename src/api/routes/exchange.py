from fastapi import APIRouter, HTTPException
from src.services.multi_exchange_client import MultiExchangeClient

router = APIRouter(prefix="/api/v1/currency", tags=["currency"])

exchange_client = MultiExchangeClient([
    "https://first.non-working.api/latest",
    "https://second.non-working.api/v3/latest",
    "https://api.exchangerate-api.com/v4/latest"        # рабочий
])

@router.get("/convert")
async def convert_price(price: float, from_currency: str, to_currency: str):
    if from_currency == to_currency:
        return price
    rate = exchange_client.get_exchange_rate(from_currency, to_currency)
    if rate is None:
        raise HTTPException(status_code=503, detail="service unavailable")
    converted = price * rate
    return converted