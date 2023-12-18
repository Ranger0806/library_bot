from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keybords.adm_keybord import create_keybord
from library_db import LibraryDB
from Config import *
from Filters.filter_adm import AdmFilter
from Filters.filter import StatusFilter

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        db = LibraryDB()
        if not await db.cheker_user(user_id=message.from_user.id):
            await db.get_new_user(user_id=message.from_user.id, name=message.from_user.first_name, status=SET_STATUS_DEFAULT, folder=SET_STATUS_DEFAULT, role=SET_STATUS_DEFAULT)
        else:
            await db.set_status(status=SET_STATUS_DEFAULT, user_id=message.from_user.id)
        await message.answer(
            f"*Привет {message.from_user.first_name}! Добро пожаловать в бесплатную библиотеку в телеграмм!*\n\nСписок жанров на выбор:",
            reply_markup=create_keybord(), parse_mode="Markdown")
    except Exception as e:
        await message.answer("Unexpected error")

@router.message(Command("admin") and AdmFilter(role=ROLE) and StatusFilter(status=SET_STATUS_DEFAULT))
async def cmd_start(message: Message):
    try:
        db = LibraryDB()
        await db.set_status(user_id=message.from_user.id, status=SET_STATUS_LOAD)
        await message.answer("Приветствую админ! Загрузите книги в выбранную папку", reply_markup=create_keybord())
    except Exception as e:
        await message.answer("Unexpected error")