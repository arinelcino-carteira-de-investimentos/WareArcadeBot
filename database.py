"""
===============================================
WareArcadeBot - Banco de Dados
===============================================
Gerenciamento do banco SQLite para clientes,
pedidos e sessões do bot.
===============================================
"""

import sqlite3
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from config import DATABASE_PATH, DOWNLOAD_LINK_EXPIRY_HOURS, DOWNLOAD_BASE_URL


def get_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            telegram_username TEXT,
            nome_completo TEXT,
            email TEXT,
            telefone TEXT,
            cpf TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            telegram_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            price REAL NOT NULL,
            payment_method TEXT,
            status TEXT DEFAULT 'pendente',
            download_token TEXT,
            download_url TEXT,
            download_expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Tabela de carrinho
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            price REAL NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de sessões (estado do usuário)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            telegram_id INTEGER PRIMARY KEY,
            state TEXT DEFAULT 'idle',
            data TEXT DEFAULT '{}',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ────────────────────────────────────────
# CLIENTES
# ────────────────────────────────────────

def get_or_create_customer(telegram_id: int, username: str = None) -> dict:
    """Obtém ou cria um cliente pelo telegram_id."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()

    if row:
        conn.close()
        return dict(row)

    cursor.execute(
        "INSERT INTO customers (telegram_id, telegram_username) VALUES (?, ?)",
        (telegram_id, username)
    )
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)


def update_customer(telegram_id: int, **kwargs) -> dict:
    """Atualiza dados de um cliente."""
    conn = get_connection()
    cursor = conn.cursor()

    valid_fields = ["nome_completo", "email", "telefone", "cpf", "telegram_username"]
    updates = []
    values = []

    for key, value in kwargs.items():
        if key in valid_fields:
            updates.append(f"{key} = ?")
            values.append(value)

    if updates:
        updates.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(telegram_id)
        query = f"UPDATE customers SET {', '.join(updates)} WHERE telegram_id = ?"
        cursor.execute(query, values)
        conn.commit()

    cursor.execute("SELECT * FROM customers WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}


def get_customer(telegram_id: int) -> dict | None:
    """Obtém dados do cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def is_customer_complete(telegram_id: int) -> bool:
    """Verifica se o cadastro do cliente está completo."""
    customer = get_customer(telegram_id)
    if not customer:
        return False
    required = ["nome_completo", "email", "telefone"]
    return all(customer.get(field) for field in required)


# ────────────────────────────────────────
# CARRINHO
# ────────────────────────────────────────

def add_to_cart(telegram_id: int, game_id: int, game_name: str, price: float):
    """Adiciona um jogo ao carrinho."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cart (telegram_id, game_id, game_name, price) VALUES (?, ?, ?, ?)",
        (telegram_id, game_id, game_name, price)
    )
    conn.commit()
    conn.close()


def get_cart(telegram_id: int) -> list:
    """Retorna os itens do carrinho."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE telegram_id = ? ORDER BY added_at", (telegram_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_cart_total(telegram_id: int) -> float:
    """Retorna o total do carrinho."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(price) as total FROM cart WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return row["total"] if row and row["total"] else 0.0


def remove_from_cart(telegram_id: int, cart_item_id: int):
    """Remove um item do carrinho."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id = ? AND telegram_id = ?", (cart_item_id, telegram_id))
    conn.commit()
    conn.close()


def clear_cart(telegram_id: int):
    """Limpa o carrinho do usuário."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()


# ────────────────────────────────────────
# PEDIDOS
# ────────────────────────────────────────

def generate_order_code() -> str:
    """Gera um código único de pedido."""
    return f"NG-{uuid.uuid4().hex[:8].upper()}"


def generate_download_token() -> str:
    """Gera um token único para download."""
    return hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()[:32]


def create_order(telegram_id: int, game_id: int, game_name: str,
                 price: float, payment_method: str) -> dict:
    """Cria um novo pedido."""
    conn = get_connection()
    cursor = conn.cursor()

    customer = get_customer(telegram_id)
    if not customer:
        conn.close()
        return {}

    order_code = generate_order_code()
    download_token = generate_download_token()
    expiry = datetime.now() + timedelta(hours=DOWNLOAD_LINK_EXPIRY_HOURS)
    download_url = f"{DOWNLOAD_BASE_URL}{download_token}"

    cursor.execute("""
        INSERT INTO orders (order_code, customer_id, telegram_id, game_id, game_name,
                          price, payment_method, status, download_token, download_url,
                          download_expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'confirmado', ?, ?, ?)
    """, (
        order_code, customer["id"], telegram_id, game_id, game_name,
        price, payment_method, download_token, download_url, expiry.isoformat()
    ))
    conn.commit()

    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}


def create_orders_from_cart(telegram_id: int, payment_method: str) -> list:
    """Cria pedidos a partir do carrinho e limpa o carrinho."""
    cart_items = get_cart(telegram_id)
    orders = []
    for item in cart_items:
        order = create_order(
            telegram_id, item["game_id"], item["game_name"],
            item["price"], payment_method
        )
        if order:
            orders.append(order)
    clear_cart(telegram_id)
    return orders


def get_customer_orders(telegram_id: int) -> list:
    """Retorna os pedidos de um cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE telegram_id = ? ORDER BY created_at DESC",
        (telegram_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_order_by_code(order_code: str) -> dict | None:
    """Retorna um pedido pelo código."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_orders() -> list:
    """Retorna todos os pedidos (admin)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ────────────────────────────────────────
# SESSÕES (controle de estado do usuário)
# ────────────────────────────────────────

def get_user_state(telegram_id: int) -> tuple:
    """Retorna (state, data) do usuário."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state, data FROM user_sessions WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row["state"], json.loads(row["data"])
    return "idle", {}


def set_user_state(telegram_id: int, state: str, data: dict = None):
    """Define o estado do usuário."""
    conn = get_connection()
    cursor = conn.cursor()
    data_json = json.dumps(data or {})
    cursor.execute("""
        INSERT INTO user_sessions (telegram_id, state, data, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(telegram_id)
        DO UPDATE SET state = ?, data = ?, updated_at = ?
    """, (
        telegram_id, state, data_json, datetime.now().isoformat(),
        state, data_json, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def clear_user_state(telegram_id: int):
    """Limpa o estado do usuário."""
    set_user_state(telegram_id, "idle", {})
    # ════════════════════════════════════════
# COMPROVANTES E APROVAÇÃO DE PAGAMENTO
# ════════════════════════════════════════

def update_order_status(order_code: str, status: str, admin_id: int = None):
    """Atualiza o status de um pedido (pendente, aprovado, rejeitado)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if status == "aprovado":
        cursor.execute("""
            UPDATE orders 
            SET status = ?, paid_at = ?
            WHERE order_code = ?
        """, (status, datetime.now().isoformat(), order_code))
    else:
        cursor.execute(
            "UPDATE orders SET status = ? WHERE order_code = ?",
            (status, order_code)
        )
    
    conn.commit()
    conn.close()


def save_payment_proof(order_codes: list, file_id: str, file_type: str):
    """Salva o ID do arquivo de comprovante nos pedidos."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Cria tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_proofs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT NOT NULL,
            file_id TEXT NOT NULL,
            file_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_code) REFERENCES orders(order_code)
        )
    """)
    
    for code in order_codes:
        cursor.execute("""
            INSERT INTO payment_proofs (order_code, file_id, file_type)
            VALUES (?, ?, ?)
        """, (code, file_id, file_type))
    
    conn.commit()
    conn.close()


def get_orders_by_codes(codes: list) -> list:
    """Retorna pedidos por uma lista de códigos."""
    if not codes:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join(["?"] * len(codes))
    cursor.execute(
        f"SELECT * FROM orders WHERE order_code IN ({placeholders})",
        codes
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_pending_orders() -> list:
    """Retorna pedidos pendentes de aprovação (admin)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM orders WHERE status = 'aguardando_aprovacao' ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]