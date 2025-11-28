import asyncio
import logging
import aio_pika
from config import settings
from gigachat_client import GigaChatClient
from queue_handler import AIQueueHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def wait_for_rabbitmq(max_retries: int = 30, delay: float = 2.0):
    for attempt in range(max_retries):
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            await connection.close()
            logger.info("RabbitMQ is ready!")
            return True
        except Exception as e:
            logger.warning(
                f"RabbitMQ not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)

    logger.error("Failed to connect to RabbitMQ after all retries")
    return False


async def main():
    if not await wait_for_rabbitmq():
        return

    gigachat_client = GigaChatClient(
        credentials=settings.GIGACHAT_CLIENT_ID,
        scope=settings.GIGACHAT_SCOPE
    )

    queue_handler = AIQueueHandler(
        rabbitmq_url=settings.RABBITMQ_URL,
        gigachat_client=gigachat_client
    )

    await queue_handler.connect()

    channel = await queue_handler.connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(
        settings.AI_REQUESTS_QUEUE,
        durable=True
    )

    logger.info("AI Service started. Waiting for messages...")

    await queue.consume(queue_handler.process_analysis_request)

    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
