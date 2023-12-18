from aiogram.filters import BaseFilter
from aiogram.types import Message
from library_db import LibraryDB

class AdmFilter(BaseFilter):
    def __init__(self, role: str):
        self.role = role

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.role, str):
            db = LibraryDB()
            if self.role == await db.get_role(user_id=message.from_user.id):
                return True
        else:
            return False
