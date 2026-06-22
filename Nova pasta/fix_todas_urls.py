"""
CORRIGE TODAS AS URLs DO BOT - DEFINITIVO
Remove botoes com URLs problematicas
"""
import shutil
import re

print("=" * 60)
print("  CORRIGINDO TODAS AS URLs DO BOT")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_urls")
print("[OK] Backup criado")

if "config.py" in __import__("os").listdir("."):
    shutil.copy("config.py", "config.py.backup_urls")
    print("[OK] Backup config.py criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Verifica config.py
try:
    with open("config.py", "r", encoding="utf-8") as f:
        config = f.read()
except:
    config = ""

# Verifica STORE_WEBSITE
if "STORE_WEBSITE" in config:
    # Procura valor atual
    match = re.search(r'STORE_WEBSITE\s*=\s*["\']([^"\']*)["\']', config)
    if match:
        site_atual = match.group(1)
        print(f"[INFO] STORE_WEBSITE atual: {site_atual}")
        
        # Se nao comecar com http, corrige
        if site_atual and not site_atual.startswith("http"):
            novo_site = f"https://{site_atual}"
            config = config.replace(
                f'STORE_WEBSITE = "{site_atual}"',
                f'STORE_WEBSITE = "{novo_site}"'
            )
            config = config.replace(
                f"STORE_WEBSITE = '{site_atual}'",
                f"STORE_WEBSITE = '{novo_site}'"
            )
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(config)
            print(f"[OK] STORE_WEBSITE corrigido para: {novo_site}")

# ====================================
# CORRIGE FUNCAO show_support COMPLETA
# ====================================
nova_support = '''async def show_support(update, context):
    """Suporte - URLs blindadas."""
    try:
        # Limpa WhatsApp (so digitos)
        whatsapp_clean = "".join(filter(str.isdigit, str(STORE_WHATSAPP)))
        if whatsapp_clean and not whatsapp_clean.startswith("55"):
            whatsapp_clean = "55" + whatsapp_clean
        
        # Limpa Instagram
        ig_clean = str(STORE_INSTAGRAM).replace("@", "").replace(" ", "").strip()
        
        text = (
            f"📞 *SUPORTE AO CLIENTE*\\n\\n"
            f"🏪 *{STORE_NAME}*\\n\\n"
            f"📧 Email: {STORE_EMAIL}\\n"
            f"📱 WhatsApp: {STORE_WHATSAPP}\\n"
            f"📸 Instagram: {STORE_INSTAGRAM}\\n"
            f"⏰ {STORE_HOURS}\\n\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n"
            "💬 Precisa de ajuda?\\n"
            "Envie uma mensagem que respondemos rapido!"
        )

        keyboard = []
        
        # WhatsApp - so se for valido
        if whatsapp_clean and len(whatsapp_clean) >= 12:
            keyboard.append([InlineKeyboardButton(
                "📱 Chamar no WhatsApp", 
                url=f"https://wa.me/{whatsapp_clean}"
            )])
        
        # Email - so se for valido
        if STORE_EMAIL and "@" in str(STORE_EMAIL):
            keyboard.append([InlineKeyboardButton(
                "📧 Enviar Email", 
                url=f"mailto:{STORE_EMAIL}"
            )])
        
        # Instagram - so se for valido
        if ig_clean and len(ig_clean) >= 3:
            keyboard.append([InlineKeyboardButton(
                "📸 Instagram", 
                url=f"https://instagram.com/{ig_clean}"
            )])
        
        keyboard.append([InlineKeyboardButton("❓ FAQ", callback_data="faq")])
        keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])

        kb = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
            except Exception:
                await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        else:
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    except Exception as e:
        logger.error(f"Erro show_support: {e}")
        try:
            text_simples = f"Suporte:\\n{STORE_EMAIL}\\nWhatsApp: {STORE_WHATSAPP}"
            kb_simples = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]])
            if update.callback_query:
                await update.callback_query.message.reply_text(text_simples, reply_markup=kb_simples)
            else:
                await update.message.reply_text(text_simples, reply_markup=kb_simples)
        except Exception:
            pass

'''

padrao = re.compile(
    r'async def show_support\(update, context\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)
if padrao.search(c):
    c = padrao.sub(nova_support, c)
    print("[OK] show_support BLINDADO")

# ====================================
# REMOVE todos url= com possiveis problemas
# Procura urls que sao variaveis (sem http://)
# ====================================
print("\n[INFO] Procurando outros botoes com URL...")

# Padroes problematicos a remover
padroes_problema = [
    # url= sem https:// ou http://
    (r'InlineKeyboardButton\([^)]*url=f?["\']\{[^}]+\}[^"\']*["\'][^)]*\)', "Botao com URL variavel"),
    # url= com texto que nao parece URL
    (r'InlineKeyboardButton\([^)]*url=["\'](?!https?://|mailto:)[^"\']*["\'][^)]*\)', "Botao com URL invalida"),
]

# So mostra avisos, nao remove (pode quebrar)
total_avisos = 0
for padrao_url, desc in padroes_problema:
    matches = re.findall(padrao_url, c)
    if matches:
        for m in matches[:3]:  # mostra so os 3 primeiros
            print(f"[AVISO] {desc}: {m[:80]}...")
        total_avisos += len(matches)

print(f"\n[INFO] Total de possiveis problemas: {total_avisos}")

# ====================================
# CORRIGE institutional_detail (se tiver URL)
# ====================================
# Procura por url= dentro de institutional_detail
match_inst = re.search(
    r'async def institutional_detail.*?(?=\nasync def |\ndef )',
    c, re.DOTALL
)
if match_inst:
    bloco = match_inst.group(0)
    # Remove qualquer url= problematico
    bloco_novo = re.sub(
        r',?\s*InlineKeyboardButton\([^)]*url=f?["\'][^"\']*["\'][^)]*\)',
        "",
        bloco
    )
    if bloco != bloco_novo:
        c = c.replace(bloco, bloco_novo)
        print("[OK] URLs problematicas removidas do Institucional")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("\n[OK] Sintaxe valida!")
    print("\n" + "=" * 60)
    print("  CORRECAO COMPLETA APLICADA!")
    print("=" * 60)
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"\n[ERRO] {e}")
    shutil.copy("bot.py.backup_urls", "bot.py")
    print("[OK] Backup restaurado.")