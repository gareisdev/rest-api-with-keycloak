from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import requests
import os
from pydantic import BaseModel
import sys
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from jose.constants import ALGORITHMS


realm = os.environ["OIDC_REALM_NAME"]
client_id = os.environ["OIDC_CLIENT_ID"]
client_secret = os.environ["OIDC_CLIENT_SECRET"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: Optional[str] = None


def get_public_key():
    try:
        r = requests.get("http://{}/realms/{}".format(
            os.environ["OIDC_SERVER_URL"],
            realm
        ),timeout=3)
        r.raise_for_status()
        response_json = r.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        sys.exit(1)

    return response_json["public_key"]

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS.RS256],
                             options={"verify_signature": True, "verify_aud": False, "exp": True})
        username: str = payload.get("preferred_username")
        token_data = TokenData(username=username)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data


SECRET_KEY = f'-----BEGIN PUBLIC KEY-----\r\n{get_public_key()}\r\n-----END PUBLIC KEY-----'
