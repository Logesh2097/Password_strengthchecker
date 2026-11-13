"""Password strength rules, kept free of any web code so they can be tested."""

from __future__ import annotations

import re

MIN_LENGTH = 8
STRONG = "Password is strong."

# Each rule is (pattern the password must contain, message shown when it does not).
RULES = (
    (r"[A-Z]", "Password must contain at least one uppercase letter."),
    (r"[a-z]", "Password must contain at least one lowercase letter."),
    (r"\d", "Password must contain at least one digit."),
    (
        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
        "Password must contain at least one special character.",
    ),
)


def check_password_strength(password: str) -> str:
    """Return the first rule the password breaks, or ``STRONG`` if it breaks none."""
    if len(password) < MIN_LENGTH:
        return f"Password must be at least {MIN_LENGTH} characters long."
    for pattern, message in RULES:
        if not re.search(pattern, password):
            return message
    return STRONG


def is_strong(password: str) -> bool:
    return check_password_strength(password) == STRONG
