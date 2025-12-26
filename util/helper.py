import hashlib

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def gen_hash_512(data):
    return hashlib.sha512(data.encode("utf-8")).hexdigest()

# authorization: Optional[str] = Header(default=None)
def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security),):
    return credentials.credentials
