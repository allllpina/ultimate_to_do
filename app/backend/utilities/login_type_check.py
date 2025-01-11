import re

def is_email(value: str) -> bool:
    """Перевіряє, чи є рядок поштовою адресою"""
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, value) is not None

def is_username(value: str) -> bool:
    """Перевіряє, чи є рядок ім'ям користувача"""
    # Перевірка, чи є рядок лише з букв, цифр та підкреслень
    username_regex = r"^[a-zA-Z0-9_]+$"
    return re.match(username_regex, value) is not None