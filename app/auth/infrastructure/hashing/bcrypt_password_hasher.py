import bcrypt

from app.common.utils.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    @staticmethod
    def hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), hash.encode())
