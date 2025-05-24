from datetime import datetime
from datetime import timezone as time
from typing import Optional
from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: Optional[UUID]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    hashed_password: str
    is_active: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(time.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(time.utc)
