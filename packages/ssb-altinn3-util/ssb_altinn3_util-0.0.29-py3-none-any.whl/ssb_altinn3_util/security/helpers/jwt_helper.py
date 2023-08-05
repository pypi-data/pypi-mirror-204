import base64
import json
from typing import Dict


def get_user_email_from_token(token: str) -> str:
    """Get the user email from the jwt token"""
    token = token.split(sep=" ")[1]
    token = token.split(sep=".")[1]
    token_decoded = base64.b64decode(token + "==").decode("UTF-8")
    token_json: Dict = json.loads(token_decoded)
    email: str = token_json.get("email")
    return email
