from pydantic import BaseModel
from typing import List, Optional


class AuthorizationResult(BaseModel):
    access_granted: bool
    status_code: int
    error_message: Optional[str]
    allowed_forms: List[str]
