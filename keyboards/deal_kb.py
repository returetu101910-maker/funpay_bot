from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.i18n import t


def deal_method_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Карта / Card", callback_data="deal_method_card", style="success")
    builder.button(text="Звёзды / Stars", callback_data="deal_method_stars", style="success")
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="back_to_main",
        style="danger"
    )
    builder.adjust(1, 1, 1)
    return builder.as_markup()


def deal_currency_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for c in ["RUB", "KZT", "UAH", "BYN", "AZN", "AMD", "EUR", "UZS"]:
        builder.button(text=c, callback_data=f"deal_currency_{c}", style="success")
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="deal_back_to_method",
        style="danger"
    )
    builder.adjust(4, 4, 1)
    return builder.as_markup()


def deal_amount_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="deal_back_to_currency",
        style="danger"
    )
    builder.adjust(1)
    return builder.as_markup()


def deal_description_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="deal_back_to_amount",
        style="danger"
    )
    builder.adjust(1)
    return builder.as_markup()


def deal_card_kb(user_id: int, deal_id: str, link: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📤 Поделиться ссылкой",
        url=f"https://t.me/share/url?url={link}",
        style="success"
    )
    builder.button(
        text="💬 Саппорт",
        url="https://t.me/FunPay_officiall",
        style="primary"
    )
    builder.button(text="🔴 Выйти из сделки", callback_data="deal_cancel", style="danger")
    builder.adjust(1, 1, 1)
    return builder.as_markup()


def deal_offer_kb(user_id: int, deal_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Принять", callback_data=f"deal_accept_{deal_id}", style="success")
    builder.button(text="🔴 Отклонить", callback_data=f"deal_decline_{deal_id}", style="danger")
    builder.adjust(1, 1)
    return builder.as_markup()


def deal_seller_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💬 Саппорт",
        url="https://t.me/FunPay_officiall",
        style="primary"
    )
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="back_to_main",
        style="danger"
    )
    builder.adjust(1, 1)
    return builder.as_markup()


def deal_done_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(user_id, "btn_withdraw"), callback_data="withdraw", style="success")
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="back_to_main",
        style="danger"
    )
    builder.adjust(1, 1)
    return builder.as_markup()


def deal_cancelled_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"← {t(user_id, 'btn_back')}",
        callback_data="back_to_main",
        style="danger"
    )
    builder.adjust(1)
    return builder.as_markup()