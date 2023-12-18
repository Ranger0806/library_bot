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


@router.callback_query(F.data == "prose" and AdmFilter(role=SET_STATUS_DEFAULT))
async def prose_callback(call_back: CallbackQuery):
    try:
        db = LibraryDB()
        await db.set_status(user_id=call_back.from_user.id, status=SET_STATUS_WATCH)
        await db.set_folder(user_id=call_back.from_user.id, folder="prose")
        folder_name = "prose"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        folder = Path(folder_name)
        if len(list(folder.iterdir())) == 0:
            await call_back.message.answer("Нет доступных книг!", reply_markup=create_keybord())
            await call_back.answer("Запрос выполнен!")
        else:
            str_files = ""
            for i in os.listdir(folder_name):
                str_files += i + "\n"
            await call_back.message.answer(
                f"Список доступных книг.\n\n{str_files}\nОтправьте название книг или кгиги чтобы получить их. Введите название в формате (название.расширение) (так же вы можете вводить несколько книг через 'файл.расширение, файл.расширение и т.д' либо введя их в сообщении по одному в столбик)*",
                reply_markup=create_keybord())
            await call_back.answer("Запрос выполнен!")

    except Exception as e:
        print(e)
        await call_back.message.answer("Unexpected error")
        await call_back.answer("Please try again")


@router.message(StatusFilter(status=SET_STATUS_WATCH) and AdmFilter(role=SET_STATUS_DEFAULT))
async def get_book(message: Message):
    db = LibraryDB()
    bot = Bot(token=BOT_TOKEN)
    if await db.get_status(user_id=message.from_user.id) == SET_STATUS_WATCH:
        try:
            msg = message.text.lower()
            await message.delete() - 1
            if msg.count(", ") > 0:
                msg = msg.split(", ")
                for f in msg:
                    await bot.send_document(chat_id=message.from_user.id, document=FSInputFile(
                        path=f"{await db.get_folder(user_id=message.from_user.id)}\\{f}"))
                await db.set_status(user_id=message.from_user.id, status=SET_STATUS_DEFAULT)
                await bot.send_message(chat_id=message.from_user.id, text="*Вернуться к выбору книг:*",
                                       reply_markup=create_keybord(), parse_mode="Markdown")

            elif msg.count(",") > 0:
                msg = msg.split(",")
                for f in msg:
                    await bot.send_document(chat_id=message.from_user.id, document=FSInputFile(
                        path=f"{await db.get_folder(user_id=message.from_user.id)}\\{f}"))
                await db.set_status(user_id=message.from_user.id, status=SET_STATUS_DEFAULT)
                await bot.send_message(chat_id=message.from_user.id, text="*Вернуться к выбору книг:*",
                                       reply_markup=create_keybord(), parse_mode="Markdown")

            elif msg.count("\n") >= 0:
                msg = msg.split("\n")
                for f in msg:
                    await bot.send_document(chat_id=message.from_user.id, document=FSInputFile(
                        path=f"{await db.get_folder(user_id=message.from_user.id)}\\{f}"))
                await db.set_status(user_id=message.from_user.id, status=SET_STATUS_DEFAULT)
                await bot.send_message(chat_id=message.from_user.id, text="*Вернуться к выбору книг:*",
                                       reply_markup=create_keybord(), parse_mode="Markdown")

        except TelegramNetworkError:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="*Данные введены не корректно попробуйте еще раз!*",
                                   reply_markup=create_keybord(), parse_mode="Markdown")
