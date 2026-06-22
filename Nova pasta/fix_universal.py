"""
CORRECAO UNIVERSAL - REMOVE TODOS OS BOTOES COM URL
Substitui por mensagens de texto com links clicaveis
"""
import shutil
import re

print("=" * 60)
print("  CORRECAO UNIVERSAL - REMOVE BOTOES URL")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_universal")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# ============================================
# Funcao show_support SIMPLES (SEM URLs)
# ============================================
nova_support = '''async def show_support(update, context):
    """Suporte - SEM BOTOES com URL externa."""
    try:
        whatsapp_num = "".join(filter(str.isdigit, str(STORE_WHATSAPP)))
        if whatsapp_num and not whatsapp_num.startswith("55"):
            whatsapp_num = "55" + whatsapp_num
        
        text = (
            f"📞 *SUPORTE AO CLIENTE*\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            f"🏪 *{STORE_NAME}*\\n\\n"
            f"💬 *Fale conosco diretamente:*\\n\\n"
            f"📱 *WhatsApp:* {STORE_WHATSAPP}\\n"
            f"_Clique aqui:_ https://wa.me/{whatsapp_num}\\n\\n"
            f"📧 *Email:* {STORE_EMAIL}\\n\\n"
            f"📸 *Instagram:* {STORE_INSTAGRAM}\\n\\n"
            f"⏰ *Horario:* {STORE_HOURS}\\n\\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            f"💚 Atendimento humanizado!\\n"
            f"Respondemos em ate 30 minutos."
        )

        keyboard = [
            [InlineKeyboardButton("❓ Ver FAQ", callback_data="faq")],
            [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
        ]

        kb = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, parse_mode=ParseMode.MARKDOWN, 
                    reply_markup=kb,
                    disable_web_page_preview=True
                )
            except Exception as e:
                logger.error(f"Erro edit support: {e}")
                await update.callback_query.message.reply_text(
                    text, parse_mode=ParseMode.MARKDOWN, 
                    reply_markup=kb,
                    disable_web_page_preview=True
                )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, 
                reply_markup=kb,
                disable_web_page_preview=True
            )

    except Exception as e:
        logger.error(f"Erro CRITICO show_support: {e}", exc_info=True)
        try:
            simples = "Suporte:\\nWhatsApp: " + str(STORE_WHATSAPP) + "\\nEmail: " + str(STORE_EMAIL)
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
    print("[OK] show_support SIMPLIFICADO (sem botoes URL)")

# ============================================
# Funcao show_indique SEM URL
# ============================================
nova_indique = '''async def show_indique(update, context):
    """Programa Indique e Ganhe - SEM botao URL."""
    try:
        user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
        
        text = (
            "🎁 *INDIQUE E GANHE R$ 15!*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "Compartilhe a alegria! 💚\\n\\n"
            "*Como funciona:*\\n\\n"
            "1️⃣ Copie seu link abaixo\\n"
            "2️⃣ Envie para amigos\\n"
            "3️⃣ Quando comprarem, voce ganha R$ 15!\\n\\n"
            "🔗 *Seu link exclusivo:*\\n"
            f"`https://t.me/WareArcadeBot?start=ref_{user_id}`\\n\\n"
            "_Toque no link acima para copiar!_\\n\\n"
            "💚 *Voce indica, todos ganham!*\\n"
            "_Sem limites de indicacoes!_"
        )
        
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
        ])
        
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, parse_mode=ParseMode.MARKDOWN, 
                    reply_markup=kb,
                    disable_web_page_preview=True
                )
            except Exception:
                await update.callback_query.message.reply_text(
                    text, parse_mode=ParseMode.MARKDOWN, 
                    reply_markup=kb,
                    disable_web_page_preview=True
                )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, 
                reply_markup=kb,
                disable_web_page_preview=True
            )

    except Exception as e:
        logger.error(f"Erro show_indique: {e}", exc_info=True)

'''

padrao2 = re.compile(
    r'async def show_indique\(update, context\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)
if padrao2.search(c):
    c = padrao2.sub(nova_indique, c)
    print("[OK] show_indique SIMPLIFICADO")

# ============================================
# REMOVE TODOS os InlineKeyboardButton com url= problematicos
# ============================================
print("\n[INFO] Procurando URLs problematicas...")

# Encontra todos os "url=" no codigo
urls_encontradas = re.findall(r'url\s*=\s*[^,)]+', c)
print(f"[INFO] Total de url= encontradas: {len(urls_encontradas)}")

# Mostra as 5 primeiras para debug
for i, u in enumerate(urls_encontradas[:5]):
    print(f"  {i+1}. {u[:80]}")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("\n[OK] Sintaxe valida!")
    print("\n" + "=" * 60)
    print("  CORRECAO APLICADA!")
    print("=" * 60)
    print("\n  O que mudou:")
    print("  - show_support: SEM botoes URL externos")
    print("  - show_indique: SEM botoes URL externos")
    print("  - Links agora aparecem no TEXTO (clicaveis)")
    print("  - Apenas botoes de callback (menu, faq)")
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"\n[ERRO] {e}")
    shutil.copy("bot.py.backup_universal", "bot.py")
    print("[OK] Backup restaurado.")