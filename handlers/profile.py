from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.menus import profile_kb
from utils.notifier import show_screen
from utils.i18n import t
from database.storage import get_user

router = Router()


def stars_line(rating: int) -> str:
    return "★" * rating + "☆" * (5 - rating)


@router.callback_query(F.data == "profile")
async def cb_profile(call: CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    text = (
        f"👤 <b>{t(uid, 'profile')}</b>\n\n"
        f"💰 <b>{t(uid, 'balance')}</b>\n"
        f"{u['balance']:.2f}\n\n"
        f"⭐ <b>Звёзды:</b> {u['stars']:.0f}\n\n"
        f"📊 <b>{t(uid, 'successful_deals')}</b> {u['deals_count']}\n\n"
        f"⭐ <b>{t(uid, 'level')}</b> {t(uid, 'novice')}\n"
        f"🛡 <b>{t(uid, 'commission')}</b> 3%\n"
        f"📈 <b>{t(uid, 'rating')}</b> {stars_line(u['rating'])} "
        f"<b>{u['rating']}.0/5 ({u['deals_count']})</b>"
    )
    await show_screen(call, text, profile_kb(uid))
    await call.answer()