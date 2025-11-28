from pydantic import BaseModel
from typing import Optional, Dict, Any


class EmailAnalysisRequest(BaseModel):
    email_text: str
    generate_response: bool = False
    correlation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    class Config:
        schema_extra = {
            "example": {
                "email_text": "Прошу предоставить выписку по счету...",
                "generate_response": True,
                "correlation_id": "req_12345",
                "context": {
                    "style_preference": "Деловой корпоративный",
                    "formality_level": 4
                }
            }
        }
