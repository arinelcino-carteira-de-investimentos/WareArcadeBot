
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import build_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo ao WareArcadeBot!",
        reply_markup=build_main_menu()
    )
