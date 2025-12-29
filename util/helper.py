import hashlib
from datetime import datetime, timezone

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from exception.security_exception import SecurityException

security = HTTPBearer()


def gen_hash_512(data):
    return hashlib.sha512(data.encode("utf-8")).hexdigest()


# authorization: Optional[str] = Header(default=None)
def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security), ):
    return credentials.credentials


def check_same_sector(self, list_first, list_second):
    ids_first = {item['id'] for item in list_first}
    ids_second = {item['id'] for item in list_second}
    return bool(ids_first & ids_second)


def check_token(dict_login):
    if dict_login is None:
        raise SecurityException("Invalid access token", 401)
    if dict_login['expired_at'] is not None:
        raise SecurityException("Invalid token", 401)
    expires_at = dict_login['token_valid_until']
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        raise SecurityException("Token expired", 401)
