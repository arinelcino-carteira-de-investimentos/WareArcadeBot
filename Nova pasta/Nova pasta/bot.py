"""
🎮 WareArcadeBot - Versão Railway
"""

import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# PEGA O TOKEN DIRETO DA VARIÁVEL DE AMBIENTE
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 60)
print("🎮 WareArcadeBot - Iniciando...")
print("=" * 60)

# Verifica o token
if not TELEGRAM_BOT_TOKEN:
    print("❌ ERRO: TELEGRAM_BOT_TOKEN não configurado!")
    print("Configure a variável de ambiente TELEGRAM_BOT_TOKEN")
    exit(1)

print(f"✅ Token carregado: {TELEGRAM_BOT_TOKEN[:10]}...")

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        [InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]
    
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for game in GAMES:
        keyboard.append([InlineKeyboardButton(f"🎮 {game['nome']} - R$ {game['preco']:.2f}", callback_data=f"game_{game['id']}")])
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="menu")])
    
    await update.callback_query.edit_message_text(
        "🎮 *CATÁLOGO*\n\nSelecione um produto:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def game_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, game_id: int):
    game = get_game(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!")
        return
    
    text = f"🎮 *{game['nome']}*\n\n💰 R$ {game['preco']:.2f}\n📝 {game['desc']}\n\n✅ Entrega imediata"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Voltar", callback_data="catalog")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ]
    
    await update.callback_query.message.delete()
    await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 *SUPORTE*\n\n"
        "📱 WhatsApp: +5511940462611\n"
        "📧 Email: warearcadebot@gmail.com\n\n"
        "💚 Atendimento humanizado!"
    )
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="menu")]]))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "menu":
        await start(update, context)
    elif data == "catalog":
        await catalog(update, context)
    elif data == "support":
        await show_support(update, context)
    elif data.startswith("game_"):
        game_id = int(data.split("_")[1])
        await game_detail(update, context, game_id)

# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════

async def main_async():
    print("🚀 Conectando ao Telegram...")
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    print("✅ Bot rodando! Aguardando mensagens...")
    print("=" * 60)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    await asyncio.Event().wait()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("🛑 Bot parado.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()