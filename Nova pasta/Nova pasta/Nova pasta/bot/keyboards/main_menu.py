
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Jogos", callback_data="games")],
        [InlineKeyboardButton("⚙️ Configurações", callback_data="settings")],
        [InlineKeyboardButton("❓ Ajuda", callback_data="help")],
    ])
