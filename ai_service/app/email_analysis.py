def get_email_analysis_schema() -> str:
    return '''
    {
        "type": "object",
        "properties": {
            "analysis_id": {"type": "string", "format": "uuid"},
            "original_text": {"type": "string"},
            "classification": {
                "type": "object",
                "properties": {
                    "primary_type": {
                        "type": "string",
                        "enum": ["Запрос информации", "Официальная жалоба", "Регуляторный запрос", "Партнёрское предложение", "Запрос на согласование", "Уведомление", "Запрос документации", "Технический вопрос", "Коммерческое предложение"]
                    },
                    "secondary_type": {
                        "type": "array",
                        "items": {
                            "type": "string", 
                            "enum": ["Уточнение по договору", "Жалоба на сервис", "Запрос выписки", "Аудит документации", "Проверка соблюдения", "Запрос KYC", "Согласование условий", "Техническая поддержка", "Изменение реквизитов"]
                        }
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": ["primary_type", "confidence"]
            },
            "critical_parameters": {
                "type": "object", 
                "properties": {
                    "urgency": {"type": "string", "enum": ["Стандартный", "Срочный", "Критичный"]},
                    "sla_deadline": {"type": "string", "format": "date-time"},
                    "formality_level": {"type": "integer", "minimum": 1, "maximum": 5},
                    "required_departments": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["Юридический отдел", "Служба безопасности", "Бэк-офис", "Кредитный отдел", "Отдел казначейства", "Отдел розничного бизнеса", "Техническая поддержка", "Комплаенс", "Бухгалтерия"]
                        }
                    },
                    "legal_risks_detected": {"type": "boolean"},
                    "risk_description": {"type": "string"},
                    "confidentiality_level": {"type": "string", "enum": ["Обычный", "Конфиденциальный", "Строго конфиденциальный"]}
                },
                "required": ["urgency", "formality_level", "required_departments"]
            },
            "key_information": {
                "type": "object",
                "properties": {
                    "core_request": {"type": "string", "description": "Сжатое описание сути запроса 1-2 предложениями"},
                    "sender_details": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "organization": {"type": "string"}, 
                            "position": {"type": "string"},
                            "contacts": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "mentioned_contracts": {"type": "array", "items": {"type": "string"}},
                    "mentioned_regulations": {"type": "array", "items": {"type": "string"}},
                    "sender_expectations": {
                        "type": "array", 
                        "items": {
                            "type": "string",
                            "enum": ["Получить документ", "Получить разъяснение", "Исправить ошибку", "Согласовать условия", "Подписать договор", "Предоставить доступ", "Вернуть средства", "Обновить информацию"]
                        }
                    },
                    "deadline_mentioned": {"type": "string", "format": "date"}
                },
                "required": ["core_request"]
            },
            "computed_metrics": {
                "type": "object", 
                "properties": {
                    "response_complexity": {"type": "number", "minimum": 0, "maximum": 1},
                    "tone_sentiment": {"type": "string", "enum": ["Негативный", "Нейтральный", "Позитивный"]},
                    "compliance_check_score": {"type": "number", "minimum": 0, "maximum": 1},
                    "clarity_score": {"type": "number", "minimum": 0, "maximum": 1}
                }
            }
        },
        "required": ["analysis_id", "original_text", "classification", "critical_parameters", "key_information"]
    }
    '''


EMAIL_ANALYSIS_PROMPT = """
Ты - AI-ассистент системообразующего банка. Проанализируй входящее письмо и верни структурированный анализ в формате JSON строго по схеме ниже.

СХЕМА_АНАЛИЗА:
{json_schema}

ИНСТРУКЦИИ:
1. Точность классификации - критически важна для маршрутизации
2. Определи срочность на основе регуляторных требований и содержания  
3. Выяви все потенциальные юридические риски
4. Извлеки ключевую информацию максимально полно
5. Оцени сложность ответа от 0.1 (простой) до 1.0 (очень сложный)
6. Верни ТОЛЬКО JSON без каких-либо дополнительных комментариев

ПИСЬМО ДЛЯ АНАЛИЗА:
{email_text}
"""


def build_analysis_prompt(email_text: str) -> str:
    return EMAIL_ANALYSIS_PROMPT.format(
        email_text=email_text,
        json_schema=get_email_analysis_schema()
    )
