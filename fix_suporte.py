"""
CORRIGE ERRO BOTAO SUPORTE - URL INVALIDA WhatsApp
"""
import shutil
import re

print("=" * 60)
print("  CORRIGINDO BOTAO DE SUPORTE (WhatsApp URL)")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup_suporte")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Funcao show_support BLINDADA
nova_support = '''async def show_support(update, context):
    """Exibe informacoes de suporte - URL CORRIGIDA."""
    try:
        # Limpa o numero do WhatsApp (so digitos!)
        whatsapp_clean = "".join(filter(str.isdigit, STORE_WHATSAPP))
        # Garante que comeca com 55 (Brasil)
        if not whatsapp_clean.startswith("55"):
            whatsapp_clean = "55" + whatsapp_clean
        
        # Limpa Instagram
        instagram_clean = STORE_INSTAGRAM.replace("@", "").replace(" ", "")
        
        text = (
            f"📞 *SUPORTE AO CLIENTE*\\n\\n"
            f"🏪 *{STORE_NAME}*\\n\\n"
            f"📧 Email: {STORE_EMAIL}\\n"
            f"📱 WhatsApp: {STORE_WHATSAPP}\\n"
            f"📸 Instagram: {STORE_INSTAGRAM}\\n"
            f"⏰ Horario: {STORE_HOURS}\\n\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "💬 *Precisa de ajuda?*\\n"
            "Envie uma mensagem descrevendo seu problema "
            "que nossa equipe respondera o mais rapido possivel!"
        )

        # URL do WhatsApp (formato correto: wa.me/55XXXXXXXXXXX)
        wa_url = f"https://wa.me/{whatsapp_clean}"
        ig_url = f"https://instagram.com/{instagram_clean}"
        site_url = STORE_WEBSITE if STORE_WEBSITE.startswith("http") else f"https://{STORE_WEBSITE}"

        keyboard = []
        
        # So adiciona se a URL for valida
        if whatsapp_clean and len(whatsapp_clean) >= 10:
            keyboard.append([InlineKeyboardButton("📱 WhatsApp", url=wa_url)])
        
        if STORE_EMAIL and "@" in STORE_EMAIL:
            keyboard.append([InlineKeyboardButton("📧 Email", url=f"mailto:{STORE_EMAIL}")])
        
        if site_url and site_url.startswith("http"):
            keyboard.append([InlineKeyboardButton("🌐 Site", url=site_url)])
        
        if instagram_clean:
            keyboard.append([InlineKeyboardButton("📸 Instagram", url=ig_url)])
        
        keyboard.append([InlineKeyboardButton("❓ FAQ", callback_data="faq")])
        keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="main_menu")])

        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception:
                await update.callback_query.message.reply_text(
                    text, parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception as e:
        logger.error(f"Erro em show_support: {e}", exc_info=True)
        # Fallback simples
        try:
            simples = (
                f"📞 SUPORTE\\n\\n"
                f"Email: {STORE_EMAIL}\\n"
                f"WhatsApp: {STORE_WHATSAPP}\\n"
                f"Instagram: {STORE_INSTAGRAM}"
            )
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]])
            
            if update.callback_query:
                await update.callback_query.message.reply_text(simples, reply_markup=kb)
            else:
                await update.message.reply_text(simples, reply_markup=kb)
        except Exception:
            pass

'''

# Substitui show_support
padrao = re.compile(
    r'async def show_support\(update, context\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)

if padrao.search(c):
    c = padrao.sub(nova_support, c)
    print("[OK] show_support BLINDADO!")
else:
    print("[AVISO] show_support nao encontrada!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida sintaxe
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\n" + "=" * 60)
    print("  CORRECAO APLICADA!")
    print("=" * 60)
    print("\n  O que foi corrigido:")
    print("  - URL do WhatsApp agora e gerada corretamente")
    print("  - Apenas digitos (sem (), ., -)")
    print("  - Adiciona 55 (Brasil) se nao tiver")
    print("  - URLs invalidas sao puladas")
    print("  - Fallback automatico em caso de erro")
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_suporte", "bot.py")
    print("[OK] Backup restaurado.")