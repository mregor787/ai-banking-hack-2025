from flask import Flask, request, jsonify
import pika
import json
import requests
import logging
from config import Config

app = Flask(__name__)
config = Config()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Промпты для генерации разных типов писем
PROMPTS = {
    "information_request": """
    Сгенерируй официальное письмо-запрос информации или документов от банка. 
    Тема: запрос недостающих документов или информации по договору/сделке.
    Стиль: строгий официально-деловой.
    Обязательные элементы:
    - Исходящий номер и дата
    - Точное указание запрашиваемых документов/информации
    - Срок предоставления (3-5 рабочих дней)
    - Основание для запроса (ссылка на договор/нормативный акт)
    - Контактные данные ответственного сотрудника
    """,

    "complaint": """
    Сгенерируй официальную жалобу или претензию в банк.
    Тема: нарушение условий договора, некорректное списание средств, проблемы с обслуживанием.
    Стиль: официально-деловой с элементами требовательного тона.
    Обязательные элементы:
    - Указание договора/счета с проблемой
    - Четкое описание нарушения
    - Требования по устранению
    - Сроки выполнения требований
    - Предупреждение о дальнейших действиях при невыполнении
    """,

    "regulatory_request": """
    Сгенерируй регуляторный запрос от Центрального Банка или надзорного органа.
    Тема: запрос информации в рамках надзорной деятельности.
    Стиль: строгий официальный с цитированием нормативных актов.
    Обязательные элементы:
    - Ссылка на нормативный акт (Указание Банка России)
    - Четкий перечень запрашиваемой информации
    - Срок предоставления
    - Предупреждение о последствиях неисполнения
    - Реквизиты надзорного органа
    """,

    "partnership_offer": """
    Сгенерируй партнёрское предложение для банка.
    Тема: предложение о сотрудничестве, совместные проекты, взаимовыгодное партнерство.
    Стиль: деловой с элементами маркетинга.
    Обязательные элементы:
    - Представление компании/проекта
    - Конкретное предложение о сотрудничестве
    - Выгоды для банка
    - Предлагаемые условия
    - Контактные данные для обсуждения
    """,

    "approval_request": """
    Сгенерируй запрос на согласование для банка.
    Тема: согласование документов, условий сделки, мероприятий.
    Стиль: официально-деловой.
    Обязательные элементы:
    - Четкое описание объекта согласования
    - Приложенные документы (если есть)
    - Сроки согласования
    - Обоснование необходимости согласования
    - Контактные данные
    """,

    "notification": """
    Сгенерируй уведомление или информационное письмо.
    Тема: информирование об изменениях, новых условиях, важных событиях.
    Стиль: официально-деловой, информационный.
    Обязательные элементы:
    - Четкое описание изменений/информации
    - Даты вступления в силу
    - Контактные данные для вопросов
    - Указание на нормативные основания (если применимо)
    """
}


class RabbitMQClient:
    def __init__(self, rabbitmq_url):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(
                queue=config.AI_REQUESTS_QUEUE, durable=True)
            logger.info("Успешное подключение к RabbitMQ")
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к RabbitMQ: {e}")
            return False

    def publish_message(self, message):
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()

            self.channel.basic_publish(
                exchange='',
                routing_key=config.AI_REQUESTS_QUEUE,
                body=json.dumps(message, ensure_ascii=False),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent message
                )
            )
            logger.info(
                f"Сообщение отправлено в очередь: {config.AI_REQUESTS_QUEUE}")
            return True
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в RabbitMQ: {e}")
            return False

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


class DeepSeekClient:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def generate_email(self, prompt, email_type):
        try:
            full_prompt = f"""
            {prompt}
            
            Требования к письму:
            1. Реалистичное содержание с конкретными деталями (номера договоров, даты, суммы)
            2. Соответствие корпоративному стилю банковской документации
            3. Профессиональный деловой язык без эмоциональных окрасов
            4. Полные реквизиты и контактная информация
            5. Структурированный формат с заголовком, основным текстом и подписью
            
            Сгенерируй письмо типа: {email_type}
            """

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты - эксперт по деловой переписке в банковской сфере. Генерируешь реалистичные официальные письма с полными реквизитами и профессиональным стилем."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            response = requests.post(
                self.api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            email_content = result['choices'][0]['message']['content']

            return {
                "type": email_type,
                "content": email_content,
                "status": "generated"
            }

        except Exception as e:
            logger.error(f"Ошибка генерации письма через DeepSeek: {e}")
            return {
                "type": email_type,
                "content": f"Ошибка генерации: {str(e)}",
                "status": "error"
            }


def get_random_email_type():
    """Возвращает случайный тип письма из доступных"""
    import random
    return random.choice(list(PROMPTS.keys()))


@app.route('/generate/mails', methods=['GET'])
def generate_mails():
    try:
        count = int(request.args.get('count', 1))
        email_type = request.args.get('type', 'random')

        if count < 1 or count > 50:
            return jsonify({
                "error": "Параметр count должен быть между 1 и 50"
            }), 400

        # Инициализация клиентов
        rabbit_client = RabbitMQClient(config.RABBITMQ_URL)
        deepseek_client = DeepSeekClient(
            config.DEEPSEEK_API_KEY, config.DEEPSEEK_API_URL)

        if not rabbit_client.connect():
            return jsonify({
                "error": "Не удалось подключиться к RabbitMQ"
            }), 500

        generated_emails = []
        successful_publishes = 0

        for i in range(count):
            # Определяем тип письма
            current_type = get_random_email_type() if email_type == 'random' else email_type

            if current_type not in PROMPTS:
                return jsonify({
                    "error": f"Неизвестный тип письма: {current_type}"
                }), 400

            # Генерируем письмо
            prompt = PROMPTS[current_type]
            email_data = deepseek_client.generate_email(prompt, current_type)

            if email_data['status'] == 'generated':
                # Добавляем метаданные
                email_data['id'] = f"email_{i+1}_{current_type}"
                email_data['timestamp'] = __import__(
                    'datetime').datetime.now().isoformat()

                # Публикуем в RabbitMQ
                if rabbit_client.publish_message(email_data):
                    successful_publishes += 1

                generated_emails.append({
                    "id": email_data['id'],
                    "type": email_data['type'],
                    "status": email_data['status']
                })
            else:
                generated_emails.append({
                    "id": f"email_{i+1}_{current_type}",
                    "type": current_type,
                    "status": "error",
                    "error": email_data['content']
                })

        rabbit_client.close()

        return jsonify({
            "total_requested": count,
            "successfully_generated": len([e for e in generated_emails if e['status'] != 'error']),
            "successfully_published": successful_publishes,
            "emails": generated_emails
        })

    except ValueError:
        return jsonify({
            "error": "Параметр count должен быть числом"
        }), 400
    except Exception as e:
        logger.error(f"Ошибка в endpoint /generate/mails: {e}")
        return jsonify({
            "error": f"Внутренняя ошибка сервера: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint для проверки здоровья сервиса"""
    try:
        rabbit_client = RabbitMQClient(config.RABBITMQ_URL)
        rabbit_healthy = rabbit_client.connect()
        rabbit_client.close()

        return jsonify({
            "status": "healthy",
            "rabbitmq": "connected" if rabbit_healthy else "disconnected",
            "deepseek": "configured" if config.DEEPSEEK_API_KEY != "your-deepseek-api-key-here" else "not_configured"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
