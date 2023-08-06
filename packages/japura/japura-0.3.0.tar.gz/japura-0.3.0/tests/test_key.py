from japura.key import JWT, SecureKey


class TestJWT:

    key = 'secret_key'
    payload = {'is_login': True}

    def test_encode_returns_token_string(self):
        jwt = JWT(self.key)
        token = jwt.encode(self.payload)
        assert isinstance(token, str)

    def test_decode_returns_payload_dict(self):
        jwt = JWT(self.key)
        token = jwt.encode(self.payload)
        assert jwt.decode(token) == self.payload


class TestSecureKey:

    def test_fernet(self):
        key = SecureKey.fernet()
        assert isinstance(key, bytes)

    def test_bcrypt_hashing(self):
        password = 'my_password'
        hashed_password = SecureKey.bcrypt(password)
        assert isinstance(hashed_password, bytes)

    def test_bcrypt_validation(self):
        password = 'my_password'
        hashed_password = SecureKey.bcrypt(password)
        assert SecureKey.bcrypt(password, hashed_password)

    def test_bcrypt_validation_wrong_password(self):
        password = 'my_password'
        wrong_password = 'wrong_password'
        hashed_password = SecureKey.bcrypt(password)
        assert not SecureKey.bcrypt(wrong_password, hashed_password)
