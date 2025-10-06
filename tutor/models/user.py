from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = ""
    first_name: str = ""
    last_name: str = ""
    lesson_price: float = 0.0
    contact_info: str = ""
    is_active: bool = True
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None