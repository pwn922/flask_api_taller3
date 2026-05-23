from app.auth.infrastructure.hashing.bcrypt_password_hasher import BcryptPasswordHasher

BCRYPT_HASH_LENGTH = 60


class TestBcryptPasswordHasher:
    def setup_method(self):
        self.hasher = BcryptPasswordHasher()

    def test_hash_returns_bcrypt_hash(self):
        password = "test_password_123"
        result = self.hasher.hash(password)

        assert result.startswith("$2b$")
        assert len(result) == BCRYPT_HASH_LENGTH

    def test_hash_is_deterministic(self):
        password = "test_password_123"
        hash1 = self.hasher.hash(password)
        hash2 = self.hasher.hash(password)

        assert hash1 != hash2

    def test_verify_password_returns_true_for_correct_password(self):
        password = "my_secure_password"
        hashed = self.hasher.hash(password)

        assert self.hasher.verify_password(password, hashed) is True

    def test_verify_password_returns_false_for_incorrect_password(self):
        password = "my_secure_password"
        hashed = self.hasher.hash(password)

        assert self.hasher.verify_password("wrong_password", hashed) is False

    def test_verify_password_returns_false_for_empty_password(self):
        password = "my_secure_password"
        hashed = self.hasher.hash(password)

        assert self.hasher.verify_password("", hashed) is False
