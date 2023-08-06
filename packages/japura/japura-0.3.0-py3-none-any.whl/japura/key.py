from typing import Dict, Any
from cryptography.fernet import Fernet
from typing import Any, Dict, Optional, Union

import bcrypt
import jwt


class JWT:
    """JSON Web Token (JWT) encoder and decoder.

    Attributes
    ----------
    key : str
        The secret key used to encode and decode JWTs.

    Methods
    -------
    encode(payload: Dict[str, Any]) -> str:
        Encodes the given payload into a JWT using the specified key.
    decode(token: str) -> bool:
        Decodes the given JWT string using the specified key.
    """

    def __init__(self, key: str):
        """Constructs a new JWT encoder and decoder with the specified secret key.

        Parameters
        ----------
        key : str
            The secret key to use for encoding and decoding JWTs.
        """
        self.key = key

    def encode(self, payload: Dict[str, Any]) -> str:
        """Encodes the given payload into a JWT using the specified key.

        Parameters
        ----------
        payload : Dict[str, Any]
            The dictionary containing the payload data to be encoded.

        Returns
        -------
        str
            The encoded JWT string.
        """
        return jwt.encode(payload, self.key, algorithm='HS256')

    def decode(self, token: str) -> bool:
        """Decodes the given JWT string using the specified key.

        Parameters
        ----------
        token : str
            The JWT string to be decoded.

        Returns
        -------
        bool
            True if the JWT was successfully decoded, False otherwise.
        """
        return jwt.decode(token, self.key, algorithms=['HS256'])


class SecureKey:
    """The SecureKey class provides methods to generate and manage secure keys."""

    @staticmethod
    def fernet() -> bytes:
        """Generates a new Fernet key.

        Returns
        -------
        bytes
            A secure key generated using Fernet algorithm.
        """
        return Fernet.generate_key()

    @staticmethod
    def bcrypt(plain: str, hashed: Optional[bytes] = b'') -> Union[bool, bytes]:
        """Generates a bcrypt hash from a plaintext password or checks if a plaintext password matches a bcrypt hash.

        Parameters
        ----------
        plain : str
            The plaintext password to be hashed.
        hashed : Optional[bytes]
            The bcrypt hash to compare the plaintext password against. If not provided, a new hash will be generated.

        Returns
        -------
        Union[bool, bytes]
            If hashed is provided, returns True if the plaintext password matches the hash, False otherwise. 
            If hashed is not provided, returns a new bcrypt hash generated from the plaintext password.
        """
        if not hashed:
            return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=13))
        return bcrypt.checkpw(plain.encode(), hashed)
