from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from login_type_check import is_email
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def create_tokens(user: dict) -> dict:
    identifier = user.get("username") if user.get("username") else user.get("email")

    payload = {'sub': identifier, 'user_id': user['user_id']}

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {"access_token": access_token, "refresh_token": refresh_token}

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def refresh_token(refresh_token: str, actual_user_data: dict) -> str | None:
    payload = verify_token(refresh_token)

    if not payload:
        return None  # Refresh-токен недійсний
    elif payload["sub"] != actual_user_data['email' if is_email(payload["sub"]) else 'username']: # Перевіряємо, чи співпадає ім'я користувача або ел.пошта в токені з актуальним
        return None
    new_access_token = create_access_token(payload)
    return new_access_token
