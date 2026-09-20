from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.i18n import t


def mask_card(number: str) -> str:
    digits = "".join(ch for ch in number if ch.isdigit())
    if len(digits) < 10:
        return number
    return f"{digits[:6]}...{digits[-4:]}"


def details_kb(user_id: int, cards: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, card in enumerate(cards):
        builder.button(
            text=mask_card(card["number"]),
            callback_data=f"card_show_{idx}",
            style="success"
        )
        builder.button(
            text="🗑 Удалить",
            callback_data=f"card_del_{idx}",
            style="danger"
        )

    builder.button(text="💳 Добавить карту", callback_data="details_add_card", style="success")
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="back_to_main",
        style="danger"
    )

    if cards:
        builder.adjust(*([2] * len(cards)), 1, 1)
    else:
        builder.adjust(1, 1)

    return builder.as_markup()


def back_to_details_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="details",
        style="danger"
    )
    builder.adjust(1)
    return builder.as_markup()