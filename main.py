import asyncio
import logging
from os import getenv
from fastapi import FastAPI
from dotenv import load_dotenv
from faststream.rabbit.fastapi import RabbitRouter

load_dotenv()

RABBIT_URL = getenv("RABBIT_BROKER_URL", "amqp://guest:guest@rabbitmq:5672/")

app = FastAPI()
rabbit_router = RabbitRouter(RABBIT_URL)


@rabbit_router.post("/orders")
async def make_order(product: str):
    await rabbit_router.broker.publish(
        f"New order for product: {product}",
        queue="orders"
    )
    return {"data": "OK"}


app.include_router(rabbit_router)


@app.on_event("startup")
async def wait_for_rabbitmq():
    max_retries = 10
    delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Checking RabbitMQ connection (attempt {attempt})...")
            await rabbit_router.broker.connect()
            logging.info("RabbitMQ is available!")
            break
        except Exception as e:
            logging.warning(f"RabbitMQ not ready yet: {e}")
            await asyncio.sleep(delay)
    else:
        raise RuntimeError("RabbitMQ did not become available after retries.")