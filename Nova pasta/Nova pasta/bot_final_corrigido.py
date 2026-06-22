"""
================================================================
🎮 WareArcadeBot - Versão Final Corrigida
================================================================
Bot: @warecade_bot
Versão: 4.1 - Com adapter requests completo
================================================================
"""

import os
import logging
import math
import sqlite3
import json
import uuid
import hashlib
import smtplib
import asyncio
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode
from telegram.request import BaseRequest, RequestData
from telegram.error import NetworkError, TimedOut
from dotenv import load_dotenv

load_dotenv()

# ════════════════════════════════════════════════════════════════
# REQUESTS ADAPTER COMPLETO
# ════════════════════════════════════════════════════════════════

class RequestsAdapter(BaseRequest):
    """Adaptador completo usando requests em vez de httpx."""
    
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self.session = None
    
    async def initialize(self) -> None:
        """Inicializa a sessão."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Telegram Bot SDK (https://github.com/python-telegram-bot)',
            'Connection': 'keep-alive',
        })
    
    async def shutdown(self) -> None:
        """Fecha a sessão."""
        if self.session:
            self.session.close()
            self.session = None
    
    async def do_request(self, request: RequestData) -> Tuple[int, Dict[str, Any]]:
        """Executa a requisição usando requests."""
        if self.session is None:
            await self.initialize()
        
        url = request.url
        method = request.method.upper()
        headers = request.headers or {}
        data = request.data or {}
        timeout = request.timeout or self.timeout
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                if request.files:
                    files = {}
                    for key, value in request.files.items():
                        files[key] = (value.filename, value.content, value.content_type)
                    response = self.session.post(
                        url, headers=headers, data=data, files=files, timeout=timeout
                    )
                else:
                    response = self.session.post(
                        url, headers=headers, json=data, timeout=timeout
                    )
            else:
                response = self.session.request(
                    method, url, headers=headers, json=data, timeout=timeout
                )
            
            response.raise_for_status()
            
            if response.text:
                try:
                    return response.status_code, response.json()
                except json.JSONDecodeError:
                    return response.status_code, {"text": response.text}
            return response.status_code, {}
            
        except requests.exceptions.Timeout as e:
            raise TimedOut(f"Timeout: {e}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request error: {e}")


# ════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ════════════════════════════════════════════════════════════════

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "WareArcadeBot")

try:
    ADMIN_CHAT_IDS = [int(x.strip()) for x in os.getenv("ADMIN_CHAT_IDS", "0").split(",") if x.strip()]
except ValueError:
    ADMIN_CHAT_IDS = []

DOWNLOAD_BASE_URL = os.getenv("DOWNLOAD_BASE_URL", "https://warearcadebot.com.br/downloads/")
DOWNLOAD_LINK_EXPIRY_HOURS = int(os.getenv("DOWNLOAD_LINK_EXPIRY_HOURS", "48"))

DATABASE_PATH = os.getenv("DATABASE_PATH", "warearcade.db")
ITEMS_PER_PAGE = 6

STORE_NAME = "🎮 WareArcadeBot - Nexus Digital Shop"
STORE_WEBSITE = "https://warearcadebot.com.br/"
STORE_EMAIL = "warearcadebot@gmail.com"
STORE_INSTAGRAM = "@warearcadebot"
STORE_HOURS = "Seg a Sex: 9h-19h | Sáb: 9h-14h"
STORE_WHATSAPP = "+5511940462611"

PIX_CHAVE = os.getenv("PIX_CHAVE", "11940462611")
PIX_NOME = os.getenv("PIX_NOME", "Arinelcino Gonçalves de Sena")
PIX_CIDADE = os.getenv("PIX_CIDADE", "Sao Paulo")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# CATÁLOGO DE PRODUTOS
# ════════════════════════════════════════════════════════════════

GAMES_CATALOG = [
    {"id": 1, "nome": "House Flipper Remastered Collection", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Coleção remasterizada do simulador de reformas.", "categorias": ["Simulação"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/613100/header.jpg"},
    {"id": 2, "nome": "Manor Lords", "preco_original": 26.90, "preco_oferta": 26.90, "descricao": "Jogo de estratégia e construção medieval.", "categorias": ["Estratégia"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1363080/header.jpg"},
    {"id": 3, "nome": "Need for Speed Most Wanted Limited Edition", "preco_original": 34.90, "preco_oferta": 24.90, "descricao": "Edição limitada do clássico de corrida.", "categorias": ["Corrida"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/24740/header.jpg"},
    {"id": 4, "nome": "Red Dead Redemption 2", "preco_original": 64.90, "preco_oferta": 38.90, "descricao": "Ação e aventura no Velho Oeste.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1174180/header.jpg"},
    {"id": 5, "nome": "Elden Ring", "preco_original": 45.90, "preco_oferta": 32.90, "descricao": "RPG de ação em mundo aberto.", "categorias": ["RPG", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg"},
    {"id": 6, "nome": "God of War Ragnarok", "preco_original": 69.90, "preco_oferta": 32.90, "descricao": "Continuação épica de Kratos.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2322010/header.jpg"},
    {"id": 7, "nome": "Spider-Man Remastered", "preco_original": 42.40, "preco_oferta": 29.90, "descricao": "Marvel's Spider-Man Remasterizado.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1817070/header.jpg"},
    {"id": 8, "nome": "The Last of Us Part I", "preco_original": 48.90, "preco_oferta": 33.90, "descricao": "A jornada épica de Joel e Ellie.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1888930/header.jpg"},
    {"id": 9, "nome": "Cyberpunk 2077", "preco_original": 59.90, "preco_oferta": 29.90, "descricao": "RPG futurista em mundo aberto.", "categorias": ["RPG", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg"},
    {"id": 10, "nome": "Hogwarts Legacy", "preco_original": 69.90, "preco_oferta": 34.90, "descricao": "Explore Hogwarts neste RPG mágico.", "categorias": ["RPG", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/990080/header.jpg"},
    
    {"id": 100, "nome": "Windows 11 Pro - Licença Vitalícia", "preco_original": 899.90, "preco_oferta": 89.90, "descricao": "Licença ORIGINAL Windows 11 Pro vitalícia.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 101, "nome": "Windows 10 Pro - Licença Vitalícia", "preco_original": 699.90, "preco_oferta": 69.90, "descricao": "Licença ORIGINAL Windows 10 Pro vitalícia.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    
    {"id": 110, "nome": "Microsoft Office 2021 Pro Plus", "preco_original": 1899.90, "preco_oferta": 79.90, "descricao": "Office 2021 Pro Plus VITALÍCIO.", "categorias": ["Office"], "oferta": True, "plataforma": "PC", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"},
    
    {"id": 120, "nome": "Adobe Photoshop 2024 - Lifetime", "preco_original": 1899.90, "preco_oferta": 149.90, "descricao": "Adobe Photoshop 2024 completo.", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "🎨 Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/Adobe_Photoshop_CC_icon.svg"},
    
    {"id": 130, "nome": "AutoCAD 2024 - Profissional", "preco_original": 9999.90, "preco_oferta": 299.90, "descricao": "AutoCAD 2024 completo.", "categorias": ["Engenharia"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg"},
    
    {"id": 140, "nome": "Norton 360 Deluxe", "preco_original": 399.90, "preco_oferta": 89.90, "descricao": "Norton 360 Deluxe. Antivírus + VPN.", "categorias": ["Antivírus"], "oferta": True, "plataforma": "Multi", "tipo": "🔒 Segurança", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Norton_AntiVirus_logo.png"},
    
    {"id": 150, "nome": "WinRAR Premium - Vitalício", "preco_original": 149.90, "preco_oferta": 29.90, "descricao": "WinRAR Premium vitalício.", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "🛠️ Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},
    
    {"id": 160, "nome": "Netflix Premium 4K - 30 dias", "preco_original": 55.90, "preco_oferta": 19.90, "descricao": "Netflix Premium 4K por 30 dias.", "categorias": ["Streaming"], "oferta": True, "plataforma": "Multi", "tipo": "🎬 Streaming", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"},
    
    {"id": 165, "nome": "Spotify Premium - 30 dias", "preco_original": 21.90, "preco_oferta": 9.90, "descricao": "Spotify Premium por 30 dias.", "categorias": ["Música"], "oferta": True, "plataforma": "Multi", "tipo": "🎵 Música", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg"},
    
    {"id": 168, "nome": "Steam Gift Card R$ 50", "preco_original": 50.00, "preco_oferta": 42.90, "descricao": "Cartão Steam R$ 50,00.", "categorias": ["Gift Card"], "oferta": True, "plataforma": "PC", "tipo": "🎁 Gift Card", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg"},
    
    {"id": 172, "nome": "Google One 2TB - 1 ano", "preco_original": 449.90, "preco_oferta": 189.90, "descricao": "Google One 2TB por 1 ano.", "categorias": ["Cloud"], "oferta": True, "plataforma": "Multi", "tipo": "☁️ Cloud", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/c/c6/Google_One_logo.svg"},
    
    {
        "id": 999,
        "nome": "🧪 TESTE DO ARI - R$ 1,50",
        "preco_original": 1.50,
        "preco_oferta": 1.50,
        "descricao": "✅ Produto de teste para validar o fluxo completo!",
        "categorias": ["Destaques"],
        "oferta": True,
        "plataforma": "PC",
        "tipo": "🧪 Teste",
        "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/440/header.jpg"
    },
]


# ════════════════════════════════════════════════════════════════
# FUNÇÕES DO CATÁLOGO
# ════════════════════════════════════════════════════════════════

def get_game_by_id(game_id):
    for game in GAMES_CATALOG:
        if game["id"] == game_id:
            return game
    return None

def search_games(query):
    query_lower = query.lower()
    return [g for g in GAMES_CATALOG if query_lower in g["nome"].lower()]

def get_offers():
    return [g for g in GAMES_CATALOG if g["oferta"]]

def format_price(game):
    if game["oferta"] and game["preco_original"] != game["preco_oferta"]:
        return f"~R$ {game['preco_original']:.2f}~ → *R$ {game['preco_oferta']:.2f}* 🏷️"
    return f"*R$ {game['preco_oferta']:.2f}*"


# ════════════════════════════════════════════════════════════════
# BANCO DE DADOS
# ════════════════════════════════════════════════════════════════

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            telegram_username TEXT,
            nome_completo TEXT,
            email TEXT,
            telefone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
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
            paid_at TIMESTAMP
        )
    """)
    
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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            telegram_id INTEGER PRIMARY KEY,
            state TEXT DEFAULT 'idle',
            data TEXT DEFAULT '{}',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_proofs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT NOT NULL,
            file_id TEXT NOT NULL,
            file_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def get_or_create_customer(telegram_id, username=None):
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

def get_customer(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def is_customer_complete(telegram_id):
    customer = get_customer(telegram_id)
    if not customer:
        return False
    return all(customer.get(field) for field in ["nome_completo", "email", "telefone"])

def add_to_cart(telegram_id, game_id, game_name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cart (telegram_id, game_id, game_name, price) VALUES (?, ?, ?, ?)",
        (telegram_id, game_id, game_name, price)
    )
    conn.commit()
    conn.close()

def get_cart(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart WHERE telegram_id = ? ORDER BY added_at", (telegram_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_cart_total(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(price) as total FROM cart WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return row["total"] if row and row["total"] else 0.0

def remove_from_cart(telegram_id, cart_item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id = ? AND telegram_id = ?", (cart_item_id, telegram_id))
    conn.commit()
    conn.close()

def clear_cart(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()

def generate_order_code():
    return f"WA-{uuid.uuid4().hex[:8].upper()}"

def generate_download_token():
    return hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()[:32]

def create_order(telegram_id, game_id, game_name, price, payment_method):
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
    """, (order_code, customer["id"], telegram_id, game_id, game_name,
          price, payment_method, download_token, download_url, expiry.isoformat()))
    conn.commit()
    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def create_orders_from_cart(telegram_id, payment_method):
    cart_items = get_cart(telegram_id)
    orders = []
    for item in cart_items:
        order = create_order(telegram_id, item["game_id"], item["game_name"], item["price"], payment_method)
        if order:
            orders.append(order)
    clear_cart(telegram_id)
    return orders

def get_customer_orders(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE telegram_id = ? ORDER BY created_at DESC", (telegram_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_order_by_code(order_code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_orders_by_codes(codes):
    if not codes:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join(["?"] * len(codes))
    cursor.execute(f"SELECT * FROM orders WHERE order_code IN ({placeholders})", codes)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_order_status(order_code, status):
    conn = get_connection()
    cursor = conn.cursor()
    if status == "aprovado":
        cursor.execute("UPDATE orders SET status = ?, paid_at = ? WHERE order_code = ?",
                       (status, datetime.now().isoformat(), order_code))
    else:
        cursor.execute("UPDATE orders SET status = ? WHERE order_code = ?", (status, order_code))
    conn.commit()
    conn.close()

def save_payment_proof(order_codes, file_id, file_type):
    conn = get_connection()
    cursor = conn.cursor()
    for code in order_codes:
        cursor.execute("INSERT INTO payment_proofs (order_code, file_id, file_type) VALUES (?, ?, ?)",
                       (code, file_id, file_type))
    conn.commit()
    conn.close()

def get_user_state(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state, data FROM user_sessions WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row["state"], json.loads(row["data"])
    return "idle", {}

def set_user_state(telegram_id, state, data=None):
    conn = get_connection()
    cursor = conn.cursor()
    data_json = json.dumps(data or {})
    cursor.execute("""
        INSERT INTO user_sessions (telegram_id, state, data, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET state = ?, data = ?, updated_at = ?
    """, (telegram_id, state, data_json, datetime.now().isoformat(),
          state, data_json, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def clear_user_state(telegram_id):
    set_user_state(telegram_id, "idle", {})


# ════════════════════════════════════════════════════════════════
# TELEGRAM - KEYBOARDS
# ════════════════════════════════════════════════════════════════

def catalog_keyboard(page, games, prefix="catalog"):
    total_pages = max(1, math.ceil(len(games) / ITEMS_PER_PAGE))
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_games = games[start_idx:end_idx]
    
    keyboard = []
    for game in page_games:
        tag = " 🔥" if game["oferta"] else ""
        nome = game["nome"][:30] + "..." if len(game["nome"]) > 30 else game["nome"]
        keyboard.append([InlineKeyboardButton(f"🎮 {nome} - R$ {game['preco_oferta']:.2f}{tag}",
                                               callback_data=f"game_{game['id']}")])
    
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"{prefix}_{page-1}"))
    nav.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"{prefix}_{page+1}"))
    keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def game_detail_keyboard(game_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Adicionar ao Carrinho", callback_data=f"add_cart_{game_id}")],
        [InlineKeyboardButton("⚡ Comprar Agora", callback_data=f"buy_now_{game_id}")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="catalog_0"), InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]
    ])

def payment_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 PIX (Imediato)", callback_data="pay_pix")],
        [InlineKeyboardButton("💳 Cartão de Crédito", callback_data="pay_cartao")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")]
    ])

def back_to_menu_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")]])


# ════════════════════════════════════════════════════════════════
# HANDLERS
# ════════════════════════════════════════════════════════════════

async def start(update, context):
    user = update.effective_user
    get_or_create_customer(user.id, user.username)
    clear_user_state(user.id)
    
    total = len(GAMES_CATALOG)
    ofertas = len([g for g in GAMES_CATALOG if g["oferta"]])
    
    welcome = (
        f"🎮 *{STORE_NAME}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Olá, *{user.first_name}*! 👋\n\n"
        f"📦 *{total} produtos* disponíveis\n"
        f"🔥 *{ofertas} em oferta*\n\n"
        f"💚 PIX | Cartão | Boleto\n"
        f"⚡ Entrega imediata\n\n"
        f"👇 *Escolha uma opção:*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎮 Catálogo", callback_data="catalog_0")],
        [InlineKeyboardButton("🔥 Ofertas", callback_data="offers_0"),
         InlineKeyboardButton("🔍 Buscar", callback_data="search")],
        [InlineKeyboardButton("🛒 Carrinho", callback_data="cart"),
         InlineKeyboardButton("📦 Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]
    
    if update.message:
        await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(welcome, parse_mode=ParseMode.MARKDOWN,
                                                       reply_markup=InlineKeyboardMarkup(keyboard))

async def search_product_click(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    set_user_state(user_id, "AWAITING_SEARCH")
    await query.message.reply_text("🔍 Digite o nome do produto que deseja buscar:")

async def handle_user_message(update, context):
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)
    text = update.message.text
    
    if state == "AWAITING_SEARCH":
        clear_user_state(user_id)
        results = search_games(text)
        if not results:
            await update.message.reply_text(f"❌ Nenhum resultado para: {text}", reply_markup=back_to_menu_keyboard())
            return
        await update.message.reply_text(f"🔍 Resultados para '{text}':",
                                        reply_markup=catalog_keyboard(0, results, "search_res"))

async def show_game_detail(update, context, game_id):
    game = get_game_by_id(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!", show_alert=True)
        return
    
    preco = format_price(game)
    text = f"🎮 *{game['nome']}*\n\n💰 {preco}\n📝 {game['descricao']}\n🖥️ {game['plataforma']}\n\n✅ Entrega imediata"
    
    try:
        await update.callback_query.message.delete()
    except: pass
    
    imagem_url = game.get("imagem_url", "")
    if imagem_url and imagem_url.startswith("http"):
        try:
            await context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                                         photo=imagem_url, caption=text,
                                         reply_markup=game_detail_keyboard(game_id))
            return
        except:
            pass
    
    await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                   text=text, reply_markup=game_detail_keyboard(game_id))

async def show_offers(update, context, page=0):
    offers = get_offers()
    if not offers:
        await update.callback_query.edit_message_text("🔥 Nenhuma oferta no momento.", reply_markup=back_to_menu_keyboard())
        return
    await update.callback_query.edit_message_text("🔥 OFERTAS IMPERDÍVEIS!", reply_markup=catalog_keyboard(page, offers, "offers"))

async def show_cart(update, context):
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)
    if not cart:
        await update.callback_query.edit_message_text("🛒 Carrinho vazio!", reply_markup=back_to_menu_keyboard())
        return
    
    total = get_cart_total(user_id)
    text = "🛒 *CARRINHO*\n\n"
    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['game_name']} - R$ {item['price']:.2f}\n"
    text += f"\n💰 TOTAL: R$ {total:.2f}"
    
    keyboard = [[InlineKeyboardButton(f"❌ Remover", callback_data=f"remove_{item['id']}")] for item in cart]
    keyboard.append([InlineKeyboardButton("💰 Finalizar", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="main_menu")])
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN,
                                                   reply_markup=InlineKeyboardMarkup(keyboard))

async def show_orders(update, context):
    user_id = update.callback_query.from_user.id
    orders = get_customer_orders(user_id)
    if not orders:
        await update.callback_query.edit_message_text("📦 Nenhum pedido encontrado.", reply_markup=back_to_menu_keyboard())
        return
    
    text = "📦 *MEUS PEDIDOS*\n\n"
    for o in orders[:5]:
        status_emoji = {"pendente": "⏳", "aprovado": "✅", "aguardando_aprovacao": "⏳"}.get(o["status"], "📦")
        text += f"{status_emoji} `{o['order_code']}` - {o['game_name']} - R$ {o['price']:.2f}\n"
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu_keyboard())

async def show_support(update, context):
    text = (
        f"📞 *SUPORTE*\n\n"
        f"📱 WhatsApp: {STORE_WHATSAPP}\n"
        f"📧 Email: {STORE_EMAIL}\n"
        f"📸 Instagram: {STORE_INSTAGRAM}\n"
        f"⏰ {STORE_HOURS}\n\n"
        f"💚 Atendimento humanizado!"
    )
    whatsapp_clean = "".join(filter(str.isdigit, STORE_WHATSAPP))
    if not whatsapp_clean.startswith("55"):
        whatsapp_clean = "55" + whatsapp_clean
    
    keyboard = [
        [InlineKeyboardButton("📱 WhatsApp", url=f"https://wa.me/{whatsapp_clean}")],
        [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
    ]
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN,
                                                   reply_markup=InlineKeyboardMarkup(keyboard))

async def add_to_cart(update, context, game_id):
    user_id = update.callback_query.from_user.id
    game = get_game_by_id(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!")
        return
    add_to_cart(user_id, game_id, game["nome"], game["preco_oferta"])
    await update.callback_query.answer(f"✅ {game['nome']} adicionado!")

async def buy_now(update, context, game_id):
    user_id = update.callback_query.from_user.id
    game = get_game_by_id(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!", show_alert=True)
        return
    clear_cart(user_id)
    add_to_cart(user_id, game_id, game["nome"], game["preco_oferta"])
    
    if not is_customer_complete(user_id):
        await start_registration(update, context, "checkout")
        return
    await start_checkout(update, context)

async def start_registration(update, context, redirect_to=None):
    user_id = update.callback_query.from_user.id
    set_user_state(user_id, "REGISTERING", {"redirect": redirect_to})
    await update.callback_query.edit_message_text(
        "📝 *CADASTRO*\n\nPara finalizar, precisamos de alguns dados.\n\n🔒 Seus dados estão seguros!\n\n*Digite seu nome completo:*",
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_registration(update, context):
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)
    text = update.message.text
    
    if state == "REGISTERING":
        if "nome" not in data:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE customers SET nome_completo = ? WHERE telegram_id = ?", (text, user_id))
            conn.commit()
            conn.close()
            data["nome"] = text
            set_user_state(user_id, "REGISTERING", data)
            await update.message.reply_text(f"✅ Nome salvo!\n\n📧 Agora digite seu *email*:", parse_mode=ParseMode.MARKDOWN)
        elif "email" not in data:
            if "@" not in text:
                await update.message.reply_text("❌ Email inválido. Digite novamente:")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE customers SET email = ? WHERE telegram_id = ?", (text, user_id))
            conn.commit()
            conn.close()
            data["email"] = text
            set_user_state(user_id, "REGISTERING", data)
            await update.message.reply_text(f"✅ Email salvo!\n\n📱 Digite seu *telefone* (com DDD):", parse_mode=ParseMode.MARKDOWN)
        elif "telefone" not in data:
            telefone_clean = "".join(filter(str.isdigit, text))
            if len(telefone_clean) < 10:
                await update.message.reply_text("❌ Telefone inválido. Digite com DDD:")
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE customers SET telefone = ? WHERE telegram_id = ?", (telefone_clean, user_id))
            conn.commit()
            conn.close()
            clear_user_state(user_id)
            await update.message.reply_text("✅ Cadastro completo!\n\nAgora vamos finalizar sua compra!")
            
            redirect = data.get("redirect")
            if redirect == "checkout":
                # Criar um contexto falso para checkout
                class FakeCallback:
                    from_user = update.effective_user
                    def __init__(self):
                        self.message = update.message
                fake_update = type('obj', (object,), {'callback_query': FakeCallback()})()
                await start_checkout(fake_update, context)

async def start_checkout(update, context):
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)
    if not cart:
        await update.callback_query.answer("Carrinho vazio!", show_alert=True)
        return
    
    customer = get_customer(user_id)
    total = get_cart_total(user_id)
    
    text = f"💳 *FINALIZAR COMPRA*\n\n👤 {customer.get('nome_completo', '')}\n📧 {customer.get('email', '')}\n📱 {customer.get('telefone', '')}\n\n📦 Itens:\n"
    for item in cart:
        text += f"  • {item['game_name']} - R$ {item['price']:.2f}\n"
    text += f"\n💰 TOTAL: R$ {total:.2f}\n\nSelecione o pagamento:"
    
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=payment_keyboard())

async def process_payment(update, context, method):
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)
    total = get_cart_total(user_id)
    
    if not cart:
        await update.callback_query.answer("Carrinho vazio!", show_alert=True)
        return
    
    orders = create_orders_from_cart(user_id, method)
    if not orders:
        await update.callback_query.edit_message_text("❌ Erro ao processar.", reply_markup=back_to_menu_keyboard())
        return
    
    order_codes = [o["order_code"] for o in orders]
    
    if method == "pix":
        text = f"💚 *PIX*\n\n💰 Valor: R$ {total:.2f}\n\n📱 Chave: `{PIX_CHAVE}`\n👤 Nome: {PIX_NOME}\n\nApós pagar, envie o comprovante aqui no chat."
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN,
                                                       reply_markup=InlineKeyboardMarkup([
                                                           [InlineKeyboardButton("✅ Já paguei", callback_data="confirm_purchase")],
                                                           [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")]
                                                       ]))
        set_user_state(user_id, "AWAITING_PROOF", {"order_codes": order_codes})
    else:
        await update.callback_query.edit_message_text("💳 Cartão: Entre em contato pelo suporte.", reply_markup=back_to_menu_keyboard())

async def handle_payment_proof(update, context):
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)
    
    if state != "AWAITING_PROOF":
        return
    
    file_id = None
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.document:
        file_id = update.message.document.file_id
    
    if not file_id:
        await update.message.reply_text("📎 Envie uma foto do comprovante.")
        return
    
    order_codes = data.get("order_codes", [])
    if not order_codes:
        await update.message.reply_text("❌ Pedido não encontrado.")
        clear_user_state(user_id)
        return
    
    save_payment_proof(order_codes, file_id, "photo")
    for code in order_codes:
        update_order_status(code, "aguardando_aprovacao")
    
    clear_user_state(user_id)
    
    await update.message.reply_text(
        f"✅ Comprovante recebido!\n\n📋 Pedido: {', '.join(order_codes)}\n⏳ Aguardando aprovação.\n\nAssim que aprovado, você receberá o link de download!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard()
    )
    
    if ADMIN_CHAT_IDS:
        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(admin_id, f"🛒 Novo pedido para aprovação: {', '.join(order_codes)}\nUse /aprovar {order_codes[0]}")
                if update.message.photo:
                    await context.bot.send_photo(admin_id, file_id)
            except:
                pass

async def admin_approve(update, context):
    if update.effective_user.id not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ Acesso negado.")
        return
    
    args = context.args
    if not args:
        await update.message.reply_text("Use: /aprovar CODIGO")
        return
    
    order_code = args[0].upper()
    order = get_order_by_code(order_code)
    if not order:
        await update.message.reply_text(f"❌ Pedido {order_code} não encontrado.")
        return
    
    update_order_status(order_code, "aprovado")
    
    telegram_id = order["telegram_id"]
    download_url = order["download_url"]
    
    try:
        await context.bot.send_message(
            telegram_id,
            f"🎉 *PEDIDO APROVADO!*\n\n🎮 {order['game_name']}\n⬇️ {download_url}\n\n⏳ Válido por {DOWNLOAD_LINK_EXPIRY_HOURS}h",
            parse_mode=ParseMode.MARKDOWN
        )
    except:
        pass
    
    await update.message.reply_text(f"✅ Pedido {order_code} aprovado!")

async def button(update, context):
    query = update.callback_query
    try:
        await query.answer()
    except:
        pass
    
    data = query.data
    user_id = query.from_user.id
    
    if data == "main_menu":
        await start(update, context)
    elif data.startswith("catalog_"):
        page = int(data.split("_")[1])
        await query.edit_message_text("🎮 CATÁLOGO", reply_markup=catalog_keyboard(page, GAMES_CATALOG))
    elif data.startswith("offers_"):
        page = int(data.split("_")[1])
        await show_offers(update, context, page)
    elif data == "search":
        await search_product_click(update, context)
    elif data.startswith("game_"):
        game_id = int(data.split("_")[1])
        await show_game_detail(update, context, game_id)
    elif data == "cart":
        await show_cart(update, context)
    elif data.startswith("remove_"):
        item_id = int(data.split("_")[1])
        remove_from_cart(user_id, item_id)
        await show_cart(update, context)
    elif data.startswith("add_cart_"):
        game_id = int(data.split("_")[2])
        await add_to_cart(update, context, game_id)
    elif data.startswith("buy_now_"):
        game_id = int(data.split("_")[2])
        await buy_now(update, context, game_id)
    elif data == "checkout":
        await start_checkout(update, context)
    elif data.startswith("pay_"):
        method = data.split("_")[1]
        await process_payment(update, context, method)
    elif data == "confirm_purchase":
        await query.edit_message_text("📎 Envie o comprovante de pagamento (foto ou documento).")
    elif data == "my_orders":
        await show_orders(update, context)
    elif data == "support":
        await show_support(update, context)
    elif data == "noop":
        pass


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

async def main_async():
    print("=" * 60)
    print("🎮 WareArcadeBot - Versão com requests")
    print("=" * 60)
    
    init_db()
    print(f"✅ Banco: {DATABASE_PATH}")
    print(f"📦 Catálogo: {len(GAMES_CATALOG)} produtos")
    print("🚀 Conectando ao Telegram...")
    
    # ── Usa o adapter com requests ──
    adapter = RequestsAdapter(timeout=120)
    
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .request(adapter)
        .connect_timeout(120)
        .read_timeout(120)
        .write_timeout(120)
        .pool_timeout(120)
        .build()
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("aprovar", admin_approve))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_payment_proof))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    print("✅ Bot iniciado! Aguardando mensagens...")
    print("=" * 60)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Bot finalizado.")

def main():
    tentativas = 0
    while tentativas < 10:
        try:
            asyncio.run(main_async())
            break
        except KeyboardInterrupt:
            print("\n🛑 Parado pelo usuário.")
            break
        except Exception as e:
            tentativas += 1
            print(f"⚠️ Tentativa {tentativas}/10 falhou: {e}")
            if tentativas < 10:
                print(f"⏳ Tentando novamente em 10s...")
                time.sleep(10)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token não configurado!")
        print("   Crie um arquivo .env com: TELEGRAM_BOT_TOKEN=seu_token")
    else:
        main()