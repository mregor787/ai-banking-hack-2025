RESPONSE_GENERATION_PROMPT = """
На основе анализа письма и контекста сгенерируй профессиональный ответ.

АНАЛИЗ ПИСЬМА:
{analysis_result}

КОНТЕКСТ И ТРЕБОВАНИЯ:
- Стиль: {style_preference}
- Уровень формальности: {formality_level}/5
- Ключевые моменты для освещения: {key_points}
- Юридические ограничения: {legal_constraints}
- История взаимодействий: {interaction_history}

СГЕНЕРИРУЙ ОТВЕТ, КОТОРЫЙ:
1. Соответствует корпоративному стилю банка
2. Полностью отвечает на запрос
3. Учитывает все юридические нюансы  
4. Соблюдает деловой этикет
5. Содержит необходимые ссылки и реквизиты

Текст ответа:
"""


def build_response_prompt(analysis_result: dict, context: dict) -> str:
    return RESPONSE_GENERATION_PROMPT.format(
        analysis_result=analysis_result,
        **context
    )
