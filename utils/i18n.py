USER_LANGS: dict[int, str] = {}


LANG_HEADER = (
    "🇬🇧 Select language:\n"
    "🇷🇺 Выберите язык:\n"
    "🇨🇳 选择语言：\n"
    "🇸🇦 اختر اللغة:"
)


TRANSLATIONS = {
    "ru": {
        "main_title": "FunPay · Официальная OTC-платформа",
        "main_desc": "Мы предоставляем полностью автоматизированный сервис гаранта для безопасного обмена цифровыми активами.",
        "why_choose": "Почему выбирают нас?",
        "bullet1": "Средства блокируются в блокчейне — прозрачно и безопасно",
        "bullet2": "Автоматическая проверка оплаты и передачи товара",
        "bullet3": "Система рейтинга покупателей и продавцов",
        "bullet4": "Поддержка 24/7",
        "support": "Поддержка",
        "btn_create_deal": "Создать сделку",
        "btn_profile": "Профиль",
        "btn_withdraw": "Вывод",
        "btn_details": "Реквизиты",
        "btn_referrals": "Рефералы",
        "btn_language": "Язык",
        "btn_reviews": "Отзывы",
        "btn_support": "Поддержка",
        "btn_back": "Назад",
        "profile": "Профиль:",
        "balance": "Баланс:",
        "successful_deals": "Успешные сделки:",
        "level": "Уровень:",
        "commission": "Комиссия:",
        "rating": "Рейтинг:",
        "novice": "Новичок",
        "referrals_title": "Реферальная программа:",
        "referrals_invite": "Приглашайте друзей и получайте вознаграждение!",
        "your_ref_link": "Ваша ссылка:",
        "ref_count": "Приглашено:",
        "choose_lang": "Выберите язык:",
        "lang_set": "Язык изменён",
    },
    "en": {
        "main_title": "FunPay · Official OTC Platform",
        "main_desc": "We provide a fully automated escrow service for secure exchange of digital assets.",
        "why_choose": "Why choose us?",
        "bullet1": "Funds are locked in blockchain — transparent and secure",
        "bullet2": "Automatic verification of payment and item delivery",
        "bullet3": "Rating system for buyers and sellers",
        "bullet4": "24/7 support",
        "support": "Support",
        "btn_create_deal": "Create deal",
        "btn_profile": "Profile",
        "btn_withdraw": "Withdraw",
        "btn_details": "Details",
        "btn_referrals": "Referrals",
        "btn_language": "Language",
        "btn_reviews": "Reviews",
        "btn_support": "Support",
        "btn_back": "Back",
        "profile": "Profile:",
        "balance": "Balance:",
        "successful_deals": "Successful deals:",
        "level": "Level:",
        "commission": "Commission:",
        "rating": "Rating:",
        "novice": "Novice",
        "referrals_title": "Referral program:",
        "referrals_invite": "Invite friends and get rewarded!",
        "your_ref_link": "Your link:",
        "ref_count": "Invited:",
        "choose_lang": "Choose your language:",
        "lang_set": "Language changed",
    },
    "zh": {
        "main_title": "FunPay · 官方场外交易平台",
        "main_desc": "我们提供全自动化的担保服务，确保数字资产的安全交换。",
        "why_choose": "为什么选择我们？",
        "bullet1": "资金锁定在区块链中 —— 透明且安全",
        "bullet2": "自动验证付款和商品交付",
        "bullet3": "买家和卖家评分系统",
        "bullet4": "24/7 支持",
        "support": "支持",
        "btn_create_deal": "创建交易",
        "btn_profile": "个人资料",
        "btn_withdraw": "提现",
        "btn_details": "支付信息",
        "btn_referrals": "推荐",
        "btn_language": "语言",
        "btn_reviews": "评价",
        "btn_support": "支持",
        "btn_back": "返回",
        "profile": "个人资料：",
        "balance": "余额：",
        "successful_deals": "成功交易：",
        "level": "等级：",
        "commission": "佣金：",
        "rating": "评分：",
        "novice": "新手",
        "referrals_title": "推荐计划：",
        "referrals_invite": "邀请好友并获得奖励！",
        "your_ref_link": "您的链接：",
        "ref_count": "已邀请：",
        "choose_lang": "选择语言：",
        "lang_set": "语言已更改",
    },
    "ar": {
        "main_title": "FunPay · منصة OTC الرسمية",
        "main_desc": "نحن نقدم خدمة ضمان مؤتمتة بالكامل لتبادل الأصول الرقمية بشكل آمن.",
        "why_choose": "لماذا يختاروننا؟",
        "bullet1": "الأموال محجوزة في البلوكشين — شفافة وآمنة",
        "bullet2": "التحقق التلقائي من الدفع وتسليم المنتج",
        "bullet3": "نظام تقييم المشترين والبائعين",
        "bullet4": "دعم على مدار الساعة",
        "support": "الدعم",
        "btn_create_deal": "إنشاء صفقة",
        "btn_profile": "الملف الشخصي",
        "btn_withdraw": "سحب",
        "btn_details": "بيانات الدفع",
        "btn_referrals": "الإحالات",
        "btn_language": "اللغة",
        "btn_reviews": "التقييمات",
        "btn_support": "الدعم",
        "btn_back": "رجوع",
        "profile": "الملف الشخصي:",
        "balance": "الرصيد:",
        "successful_deals": "الصفقات الناجحة:",
        "level": "المستوى:",
        "commission": "العمولة:",
        "rating": "التقييم:",
        "novice": "مبتدئ",
        "referrals_title": "برنامج الإحالة:",
        "referrals_invite": "ادعُ أصدقاءك واحصل على مكافأة!",
        "your_ref_link": "رابطك:",
        "ref_count": "تمت الدعوة:",
        "choose_lang": "اختر اللغة:",
        "lang_set": "تم تغيير اللغة",
    },
}


def t(user_id: int, key: str, **kwargs) -> str:
    lang = USER_LANGS.get(user_id, "ru")
    pack = TRANSLATIONS.get(lang, TRANSLATIONS["ru"])
    text = pack.get(key, TRANSLATIONS["ru"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text


COUNTRIES = [
    ("ru", "🇷🇺", "Русский"),
    ("en", "🇬🇧", "English"),
    ("zh", "🇨🇳", "中文"),
    ("ar", "🇸🇦", "العربية"),
]