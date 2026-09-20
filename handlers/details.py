import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.details_states import DetailsStates
from keyboards.details_kb import details_kb, back_to_details_kb
from utils.notifier import show_screen, show_screen_edit
from database.storage import get_cards, add_card, delete_card

router = Router()


@router.callback_query(F.data == "details")
async def cb_details(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.clear()
    cards = get_cards(uid)
    await show_screen(
        call,
        "💼 <b>Выберите кошелёк для добавления:</b>",
        details_kb(uid, cards)
    )
    await call.answer()


@router.callback_query(F.data == "details_add_card")
async def cb_add_card(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.set_state(DetailsStates.entering_card)
    await show_screen(
        call,
        "✏️ <b>Укажите номер карты и банк (не обязательно):</b>",
        back_to_details_kb(uid)
    )
    await call.answer()


@router.message(DetailsStates.entering_card)
async def process_card(message: Message, state: FSMContext):
    uid = message.from_user.id
    try:
        await message.delete()
    except Exception:
        pass

    raw = (message.text or "").strip()
    digits = re.sub(r"\D", "", raw)

    if len(digits) != 16:
        await show_screen_edit(
            message.bot, uid, message.chat.id,
            "❌ <b>Нужно 16 цифр. Пример:</b>\n"
            "<code>0000 0000 0000 0000</code>",
            back_to_details_kb(uid)
        )
        return

    formatted = f"{digits[0:4]} {digits[4:8]} {digits[8:12]} {digits[12:16]}"
    add_card(uid, formatted)

    await state.clear()
    await show_screen_edit(
        message.bot, uid, message.chat.id,
        "✅ <b>Реквизиты карты успешно добавлены!</b>",
        back_to_details_kb(uid)
    )


@router.callback_query(F.data.startswith("card_del_"))
async def cb_del_card(call: CallbackQuery):
    uid = call.from_user.id
    idx = int(call.data.rsplit("_", 1)[-1])
    delete_card(uid, idx)
    cards = get_cards(uid)
    await show_screen(
        call,
        "💼 <b>Выберите кошелёк для добавления:</b>",
        details_kb(uid, cards)
    )
    await call.answer("Карта удалена")


@router.callback_query(F.data.startswith("card_show_"))
async def cb_show_card(call: CallbackQuery):
    uid = call.from_user.id
    idx = int(call.data.rsplit("_", 1)[-1])
    cards = get_cards(uid)
    if 0 <= idx < len(cards):
        await call.answer(cards[idx]["number"], show_alert=True)
    else:
        await call.answer()