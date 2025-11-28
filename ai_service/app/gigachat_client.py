import json
import logging
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole


class GigaChatClient:
    def __init__(self, credentials: str, scope: str):
        self.client = GigaChat(
            credentials=credentials,
            scope=scope,
            verify_ssl_certs=False
        )
        self.logger = logging.getLogger(__name__)

    async def analyze_email(self, email_text: str, json_schema: str) -> dict:
        from prompts.email_analysis import build_analysis_prompt

        prompt = build_analysis_prompt(email_text, json_schema)

        try:
            response = self.client.chat(
                Chat(messages=[
                    Messages(
                        role=MessagesRole.SYSTEM,
                        content="Ты - AI-аналитик банковской корреспонденции. Возвращай только валидный JSON."
                    ),
                    Messages(
                        role=MessagesRole.USER,
                        content=prompt
                    )
                ]),
                temperature=0.1,
                max_tokens=4000
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            self.logger.error(f"GigaChat analysis error: {e}")
            raise

    async def generate_response(self, analysis_result: dict, context: dict) -> str:
        from prompts.response_generation import build_response_prompt

        prompt = build_response_prompt(analysis_result, context)

        try:
            response = self.client.chat(
                Chat(messages=[
                    Messages(
                        role=MessagesRole.SYSTEM,
                        content="Ты - профессиональный составитель деловой переписки банка."
                    ),
                    Messages(
                        role=MessagesRole.USER,
                        content=prompt
                    )
                ]),
                temperature=0.3,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"GigaChat generation error: {e}")
            raise
