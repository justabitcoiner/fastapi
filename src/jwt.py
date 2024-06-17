from joserfc import jwk, jwt


class SymmetricKey:
    @classmethod
    def gen_key(cls, file="secret.key", key_size=256):
        key = jwk.OctKey.generate_key(key_size)
        key = key.raw_value
        with open(file, "wb") as f:
            f.write(key)

    @classmethod
    def get_key(cls, file="secret.key"):
        with open(file, "rb") as f:
            key = f.read()
            return jwk.OctKey.import_key(key)


class DigitalSignature:
    @classmethod
    def sign(cls, key, alg, sub):
        header = {"alg": alg}
        claims = {"iss": "justabitcoiner", "sub": sub}
        token_str = jwt.encode(header, claims, key)
        return token_str

    @classmethod
    def verify(cls, value, key):
        token_obj = jwt.decode(value, key)
        header = token_obj.header
        claims = token_obj.claims
        return token_obj


class Jwt:
    @classmethod
    def gen_secret_key(cls):
        SymmetricKey.gen_key()

    @classmethod
    def gen_token(cls, user_id):
        alg = "HS256"
        secret_key = SymmetricKey.get_key()
        return DigitalSignature.sign(secret_key, alg, user_id)
