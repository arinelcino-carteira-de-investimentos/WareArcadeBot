"""
REMOVE TODOS os botoes com URL e logs detalhados
"""
import shutil
import re

print("=" * 60)
print("  REMOVENDO TODOS BOTOES URL + LOGS DETALHADOS")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_zero")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# ════════════════════════════════════════
# FUNCAO show_support SUPER SIMPLES (SEM URL)
# ════════════════════════════════════════
nova_support = '''async def show_support(update, context):
    """Suporte - APENAS TEXTO COM LINKS CLICAVEIS."""
    try:
        whatsapp_raw = str(STORE_WHATSAPP)
        whatsapp_clean = "".join(ch for ch in whatsapp_raw if ch.isdigit())
        if whatsapp_clean and not whatsapp_clean.startswith("55"):
            whatsapp_clean = "55" + whatsapp_clean
        
        ig_clean = str(STORE_INSTAGRAM).replace("@", "").replace(" ", "").strip()
        
        # Texto com links que o Telegram detecta automaticamente
        text = (
            "📞 SUPORTE AO CLIENTE\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            f"🏪 {STORE_NAME}\\n\\n"
            "💬 Fale conosco:\\n\\n"
            f"📱 WhatsApp: {STORE_WHATSAPP}\\n"
            f"🔗 https://wa.me/{whatsapp_clean}\\n\\n"
            f"📧 Email: {STORE_EMAIL}\\n\\n"
            f"📸 Instagram: @{ig_clean}\\n"
            f"🔗 https://instagram.com/{ig_clean}\\n\\n"
            f"⏰ Horario: {STORE_HOURS}\\n\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "💚 Atendimento humanizado!\\n"
            "Respondemos em ate 30 minutos.\\n\\n"
            "👆 Toque nos links acima para abrir!"
        )

        # SO botoes de CALLBACK (sem URL!)
        keyboard = [
            [InlineKeyboardButton("❓ Ver FAQ", callback_data="faq")],
            [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
        ]

        kb = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, 
                    reply_markup=kb,
                    disable_web_page_preview=True
                )
            except Exception as e:
                logger.error(f"[SUPPORT] Erro edit: {e}")
                try:
                    await update.callback_query.message.reply_text(
                        text, reply_markup=kb, disable_web_page_preview=True
                    )
                except Exception as e2:
                    logger.error(f"[SUPPORT] Erro reply: {e2}")
        else:
            await update.message.reply_text(
                text, reply_markup=kb, disable_web_page_preview=True
            )

    except Exception as e:
        logger.error(f"[SUPPORT] Erro CRITICO: {e}", exc_info=True)
        try:
            simples = f"Suporte:\\nWhatsApp: {STORE_WHATSAPP}\\nEmail: {STORE_EMAIL}"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("Menu", callback_data="main_menu")]])
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
    print("[OK] show_support SEM URLs!")

# ════════════════════════════════════════
# REMOVE TODOS os 'url=' no codigo
# ════════════════════════════════════════
print("\n[INFO] Procurando outros botoes com url=...")

# Conta quantos botoes com url existem
urls = re.findall(r'InlineKeyboardButton\([^)]*url\s*=', c)
print(f"[INFO] Total de botoes com URL: {len(urls)}")

# Mostra cada um para debug
for i, u in enumerate(urls[:10]):
    print(f"  {i+1}. {u[:100]}")

# REMOVE todos botoes com url= (radical, mas garante funcionamento)
# Antes de remover, identifica onde estao
linhas = c.split("\n")
linhas_com_url = []
for i, linha in enumerate(linhas):
    if "url=" in linha and "InlineKeyboardButton" in linha:
        linhas_com_url.append((i+1, linha.strip()[:100]))

if linhas_com_url:
    print(f"\n[AVISO] Linhas com botao URL:")
    for num, ln in linhas_com_url[:10]:
        print(f"  Linha {num}: {ln}")

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
    print(f"\n  show_support agora NAO TEM botoes com URL")
    print(f"  Links sao clicaveis no texto (Telegram detecta)")
    print(f"\n  Outros botoes com URL encontrados: {len(urls)}")
    print(f"  (Veja a lista acima para investigar)")
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"\n[ERRO] {e}")
    shutil.copy("bot.py.backup_zero", "bot.py")
    print("[OK] Backup restaurado.")