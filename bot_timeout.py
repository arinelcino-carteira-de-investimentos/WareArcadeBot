"""
WareArcadeBot - Versão com Timeouts Aumentados
"""
import os
import logging
import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.request import HTTPXRequest
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════
# BOT PRINCIPAL COM TIMEOUTS ALTOS
# ════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start básico."""
    user = update.effective_user
    welcome = (
        f"🎮 *WareArcadeBot*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Olá, *{user.first_name}*! 👋\n\n"
        f"✅ Bot conectado com sucesso!\n\n"
        f"🚀 Teste básico funcionando!\n\n"
        f"📌 Comandos disponíveis:\n"
        f"/start - Iniciar\n"
        f"/teste - Teste de conexão\n"
        f"/menu - Menu principal\n\n"
        f"💚 Conexão estável!"
    )
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Teste de conexão."""
    import time
    inicio = time.time()
    await update.message.reply_text("🔄 Testando conexão...")
    fim = time.time()
    await update.message.reply_text(f"✅ Conexão OK! Tempo: {fim - inicio:.2f}s")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu simples."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("🎮 Catálogo", callback_data="catalogo")],
        [InlineKeyboardButton("🛒 Carrinho", callback_data="carrinho")],
        [InlineKeyboardButton("📞 Suporte", callback_data="suporte")],
    ]
    await update.message.reply_text(
        "📋 *MENU PRINCIPAL*\n\nEscolha uma opção:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback dos botões."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "catalogo":
        await query.edit_message_text("🎮 Catálogo em breve...")
    elif query.data == "carrinho":
        await query.edit_message_text("🛒 Carrinho vazio!")
    elif query.data == "suporte":
        await query.edit_message_text(
            "📞 Suporte\n\n"
            "WhatsApp: +5511940462611\n"
            "Email: warearcadebot@gmail.com"
        )

async def main_async():
    """Inicializa o bot com timeouts ALTOS."""
    print("=" * 60)
    print("🎮 WareArcadeBot - Iniciando com Timeouts Altos...")
    print("=" * 60)
    print(f"✅ Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    print("⏳ Conectando ao Telegram...")

    # ── Request com timeouts ALTOS ──
    request = HTTPXRequest(
        connect_timeout=120.0,
        read_timeout=120.0,
        write_timeout=120.0,
        pool_timeout=120.0,
        http_version="1.1"
    )

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .request(request)
        .connect_timeout(120)
        .read_timeout(120)
        .write_timeout(120)
        .pool_timeout(120)
        .get_updates_connect_timeout(120)
        .get_updates_read_timeout(120)
        .build()
    )

    # ── Handlers ──
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teste", teste))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("🚀 Bot iniciado! Aguardando mensagens...")
    print("=" * 60)

    await app.initialize()
    await app.start()
    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Bot finalizado.")

def main():
    """Main com reconexão."""
    tentativas = 0
    max_tentativas = 20
    
    while tentativas < max_tentativas:
        try:
            asyncio.run(main_async())
            break
        except KeyboardInterrupt:
            print("\n🛑 Bot parado pelo usuário.")
            break
        except Exception as e:
            tentativas += 1
            print(f"\n⚠️ Tentativa {tentativas}/{max_tentativas} falhou: {e}")
            print(f"⏳ Aguardando {tentativas * 10}s...")
            time.sleep(tentativas * 10)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: Token não configurado!")
        print("   Crie um arquivo .env com: TELEGRAM_BOT_TOKEN=seu_token")
    else:
        main()