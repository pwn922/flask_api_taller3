# app/auth/infrastructure/tokens/jwt_manager.py
import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from app.auth.domain.ports.token_manager import TokenManagerPort

class JWTManager(TokenManagerPort):
    def __init__(self, secret: str, access_exp: int, refresh_exp: int):
        self.secret = secret
        self.access_exp = timedelta(minutes=access_exp)
        self.refresh_exp = timedelta(days=refresh_exp)

    def create_access_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + self.access_exp,
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + self.refresh_exp,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload
        except ExpiredSignatureError:
            raise Exception("Token expirado")
        except InvalidTokenError:
            raise Exception("Token inválido")