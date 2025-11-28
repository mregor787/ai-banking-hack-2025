import os
from typing import Optional

class Settings:
    # GigaChat настройки
    GIGACHAT_CLIENT_ID: str = os.getenv("GIGACHAT_CLIENT_ID", "")
    GIGACHAT_CLIENT_SECRET: str = os.getenv("GIGACHAT_CLIENT_SECRET", "")
    GIGACHAT_SCOPE: str = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

    # RabbitMQ настройки
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    AI_REQUESTS_QUEUE: str = os.getenv("AI_REQUESTS_QUEUE", "ai_requests")
    AI_RESPONSES_QUEUE: str = os.getenv("AI_RESPONSES_QUEUE", "ai_responses")

    # Настройки приложения
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))

settings = Settings()
