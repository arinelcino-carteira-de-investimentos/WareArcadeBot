"""
CORRIGE config.py + bot.py
- Limpa variaveis WhatsApp, Instagram, Site
- Corrige funcao show_support
"""
import shutil
import re

print("=" * 60)
print("  CORRIGINDO CONFIG.PY E BOT.PY")
print("=" * 60)

# Backups
shutil.copy("config.py", "config.py.backup_url")
shutil.copy("bot.py", "bot.py.backup_url")
print("[OK] Backups criados")

# ════════════════════════════════════════
# 1. CORRIGE config.py
# ════════════════════════════════════════
print("\n[1/2] Corrigindo config.py...")

with open("config.py", "r", encoding="utf-8") as f:
    config = f.read()

# Corrige STORE_WHATSAPP
# De: '+55 11 94046-2611'  Para: '+5511940462611'
config = re.sub(
    r'STORE_WHATSAPP\s*=\s*["\'][^"\']*["\']',
    'STORE_WHATSAPP = "+5511940462611"',
    config
)
print("[OK] STORE_WHATSAPP corrigido para: +5511940462611")

# Corrige STORE_WEBSITE
# Substitui nexusdigitalshop por warearcadebot
config = config.replace("nexusdigitalshop.com.br", "warearcadebot.com.br")
print("[OK] STORE_WEBSITE atualizado")

# Salva
with open("config.py", "w", encoding="utf-8") as f:
    f.write(config)
print("[OK] config.py salvo")

# ════════════════════════════════════════
# 2. CORRIGE bot.py - show_support
# ════════════════════════════════════════
print("\n[2/2] Corrigindo show_support no bot.py...")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Funcao show_support DEFINITIVA - com sanitização
nova_support = '''async def show_support(update, context):
    """Suporte - URL Sanitizada."""
    try:
        # Limpa WhatsApp (so digitos)
        whatsapp_raw = str(STORE_WHATSAPP)
        whatsapp_clean = "".join(c for c in whatsapp_raw if c.isdigit())
        
        # Garante 55 no inicio (Brasil)
        if whatsapp_clean and not whatsapp_clean.startswith("55"):
            whatsapp_clean = "55" + whatsapp_clean
        
        # Limpa Instagram (sem @)
        ig_clean = str(STORE_INSTAGRAM).replace("@", "").replace(" ", "").strip()
        
        # Mostra com formatacao bonita
        whatsapp_show = f"+55 (11) 9.4046-2611"
        
        text = (
            f"📞 *SUPORTE AO CLIENTE*\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            f"🏪 *{STORE_NAME}*\\n\\n"
            f"💬 *Fale conosco:*\\n\\n"
            f"📱 *WhatsApp:* {whatsapp_show}\\n"
            f"📧 *Email:* {STORE_EMAIL}\\n"
            f"📸 *Instagram:* @{ig_clean}\\n"
            f"⏰ *Horario:* {STORE_HOURS}\\n\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            f"💚 *Atendimento humanizado!*\\n"
            f"Respondemos em ate 30 minutos."
        )

        keyboard = []
        
        # WhatsApp - URL valida garantida
        if whatsapp_clean and len(whatsapp_clean) >= 12:
            wa_url = f"https://wa.me/{whatsapp_clean}"
            keyboard.append([InlineKeyboardButton("📱 Chamar no WhatsApp", url=wa_url)])
        
        # Email
        if STORE_EMAIL and "@" in str(STORE_EMAIL):
            keyboard.append([InlineKeyboardButton("📧 Enviar Email", url=f"mailto:{STORE_EMAIL}")])
        
        # Instagram
        if ig_clean and len(ig_clean) >= 3:
            keyboard.append([InlineKeyboardButton("📸 Seguir Instagram", url=f"https://instagram.com/{ig_clean}")])
        
        keyboard.append([InlineKeyboardButton("❓ Ver FAQ", callback_data="faq")])
        keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])

        kb = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
                )
            except Exception as e:
                logger.warning(f"Edit falhou: {e}")
                await update.callback_query.message.reply_text(
                    text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
                )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )

    except Exception as e:
        logger.error(f"Erro show_support: {e}", exc_info=True)
        try:
            simples = f"Suporte:\\nWhatsApp: {STORE_WHATSAPP}\\nEmail: {STORE_EMAIL}"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]])
            if update.callback_query:
                await update.callback_query.message.reply_text(simples, reply_markup=kb)
            else:
                await update.message.reply_text(simples, reply_markup=kb)
        except Exception:
            pass

'''

padrao = re.compile(
    r'async def show_support\(update, context\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)
if padrao.search(c):
    c = padrao.sub(nova_support, c)
    print("[OK] show_support CORRIGIDO!")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    
    with open("config.py", "r", encoding="utf-8") as f:
        compile(f.read(), "config.py", "exec")
    
    print("\n[OK] Sintaxe valida nos 2 arquivos!")
    
    # Verifica novos valores
    import importlib
    import config
    importlib.reload(config)
    
    print("\n" + "=" * 60)
    print("  CORRECAO APLICADA COM SUCESSO!")
    print("=" * 60)
    print(f"\n  Novos valores:")
    print(f"  WHATSAPP:  {config.STORE_WHATSAPP}")
    print(f"  WEBSITE:   {config.STORE_WEBSITE}")
    print(f"  INSTAGRAM: {config.STORE_INSTAGRAM}")
    print(f"  EMAIL:     {config.STORE_EMAIL}")
    print("\n  URL WhatsApp que sera gerada:")
    wpp_clean = "".join(c for c in config.STORE_WHATSAPP if c.isdigit())
    print(f"  https://wa.me/{wpp_clean}")
    print("\n  Rode: py bot.py")
    print("=" * 60)
    
except SyntaxError as e:
    print(f"\n[ERRO] {e}")
    shutil.copy("config.py.backup_url", "config.py")
    shutil.copy("bot.py.backup_url", "bot.py")
    print("[OK] Backups restaurados.")