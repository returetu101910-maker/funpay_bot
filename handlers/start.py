from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import BOT_USERNAME
from keyboards.menus import main_menu_kb, back_kb, language_kb
from utils.notifier import show_screen
from utils.i18n import t, USER_LANGS, LANG_HEADER

router = Router()


def main_text(user_id: int) -> str:
    return (
        f"<b>{t(user_id, 'main_title')}</b>\n\n"
        f"{t(user_id, 'main_desc')}\n\n"
        f"<b>{t(user_id, 'why_choose')}</b>\n"
        "<blockquote>"
        f"• {t(user_id, 'bullet1')}\n"
        f"• {t(user_id, 'bullet2')}\n"
        f"• {t(user_id, 'bullet3')}\n"
        f"• {t(user_id, 'bullet4')}"
        "</blockquote>\n\n"
        f"{t(user_id, 'support')}: @FunPay_officiall"
    )


@router.message(CommandStart(deep_link=False))
async def cmd_start(message: Message):
    uid = message.from_user.id
    await show_screen(message, main_text(uid), main_menu_kb(uid))


@router.callback_query(F.data == "back_to_main")
async def cb_back(call: CallbackQuery):
    uid = call.from_user.id
    await show_screen(call, main_text(uid), main_menu_kb(uid))
    await call.answer()


@router.callback_query(F.data == "language")
async def cb_language(call: CallbackQuery):
    uid = call.from_user.id
    await show_screen(call, LANG_HEADER, language_kb(uid))
    await call.answer()


@router.callback_query(F.data.startswith("lang_"))
async def cb_lang(call: CallbackQuery):
    uid = call.from_user.id
    code = call.data.replace("lang_", "")
    USER_LANGS[uid] = code
    await show_screen(call, main_text(uid), main_menu_kb(uid))
    await call.answer(t(uid, "lang_set"))


@router.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    await call.message.answer(
        f"💬 <b>{t(uid, 'support')}:</b> @FunPay_officiall\n\n"
        "Нажмите на юзернейм выше, чтобы открыть чат."
    )


@router.callback_query(F.data == "referrals")
async def cb_referrals(call: CallbackQuery):
    uid = call.from_user.id
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{uid}"

    text = (
        f"👥 <b>{t(uid, 'referrals_title')}</b>\n\n"
        f"<i>{t(uid, 'referrals_invite')}</i>\n\n"
        f"🔗 <b>{t(uid, 'your_ref_link')}</b>\n"
        f"<blockquote>{link}</blockquote>"
    )
    await show_screen(call, text, back_kb(uid))
    await call.answer()


@router.callback_query(F.data == "reviews")
async def cb_reviews(call: CallbackQuery):
    uid = call.from_user.id
    await show_screen(call, f"<b>{t(uid, 'btn_reviews')}</b>\n\n...", back_kb(uid))
    await call.answer()