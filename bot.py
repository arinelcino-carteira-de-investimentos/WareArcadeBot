"""
🎮 WareArcadeBot - Versão Railway
"""

import os
import logging
import sqlite3
import json
import uuid
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_PATH = "warearcade.db"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

print("🚀 Iniciando WareArcadeBot...")
print(f"✅ Token: {TELEGRAM_BOT_TOKEN[:10]}...")

# ════════════════════════════════════════
# BANCO DE DADOS
# ════════════════════════════════════════

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE NOT NULL,
            telegram_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'pendente',
            download_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            game_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado")

# ════════════════════════════════════════
# CATÁLOGO
# ════════════════════════════════════════

GAMES = [
    {"id": 1, "nome": "Red Dead Redemption 2", "preco": 38.90, "desc": "Ação e aventura no Velho Oeste."},
    {"id": 2, "nome": "Elden Ring", "preco": 32.90, "desc": "RPG de ação em mundo aberto."},
    {"id": 3, "nome": "God of War Ragnarok", "preco": 32.90, "desc": "Continuação épica de Kratos."},
    {"id": 4, "nome": "Windows 11 Pro", "preco": 89.90, "desc": "Licença ORIGINAL Windows 11 Pro vitalícia."},
    {"id": 5, "nome": "Office 2021 Pro Plus", "preco": 79.90, "desc": "Office 2021 Pro Plus VITALÍCIO."},
    {"id": 999, "nome": "🧪 TESTE R$ 1,50", "preco": 1.50, "desc": "Produto de teste - R$ 1,50"},
]

def get_game(game_id):
    for g in GAMES:
        if g["id"] == game_id:
            return g
    return None

# ════════════════════════════════════════
# HANDLERS
# ════════════════════════════════════════

async def start(update, context):
    user = update.effective_user
    welcome = (
        f"🎮 *WareArcadeBot*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Olá, *{user.first_name}*! 👋\n\n"
        f"📦 {len(GAMES)} produtos disponíveis\n"
        f"💚 PIX | Cartão\n"
        f"⚡ Entrega imediata\n\n"
        f"👇 Escolha uma opção:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎮 Catálogo", callback_data="catalog")],
        [InlineKeyboardButton("🛒 Carrinho", callback_data="cart")],
        [InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]
    
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

async def catalog(update, context):
    keyboard = []
    for game in GAMES:
        keyboard.append([InlineKeyboardButton(f"🎮 {game['nome']} - R$ {game['preco']:.2f}", callback_data=f"game_{game['id']}")])
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="menu")])
    
    await update.callback_query.edit_message_text(
        "🎮 *CATÁLOGO*\n\nSelecione um produto:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def game_detail(update, context, game_id):
    game = get_game(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!")
        return
    
    text = f"🎮 *{game['nome']}*\n\n💰 R$ {game['preco']:.2f}\n📝 {game['desc']}\n\n✅ Entrega imediata"
    
    keyboard = [
        [InlineKeyboardButton("🛒 Adicionar", callback_data=f"add_{game_id}")],
        [InlineKeyboardButton("⚡ Comprar", callback_data=f"buy_{game_id}")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="catalog")],
    ]
    
    await update.callback_query.message.delete()
    await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

async def add_to_cart(update, context, game_id):
    game = get_game(game_id)
    if not game:
        await update.callback_query.answer("Erro!")
        return
    await update.callback_query.answer(f"✅ {game['nome']} adicionado!")

async def buy_now(update, context, game_id):
    game = get_game(game_id)
    if not game:
        await update.callback_query.answer("Erro!")
        return
    
    order_code = f"WA-{uuid.uuid4().hex[:8].upper()}"
    download_url = f"https://warearcadebot.com.br/download/{uuid.uuid4().hex}"
    
    await update.callback_query.edit_message_text(
        f"✅ *COMPRA REALIZADA!*\n\n"
        f"📋 Pedido: `{order_code}`\n"
        f"🎮 {game['nome']}\n"
        f"💰 R$ {game['preco']:.2f}\n\n"
        f"⬇️ Link: {download_url}\n\n"
        f"💚 Aproveite!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="menu")]])
    )

async def show_cart(update, context):
    await update.callback_query.edit_message_text(
        "🛒 Carrinho vazio!\n\nAdicione produtos do catálogo.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Catálogo", callback_data="catalog")]])
    )

async def show_support(update, context):
    text = (
        "📞 *SUPORTE*\n\n"
        "📱 WhatsApp: +5511940462611\n"
        "📧 Email: warearcadebot@gmail.com\n\n"
        "💚 Atendimento humanizado!"
    )
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="menu")]]))

async def button(update, context):
    query = update.callback_query
    data = query.data
    
    if data == "menu":
        await start(update, context)
    elif data == "catalog":
        await catalog(update, context)
    elif data == "cart":
        await show_cart(update, context)
    elif data == "support":
        await show_support(update, context)
    elif data.startswith("game_"):
        game_id = int(data.split("_")[1])
        await game_detail(update, context, game_id)
    elif data.startswith("add_"):
        game_id = int(data.split("_")[1])
        await add_to_cart(update, context, game_id)
    elif data.startswith("buy_"):
        game_id = int(data.split("_")[1])
        await buy_now(update, context, game_id)

# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════

async def main_async():
    print("🎮 WareArcadeBot iniciando...")
    init_db()
    print(f"📦 Catálogo: {len(GAMES)} produtos")
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    print("✅ Bot rodando!")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    await asyncio.Event().wait()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("🛑 Bot parado.")

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TOKEN não configurado!")
    else:
        main()