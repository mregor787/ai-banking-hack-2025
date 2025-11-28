import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@mq:5672/")
    AI_REQUESTS_QUEUE = os.getenv("AI_REQUESTS_QUEUE", "external_emails")
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
