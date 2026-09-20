from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from config import START_GIF

LAST_MENU_MSG: dict[int, int] = {}


async def _edit_any(message: Message, text: str, keyboard: InlineKeyboardMarkup):
    try:
        await message.edit_caption(
            caption=text, reply_markup=keyboard, parse_mode="HTML"
        )
        return
    except TelegramBadRequest as e:
        err = str(e)
        if "message is not modified" in err:
            return
        if "there is no caption" not in err:
            raise

    try:
        await message.edit_text(
            text=text, reply_markup=keyboard, parse_mode="HTML"
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


async def show_screen(event: Message | CallbackQuery, text: str, keyboard: InlineKeyboardMarkup):
    if isinstance(event, CallbackQuery):
        await _edit_any(event.message, text, keyboard)
        LAST_MENU_MSG[event.from_user.id] = event.message.message_id
    else:
        m = await event.answer_animation(
            animation=START_GIF, caption=text, reply_markup=keyboard, parse_mode="HTML"
        )
        LAST_MENU_MSG[event.from_user.id] = m.message_id


async def show_screen_edit(bot: Bot, user_id: int, chat_id: int, text: str, keyboard: InlineKeyboardMarkup):
    msg_id = LAST_MENU_MSG.get(user_id)
    if msg_id:
        try:
            await bot.edit_message_caption(
                chat_id=chat_id, message_id=msg_id,
                caption=text, reply_markup=keyboard, parse_mode="HTML"
            )
            return
        except TelegramBadRequest as e:
            err = str(e)
            if "message is not modified" in err:
                return
            if "there is no caption" in err:
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id, message_id=msg_id,
                        text=text, reply_markup=keyboard, parse_mode="HTML"
                    )
                    return
                except TelegramBadRequest as e2:
                    if "message is not modified" in str(e2):
                        return
    m = await bot.send_animation(
        chat_id=chat_id, animation=START_GIF,
        caption=text, reply_markup=keyboard, parse_mode="HTML"
    )
    LAST_MENU_MSG[user_id] = m.message_id