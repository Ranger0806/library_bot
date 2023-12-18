from aiogram.filters import BaseFilter
from aiogram.types import Message
from library_db import LibraryDB

class StatusFilter(BaseFilter):
    def __init__(self, status: str):
        self.status = status

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.status, str):
            db = LibraryDB()
            if self.status == await db.get_status(user_id=message.from_user.id):
                return True
        else:
            return False
