from typing import Final


class AuthResponseMessage:
    SIGNUP_SUCCESS: Final[str] = "Регистрация успешна"
    SIGNUP_ERROR: Final[str] = "Пользователь уже существует или ошибка БД"
