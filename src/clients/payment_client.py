import httpx


class PaymentClient:
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url

    async def process_payment(self, order_id: int, cost: float):
        return {"status": "ok", "order_id": order_id, "amount": cost}
        # пока отключу этот сервис, т.к. нет задачи
        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post(
        #             f"{self.base_url}/api/v1/payments",
        #             json={"order_id": order_id, "cost": cost},
        #             timeout=10.0
        #         )
        #         response.raise_for_status()
        #         return response.json()
        #     except Exception as e:
        #         print(f"Exception: {e}")
        #         raise Exception(f"Payment service error: {e}")
