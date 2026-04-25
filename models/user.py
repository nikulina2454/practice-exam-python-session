from datetime import datetime
import re

class User:
    def __init__(self, username, email, role) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if role not in {"admin", "manager", "developer"}:
            raise ValueError("Role must be admin, manager, or developer")

        self.id = None
        self.username = username.strip()
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        if not isinstance(email, str):
            return False
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            if not isinstance(username, str) or not username.strip():
                raise ValueError("Username must be a non-empty string")
            self.username = username.strip()

        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format")
            self.email = email

        if role is not None:
            if role not in {"admin", "manager", "developer"}:
                raise ValueError("Role must be admin, manager, or developer")
            self.role = role

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "registration_date": self.registration_date,
        }