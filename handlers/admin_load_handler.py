from aiogram import Router, F, Bot
from pathlib import Path
from keybords.adm_keybord import create_keybord
import os
from library_db import LibraryDB
from Config import *
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.exceptions import TelegramNetworkError
from Filters.filter import StatusFilter
from Filters.filter_adm import AdmFilter


router = Router()


@router.callback_query(F.data == "prose" and AdmFilter(role=ROLE))
async def prose_callback(call_back: CallbackQuery):
    try:
        db = LibraryDB()
        await db.set_folder(user_id=call_back.from_user.id, folder="prose")
        folder_name = "prose"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        await call_back.message.answer("Отправьте файлы с книгами")
    except Exception as e:
        await call_back.message.answer("Unexpected error")
        await call_back.answer("Please try again")

@router.message(StatusFilter(status=SET_STATUS_LOAD) and AdmFilter(role=ROLE))
async def upload_file(message: Message.content_type = "file"):
    bot = Bot(token=BOT_TOKEN)
    db = LibraryDB()
    await bot.download(file=message.document,
                       destination=f"{await db.get_folder(user_id=message.from_user.id)}\\{str(message.document)}")
    if os.path.isfile(
            f"{await db.get_folder(user_id=message.from_user.id)}\\{str(message.document.file_name)}"):
        pass
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="*Что-то пошло не так\nОбратитесь к @NET_RUN_NER*",
                               parse_mode="Markdown", reply_markup=create_keybord())
    await db.set_status(user_id=message.from_user.id, status=SET_STATUS_DEFAULT)
    await bot.send_message(chat_id=message.from_user.id, text="*Всё успешно загружено!*", parse_mode="Markdown",
                           reply_markup=create_keybord())
