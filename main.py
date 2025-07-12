
from fastapi import FastAPI

from faststream.rabbit.fastapi import RabbitRouter

app = FastAPI()
rabbit_router = RabbitRouter()


@rabbit_router.post("/orders")
async def make_order(product: str):
    await rabbit_router.broker.publish(
        f"New order for product: {product}",
        queue="orders"
    )
    return {"data": "OK"}

app.include_router(rabbit_router)

