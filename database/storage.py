import os
import sqlite3
import time

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "bot.db"
)

_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_cur = _conn.cursor()

_cur.executescript("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    lang TEXT DEFAULT 'ru',
    balance REAL DEFAULT 0,
    stars REAL DEFAULT 0,
    rating INTEGER DEFAULT 0,
    deals_count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS cards (
    user_id INTEGER,
    idx INTEGER,
    number TEXT,
    bank TEXT,
    PRIMARY KEY (user_id, idx)
);
CREATE TABLE IF NOT EXISTS deals (
    deal_id TEXT PRIMARY KEY,
    creator_id INTEGER,
    seller_id INTEGER,
    amount REAL,
    currency TEXT,
    description TEXT,
    method TEXT,
    status TEXT DEFAULT 'waiting_payment',
    created_at INTEGER
);
CREATE TABLE IF NOT EXISTS co_admins (
    user_id INTEGER PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS referrers (
    referred_id INTEGER PRIMARY KEY,
    referrer_id INTEGER
);
CREATE TABLE IF NOT EXISTS ref_counts (
    user_id INTEGER PRIMARY KEY,
    count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS completed_deals (
    user_id INTEGER PRIMARY KEY,
    count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id INTEGER,
    to_id INTEGER,
    text TEXT,
    ts INTEGER
);
""")
_conn.commit()


# ========== USERS ==========
def ensure_user(user_id: int, username: str = ""):
    row = _cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        _cur.execute(
            "INSERT INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username or "")
        )
        _conn.commit()
    else:
        _cur.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            (username or "", user_id)
        )
        _conn.commit()


def get_user(user_id: int) -> dict:
    row = _cur.execute(
        "SELECT user_id, username, lang, balance, stars, rating, deals_count "
        "FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    if not row:
        ensure_user(user_id)
        row = (user_id, "", "ru", 0.0, 0.0, 0, 0)
    return {
        "user_id": row[0],
        "username": row[1],
        "lang": row[2],
        "balance": row[3],
        "stars": row[4],
        "rating": row[5],
        "deals_count": row[6],
    }


def set_balance(user_id: int, amount: float):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET balance = ? WHERE user_id = ?", (amount, user_id))
    _conn.commit()


def set_stars(user_id: int, amount: float):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET stars = ? WHERE user_id = ?", (amount, user_id))
    _conn.commit()


def add_balance(user_id: int, delta: float):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (delta, user_id))
    _conn.commit()


def add_stars(user_id: int, delta: float):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET stars = stars + ? WHERE user_id = ?", (delta, user_id))
    _conn.commit()


def set_rating(user_id: int, rating: int):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET rating = ? WHERE user_id = ?", (rating, user_id))
    _conn.commit()


def set_deals_count(user_id: int, count: int):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET deals_count = ? WHERE user_id = ?", (count, user_id))
    _conn.commit()


def set_lang(user_id: int, lang: str):
    ensure_user(user_id)
    _cur.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    _conn.commit()


# ========== CO-ADMINS ==========
def add_coadmin(user_id: int):
    _cur.execute("INSERT OR IGNORE INTO co_admins (user_id) VALUES (?)", (user_id,))
    _conn.commit()


def is_coadmin(user_id: int) -> bool:
    row = _cur.execute("SELECT 1 FROM co_admins WHERE user_id = ?", (user_id,)).fetchone()
    return row is not None


# ========== CARDS ==========
def get_cards(user_id: int) -> list[dict]:
    rows = _cur.execute(
        "SELECT number, bank FROM cards WHERE user_id = ? ORDER BY idx", (user_id,)
    ).fetchall()
    return [{"number": r[0], "bank": r[1] or ""} for r in rows]


def add_card(user_id: int, number: str, bank: str = ""):
    idx = _cur.execute(
        "SELECT COUNT(*) FROM cards WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    _cur.execute(
        "INSERT INTO cards (user_id, idx, number, bank) VALUES (?, ?, ?, ?)",
        (user_id, idx, number, bank)
    )
    _conn.commit()


def delete_card(user_id: int, idx: int):
    rows = _cur.execute(
        "SELECT number, bank FROM cards WHERE user_id = ? ORDER BY idx", (user_id,)
    ).fetchall()
    if not (0 <= idx < len(rows)):
        return
    _cur.execute("DELETE FROM cards WHERE user_id = ?", (user_id,))
    new_rows = [r for i, r in enumerate(rows) if i != idx]
    for i, (num, bank) in enumerate(new_rows):
        _cur.execute(
            "INSERT INTO cards (user_id, idx, number, bank) VALUES (?, ?, ?, ?)",
            (user_id, i, num, bank)
        )
    _conn.commit()


# ========== DEALS ==========
def create_deal(deal_id: str, creator_id: int, amount: float, currency: str,
                description: str, method: str):
    _cur.execute(
        "INSERT INTO deals (deal_id, creator_id, amount, currency, description, method, "
        "status, created_at) VALUES (?, ?, ?, ?, ?, ?, 'waiting_payment', ?)",
        (deal_id, creator_id, amount, currency, description, method, int(time.time()))
    )
    _conn.commit()


def get_deal(deal_id: str) -> dict | None:
    row = _cur.execute(
        "SELECT deal_id, creator_id, seller_id, amount, currency, description, method, "
        "status, created_at FROM deals WHERE deal_id = ?", (deal_id,)
    ).fetchone()
    if not row:
        return None
    return {
        "deal_id": row[0],
        "creator_id": row[1],
        "seller_id": row[2],
        "amount": row[3],
        "currency": row[4],
        "description": row[5],
        "method": row[6],
        "status": row[7],
        "created_at": row[8],
    }


def update_deal(deal_id: str, **kwargs):
    if not kwargs:
        return
    fields = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [deal_id]
    _cur.execute(f"UPDATE deals SET {fields} WHERE deal_id = ?", values)
    _conn.commit()


# ========== REFERRALS ==========
def add_referral(referrer_id: int, new_user_id: int):
    if new_user_id == referrer_id:
        return
    exists = _cur.execute(
        "SELECT 1 FROM referrers WHERE referred_id = ?", (new_user_id,)
    ).fetchone()
    if exists:
        return
    _cur.execute(
        "INSERT INTO referrers (referred_id, referrer_id) VALUES (?, ?)",
        (new_user_id, referrer_id)
    )
    _cur.execute(
        "INSERT OR IGNORE INTO ref_counts (user_id, count) VALUES (?, 0)", (referrer_id,)
    )
    _cur.execute(
        "UPDATE ref_counts SET count = count + 1 WHERE user_id = ?", (referrer_id,)
    )
    _conn.commit()


def get_referral_count(user_id: int) -> int:
    row = _cur.execute(
        "SELECT count FROM ref_counts WHERE user_id = ?", (user_id,)
    ).fetchone()
    return row[0] if row else 0


# ========== COMPLETED DEALS ==========
def get_completed_deals(user_id: int) -> int:
    row = _cur.execute(
        "SELECT count FROM completed_deals WHERE user_id = ?", (user_id,)
    ).fetchone()
    return row[0] if row else 0


def inc_completed_deals(user_id: int):
    _cur.execute(
        "INSERT OR IGNORE INTO completed_deals (user_id, count) VALUES (?, 0)", (user_id,)
    )
    _cur.execute(
        "UPDATE completed_deals SET count = count + 1 WHERE user_id = ?", (user_id,)
    )
    _conn.commit()


# ========== MESSAGES ==========
def save_message(from_id: int, to_id: int, text: str):
    _cur.execute(
        "INSERT INTO messages (from_id, to_id, text, ts) VALUES (?, ?, ?, ?)",
        (from_id, to_id, text, int(time.time()))
    )
    _conn.commit()


def get_chat_history(user_a: int, user_b: int, limit: int = 50) -> list[dict]:
    rows = _cur.execute(
        "SELECT from_id, to_id, text, ts FROM messages "
        "WHERE (from_id = ? AND to_id = ?) OR (from_id = ? AND to_id = ?) "
        "ORDER BY ts ASC LIMIT ?",
        (user_a, user_b, user_b, user_a, limit)
    ).fetchall()
    return [
        {"from_id": r[0], "to_id": r[1], "text": r[2], "ts": r[3]}
        for r in rows
    ]


def find_user_by_username(username: str) -> int | None:
    if not username:
        return None
    username = username.lstrip("@")
    row = _cur.execute(
        "SELECT user_id FROM users WHERE LOWER(username) = LOWER(?)",
        (username,)
    ).fetchone()
    return row[0] if row else None