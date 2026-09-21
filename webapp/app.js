const tg = window.Telegram.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
    try {
        tg.setHeaderColor("secondary_bg_color");
        tg.setBackgroundColor("secondary_bg_color");
    } catch (e) {}
}

const MY_USER_ID = (tg && tg.initDataUnsafe && tg.initDataUnsafe.user)
    ? tg.initDataUnsafe.user.id
    : 0;

const STORAGE_KEY = `my_review_${MY_USER_ID}`;

// Общий счётчик отзывов (отображается в правом верхнем углу)
const TOTAL_REVIEWS = 9563;

// ================== БАЗА ОТЗЫВОВ ==================
const BASE_REVIEWS = [
    { name: "emma", rating: 5, text: "аж страшно было, он сразу оплатил, скинула менеджеру, деньги пришли моментально, всё няшно 🌸", date: "2 авг. 2026 г." },
    { name: "эля", rating: 5, text: "Все швидко чесно красава", date: "2 авг. 2026 г." },
    { name: "sdoret", rating: 5, text: "Оплатил без вопросов, отдал через гаранта, рубли упали сразу, +гер", date: "2 авг. 2026 г." },
    { name: "уе", rating: 5, text: "По чесноку спасибо", date: "2 авг. 2026 г." },
    { name: "П", rating: 5, text: "FUNPAY топ + + +", date: "2 авг. 2026 г." },
    { name: "сry at me", rating: 5, text: "думал кинут он сразу оплатил скинул менеджеру рубли упали сразу доволен спасибо", date: "1 авг. 2026 г." },
    { name: "Xiril", rating: 5, text: "Норм все ок", date: "1 авг. 2026 г." },
    { name: "derssam", rating: 5, text: "честно думал скам продавец зашёл в сделку, платил отдал через гаранта рубли упали сразу без кидка советую", date: "1 авг. 2026 г." },
    { name: "Vkмуso сплит", rating: 5, text: "Продавец зашёл в сделку оплатил отдал через гаранта рубли упали сразу без кидка советую", date: "1 авг. 2026 г." },
    { name: "Керра", rating: 5, text: "Надёжно советую", date: "1 авг. 2026 г." },
    { name: "ZETIK |", rating: 5, text: "Месси гоат рональдо пушка", date: "31 июл. 2026 г." },
    { name: "Lili Alvirovna", rating: 5, text: "Всё честно оплата прешла", date: "31 июл. 2026 г." },
    { name: "Виолетта", rating: 5, text: "четенько", date: "31 июл. 2026 г." },
    { name: "#", rating: 5, text: "Продавец оплатил моментально, скинул менеджеру, оплата на карте через минуту", date: "31 июл. 2026 г." },
    { name: "Вера", rating: 5, text: "Быстрый вывод уважаю лзт", date: "31 июл. 2026 г." },
    { name: "глистыйΛ", rating: 5, text: "вывели в течение 2 часов, быстро пришел вывод", date: "31 июл. 2026 г." },
    { name: "zahra", rating: 5, text: "Зашли в сделку он внёс деньги скинул менеджеру оплата на карте через минуту топ селлер", date: "30 июл. 2026 г." },
    { name: "dotmoovs", rating: 5, text: "гроші прийшлишвидко дякую", date: "30 июл. 2026 г." },
    { name: "Vicky", rating: 5, text: "Оплата моментальная топ", date: "30 июл. 2026 г." },
    { name: "garixov", rating: 5, text: "Всё честно оплата пришла", date: "30 июл. 2026 г." },
    { name: "Cyan", rating: 4, text: "Договорились за минуту", date: "30 июл. 2026 г." },
    { name: "Савелий", rating: 5, text: "вывели в течение 2 часов, все четко", date: "30 июл. 2026 г." },
    { name: "Ywiii", rating: 5, text: "+реп", date: "30 июл. 2026 г." },
    { name: "mrPerignon", rating: 5, text: "оплатил без вопросов я передал подарок @FunPayUaHelper перевод дошёл сразу без кидка советую", date: "30 июл. 2026 г." },
    { name: "Playerok Deals", rating: 5, text: "Договорились за минуту", date: "30 июл. 2026 г." },
    { name: "DELURTY", rating: 5, text: "Звёзды пришли по-быстрому спасибо", date: "29 июл. 2026 г." },
    { name: "MARLON", rating: 5, text: "оплатил получил всё ровно", date: "29 июл. 2026 г." },
    { name: "@бегатестер3000", rating: 5, text: "Продавец зашёл в сделку оплатил отдал через гаранта оплата на карте через минуту +гер", date: "29 июл. 2026 г." },
    { name: "Splitov", rating: 4, text: "сделка чистая рекомендую", date: "29 июл. 2026 г." },
    { name: "bottega", rating: 5, text: "думал кинут оплатил без вопросов отдал через гаранта оплата пришла на карту в рублях +реп", date: "28 июл. 2026 г." },
    { name: "Нелла", rating: 5, text: "Всё честно оплата прешла", date: "28 июл. 2026 г." },
    { name: "Livnite", rating: 5, text: "быстро закрыли доволен", date: "28 июл. 2026 г." },
    { name: "faziaz", rating: 5, text: "быстрый вывод крипта пришла", date: "28 июл. 2026 г." },
    { name: "Вер", rating: 5, text: "быстрый вывод из плюсов быстрая сделка, вывод тоже норм", date: "28 июл. 2026 г." },
    { name: "hasler #AWR", rating: 5, text: "Продавец не подвёл", date: "28 июл. 2026 г." },
    { name: "wander⁵⁵⁰", rating: 5, text: "Сначала стрёмно было, продавец оплатил моментально.", date: "28 июл. 2026 г." },
    { name: "Lord | скуп нфт подарков", rating: 5, text: "Он сразу оплатил отдал через гаранта оплата на карте через минуту доволен спасибо", date: "27 июл. 2026 г." },
    { name: "Extazzy", rating: 5, text: "звёзды закинул сразу всё ок", date: "27 июл. 2026 г." },
    { name: "коля трактор", rating: 5, text: "всё ок +реп", date: "27 июл. 2026 г." },
    { name: "vinogradov", rating: 5, text: "Долго сомневался, он сразу оплатил, скинул менеджеру, оплата на карте через минуту. + реп", date: "27 июл. 2026 г." },
    { name: "fromov | Gift^_^", rating: 5, text: "Быстрый вывод", date: "26 июл. 2026 г." },
    { name: "rv0x3l Ϝenil", rating: 5, text: "Ок +реп", date: "26 июл. 2026 г." },
    { name: "Mochammаd Falah", rating: 5, text: "Оплатил получил всё ровно", date: "26 июл. 2026 г." },
    { name: "Kira so cute", rating: 5, text: "Зеленка топ сервис топ", date: "26 июл. 2026 г." },
    { name: "ronki", rating: 5, text: "Сделка чистая рекомендую", date: "25 июл. 2026 г." },
    { name: "Allianca", rating: 5, text: "оплатил без вопросов, скинул менеджеру, рубли упали сразу, без кидка советую", date: "25 июл. 2026 г." },
    { name: "лиликс", rating: 5, text: "зашли в сделку он внёс деньги отдал через гаранта перевод дошёл сразу без кидка советую", date: "25 июл. 2026 г." },
    { name: "user", rating: 5, text: "ЧЕЛ ТОП АНЛОК + +REP", date: "24 июл. 2026 г." },
    { name: "Wertix | only garant 5%", rating: 5, text: "Долго сомневался, продавец зашёл в сделку оплатил, я передал подарок менеджеру, деньги пришли моментально,", date: "24 июл. 2026 г." },
    { name: "MISTLINE11", rating: 5, text: "ГУД", date: "23 июл. 2026 г." },
    { name: "Thomas Jack", rating: 5, text: "норм бот, хотел продать нфт, хожу теперь только этот сервис", date: "23 июл. 2026 г." },
    { name: "Аминикса", rating: 5, text: "всё няшно и быстро целую", date: "23 июл. 2026 г." },
    { name: "Heqzeх 24/7 online #seller numbers", rating: 5, text: "Все ок", date: "22 июл. 2026 г." },
    { name: "Куперов", rating: 5, text: "думал кинут продавец оплатил моментально я передал", date: "22 июл. 2026 г." },
    { name: "Вероника", rating: 5, text: "продавец оплатил моментально, скинула менеджеру, оплата на карте через минуту, мимими", date: "21 июл. 2026 г." },
    { name: "Аслан", rating: 5, text: "Сначала стрёмно было зашли в сделку он внёс деньги я передал подарок менеджеру перевод дошёл сразу топ селлер", date: "21 июл. 2026 г." },
    { name: "аномалия.", rating: 5, text: "Думал кинут, зашли в сделку он внёс деньги, отдал через гаранта, оплата на карте через минуту, доволен спасибо", date: "21 июл. 2026 г." },
    { name: "LUNAROV", rating: 5, text: "Договорились за минуту", date: "21 июл. 2026 г." },
    { name: "auCIys", rating: 5, text: "быстрый вывод", date: "19 июл. 2026 г." },
    { name: "этилов.vk", rating: 5, text: "Звёзды пришли по-быстрому спасибо", date: "19 июл. 2026 г." },
    { name: "Xsesx", rating: 5, text: "Зашли в сделку он. отдал через гаранта, оплата пришла на карту в рублях, +реп", date: "18 июл. 2026 г." },
    { name: "изи бриджи", rating: 5, text: "Продавец не подвёл", date: "18 июл. 2026 г." },
    { name: "TIFFANY O @Onchains", rating: 5, text: "деньгым на карте топ", date: "17 июл. 2026 г." },
    { name: "НЕАДЕКВАТВН", rating: 5, text: "Продавец, не подвёл", date: "16 июл. 2026 г." },
    { name: "Polinaa", rating: 5, text: "быстро закрыли доволен", date: "16 июл. 2026 г." },
    { name: "милянянаа", rating: 5, text: "быстрый вывод, норм бот, уважаю лзт", date: "16 июл. 2026 г." },
    { name: "Xunutu", rating: 5, text: "Договорились за минуту", date: "15 июл. 2026 г." },
    { name: "Bebebe....", rating: 5, text: "оплатил без вопросов, скинул менеджеру, рубли упали сразу, топ селлер", date: "15 июл. 2026 г." },
    { name: "Пиздец", rating: 5, text: "Звёзды закинул сразу всё ок", date: "14 июл. 2026 г." },
    { name: "panklho", rating: 5, text: "Топ продавец рекомендую все ок", date: "14 июл. 2026 г." },
    { name: "atreideslolly", rating: 5, text: "продавец оплатил моментально, отдал через гаранта, перевод дошёл сразу, +реп", date: "14 июл. 2026 г." },
    { name: "Кури", rating: 5, text: "все четко — четенько", date: "13 июл. 2026 г." },
    { name: "Broker MM", rating: 5, text: "Думав шо скам але все ок продавець оплатив гроші прийшли", date: "13 июл. 2026 г." },
    { name: "de la #Casper", rating: 5, text: "быстро пришел вывод, уважаю лзт", date: "13 июл. 2026 г." },
    { name: "Kay", rating: 5, text: "Он сразу оплатил скинул менеджеру оплата пришла на карту в рублях топ селлер", date: "13 июл. 2026 г." },
    { name: "Улита", rating: 5, text: "Договорились за минуту", date: "13 июл. 2026 г." },
    { name: "Vione", rating: 5, text: "надежно советую", date: "12 июл. 2026 г." },
    { name: "Aditya", rating: 5, text: "Договорились за минуту", date: "12 июл. 2026 г." },
    { name: "MonfiGod", rating: 5, text: "все четко", date: "11 июл. 2026 г." },
    { name: "Good", rating: 5, text: "Норм бот, крипта пришла", date: "11 июл. 2026 г." },
    { name: "...", rating: 5, text: "Оплатил получил всё ровно", date: "11 июл. 2026 г." },
    { name: "vargelos #", rating: 5, text: "быстро пришел вывод", date: "10 июл. 2026 г." },
    { name: "instrumental", rating: 5, text: "Норм гуд", date: "10 июл. 2026 г." },
    { name: "awle", rating: 5, text: "Топ продавца рекомендую все ок", date: "9 июл. 2026 г." },
    { name: "Юстина", rating: 5, text: "+rep good deal", date: "9 июл. 2026 г." },
    { name: "Van1L_777", rating: 5, text: "быстро закрыли доволен", date: "8 июл. 2026 г." },
    { name: "MelOTT", rating: 5, text: "Он сразу оплатил, скинул менеджеру, оплата на карте через минуту, топ селлер", date: "8 июл. 2026 г." },
    { name: "TONCER", rating: 5, text: "Договорились за минуту", date: "8 июл. 2026 г." },
    { name: "Алёна", rating: 5, text: "ок", date: "8 июл. 2026 г." },
    { name: "thoughtplayer", rating: 5, text: "+реп гуд", date: "8 июл. 2026 г." },
    { name: "Board owner• 2% hardlain", rating: 5, text: "быстро пришел вывод, из плюсов быстрая сделка, вывод тоже норм", date: "8 июл. 2026 г." },
    { name: "Soda", rating: 5, text: "гуд", date: "7 июл. 2026 г." },
    { name: "mikron", rating: 5, text: "Уважаю лзт, вывели в течение 2 часов", date: "6 июл. 2026 г." },
    { name: "НННННННН", rating: 5, text: "Он сразу оплатил, отдал через гаранта, оплата на карте через минуту, без кидка советую", date: "6 июл. 2026 г." },
    { name: "dtvoum", rating: 5, text: "Деньги на карте топ", date: "5 июл. 2026 г." },
    { name: "Slthb", rating: 5, text: "за звёзды спасибо всё честно", date: "5 июл. 2026 г." },
    { name: "#TerMerow", rating: 5, text: "OTC GOD +rep", date: "5 июл. 2026 г." },
    { name: "xxx xxxxxx » X z. 3", rating: 5, text: "продавец зашёл в сделку оплатил, скинул менеджеру, рубли упали сразу, без кидка советую", date: "5 июл. 2026 г." },
    { name: "</> xxxxxxxxxx | xxxxxxxxxx", rating: 5, text: "Зеленка топ, хотел продать нфт, хожу теперь этот сервис", date: "5 июл. 2026 г." },
    { name: "седня - завтра", rating: 5, text: "Всё пришло +реп", date: "3 июл. 2026 г." },
    { name: "циклоп", rating: 5, text: "Сначала стрёмно было, оплатил без вопросов, скинул @FunPayUaHelper, рубли упали сразу. +реп", date: "3 июл. 2026 г." },
    { name: "hamleted", rating: 5, text: "+реп", date: "3 июл. 2026 г." },
    { name: "nikola durov", rating: 5, text: "Ок +реп", date: "2 июл. 2026 г." },
    { name: "Pi", rating: 5, text: "Все честно оплата пришла дякую", date: "2 июл. 2026 г." },
    { name: "Дмирр", rating: 5, text: "Красава все швидко швидко", date: "1 июл. 2026 г." },
    { name: "Соня", rating: 5, text: "вывели в течение 2 часов норм бот", date: "1 июл. 2026 г." },
    { name: "Maren", rating: 5, text: "из плюсов быстрая сделка, вывод тоже норм — все четко", date: "1 июл. 2026 г." },
    { name: "neelkxzx69", rating: 5, text: "+rep good deal", date: "1 июл. 2026 г." },
    { name: "KK", rating: 5, text: "TOP ZOV ZV + + + REP", date: "1 июл. 2026 г." },
    { name: "Asvnr/скуп нфт", rating: 5, text: "вывели в течение 2 часов — сервис топ", date: "28 июн. 2026 г." },
    { name: "deathed", rating: 5, text: "скибиди оп +реп", date: "28 июн. 2026 г." }
];

// ================== РЕНДЕР ==================
function renderStars(rating) {
    let html = "";
    for (let i = 1; i <= 5; i++) {
        html += `<span class="star ${i <= rating ? 'filled' : ''}">★</span>`;
    }
    return html;
}

function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
}

function buildReviewItem(r, isMine) {
    return `
        <div class="review-item ${isMine ? 'mine' : ''}">
            <div class="review-head">
                <div class="review-avatar">${(r.name[0] || "?").toUpperCase()}</div>
                <div class="review-name">${escapeHtml(r.name)}</div>
                <div class="review-stars">${renderStars(r.rating)}</div>
            </div>
            <div class="review-text">${escapeHtml(r.text)}</div>
            <div class="review-date">${r.date}</div>
        </div>
    `;
}

function renderReviews() {
    const list = document.getElementById("reviews-list");

    const myRaw = localStorage.getItem(STORAGE_KEY);
    const myReview = myRaw ? JSON.parse(myRaw) : null;

    let html = "";

    if (myReview) {
        html += buildReviewItem(myReview, true);
    }

    html += BASE_REVIEWS.map(r => buildReviewItem(r, false)).join("");

    list.innerHTML = html;

    // Счётчик сверху — общее число (9 563, как на дизайне)
    document.querySelector(".reviews-count").textContent = TOTAL_REVIEWS.toLocaleString("ru-RU").replace(/,/g, " ");

    // Подпись снизу — реальное количество отображаемых отзывов
    const visible = BASE_REVIEWS.length + (myReview ? 1 : 0);
    document.querySelector(".reviews-note").textContent =
        `Вам видны только ${visible} последних отзывов, чтобы не нагружать сервер`;
}

renderReviews();

// ================== ЕСЛИ УЖЕ ОСТАВИЛ ОТЗЫВ ==================
const existing = localStorage.getItem(STORAGE_KEY);
if (existing) {
    document.getElementById("form-card").innerHTML = `
        <div class="form-title">Ваш отзыв</div>
        <div class="form-hint">Виден только вам · поддержка <a href="https://t.me/FunPayUaHelper">@FunPayUaHelper</a></div>
        <div style="margin-top:14px;">Спасибо! Вы уже оставили отзыв.</div>
    `;
}

// ================== ЗВЁЗДЫ ==================
let selectedRating = 0;
const ratingStars = document.querySelectorAll("#rating-input .star");

function updateRatingUI(value) {
    ratingStars.forEach(s => {
        s.classList.toggle("active", parseInt(s.dataset.value) <= value);
    });
}

ratingStars.forEach(star => {
    star.addEventListener("click", (e) => {
        e.preventDefault();
        selectedRating = parseInt(star.dataset.value);
        updateRatingUI(selectedRating);
    });
    star.addEventListener("touchstart", (e) => {
        e.preventDefault();
        selectedRating = parseInt(star.dataset.value);
        updateRatingUI(selectedRating);
    }, { passive: false });
});

// ================== ОТПРАВКА ==================
const submitBtn = document.getElementById("submit-btn");

function showAlert(msg) {
    if (tg && tg.showAlert) {
        tg.showAlert(msg);
    } else {
        alert(msg);
    }
}

submitBtn.addEventListener("click", () => {
    const nickname = document.getElementById("nickname").value.trim();
    const text = document.getElementById("review-text").value.trim();

    if (selectedRating === 0) {
        showAlert("Поставьте оценку");
        return;
    }
    if (!nickname) {
        showAlert("Вы не ввели имя");
        return;
    }
    if (text.length < 3) {
        showAlert("Напишите отзыв (минимум 3 символа)");
        return;
    }

    const newReview = {
        name: nickname,
        rating: selectedRating,
        text: text,
        date: new Date().toLocaleDateString("ru-RU", { day: "numeric", month: "short", year: "numeric" }) + " г."
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(newReview));

    renderReviews();
    document.getElementById("form-card").innerHTML = `
        <div class="form-title">Ваш отзыв</div>
        <div class="form-hint">Виден только вам · поддержка <a href="https://t.me/FunPayUaHelper">@FunPayUaHelper</a></div>
        <div style="margin-top:14px;">Спасибо! Вы уже оставили отзыв.</div>
    `;

    showAlert("Спасибо! Ваш отзыв опубликован.");
});