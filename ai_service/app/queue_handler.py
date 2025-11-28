import json
import aio_pika
import logging
from gigachat_client import GigaChatClient

logger = logging.getLogger(__name__)


class AIQueueHandler:
    def __init__(self, rabbitmq_url: str, gigachat_client: GigaChatClient):
        self.rabbitmq_url = rabbitmq_url
        self.gigachat_client = gigachat_client
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(
                self.rabbitmq_url,
                reconnect_interval=5.0
            )

            self.connection.reconnect_callbacks.add(self._on_reconnect)
            self.connection.close_callbacks.add(self._on_close)

            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            logger.info("Successfully connected to RabbitMQ")

        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def _on_reconnect(self, connection):
        logger.info("Reconnected to RabbitMQ")

    async def _on_close(self, connection):
        logger.warning("Connection to RabbitMQ closed")

    async def process_analysis_request(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                request_data = json.loads(message.body.decode())
                logger.info(
                    f"Received analysis request: {request_data.get('correlation_id', 'unknown')}")

                if 'email_text' not in request_data:
                    raise ValueError("Missing required field: email_text")

                analysis_result = await self.gigachat_client.analyze_email(
                    email_text=request_data['email_text']
                )

                if request_data.get('generate_response', False):
                    response_text = await self.gigachat_client.generate_response(
                        analysis_result=analysis_result,
                        context=request_data.get('context', {})
                    )
                    analysis_result['generated_response'] = response_text

                await self._send_analysis_result(
                    analysis_result,
                    request_data.get('correlation_id')
                )

                logger.info(
                    f"Successfully processed request: {request_data.get('correlation_id', 'unknown')}")

            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON: {e}"
                logger.error(error_msg)
                await self._send_error_result(error_msg, None)
            except Exception as e:
                error_msg = f"Processing error: {e}"
                logger.error(error_msg)
                await self._send_error_result(error_msg, message.correlation_id)

    async def _send_analysis_result(self, result: dict, correlation_id: str = None):
        try:
            response_message = {
                "status": "completed",
                "correlation_id": correlation_id,
                "result": result,
                "timestamp": asyncio.get_event_loop().time()
            }

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(response_message,
                                    ensure_ascii=False).encode(),
                    correlation_id=correlation_id,
                    content_type="application/json"
                ),
                routing_key="ai_responses"
            )
        except Exception as e:
            logger.error(f"Failed to send analysis result: {e}")

    async def _send_error_result(self, error: str, correlation_id: str = None):
        try:
            error_message = {
                "status": "error",
                "correlation_id": correlation_id,
                "error": error,
                "timestamp": asyncio.get_event_loop().time()
            }

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(
                        error_message, ensure_ascii=False).encode(),
                    correlation_id=correlation_id,
                    content_type="application/json"
                ),
                routing_key="ai_responses"
            )
        except Exception as e:
            logger.error(f"Failed to send error result: {e}")

    async def close(self):
        if self.connection:
            await self.connection.close()
