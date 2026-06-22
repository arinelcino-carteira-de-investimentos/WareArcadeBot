"""
Adiciona sistema de cupons ao bot
"""
import shutil

print("=" * 60)
print("ADICIONANDO SISTEMA DE CUPONS")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup_cupons")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Adiciona dicionario de cupons
cupons_code = '''

# ════════════════════════════════════════
# SISTEMA DE CUPONS
# ════════════════════════════════════════

CUPONS_VALIDOS = {
    "WELCOME10": {"desconto": 10, "descricao": "Boas-vindas - 1a compra"},
    "OFFER10": {"desconto": 10, "descricao": "Oferta geral"},
    "GRUPO15": {"desconto": 15, "descricao": "Cupom WhatsApp grupos"},
    "FLASH20": {"desconto": 20, "descricao": "Flash Sale 24h"},
    "SAUDADE25": {"desconto": 25, "descricao": "Cliente inativo"},
    "BLACK50": {"desconto": 50, "descricao": "Black Friday"},
    "VOLTA15": {"desconto": 15, "descricao": "Recuperacao carrinho"},
    "INDICA20": {"desconto": 20, "descricao": "Programa indicacao"},
    "FIDELIDADE10": {"desconto": 10, "descricao": "Cliente fiel"},
    "ANIVERSARIO": {"desconto": 30, "descricao": "Aniversario"},
    "SEMANA10": {"desconto": 10, "descricao": "Oferta da semana"},
    "ULTIMA20": {"desconto": 20, "descricao": "Ultima chance"},
}


def validar_cupom(codigo):
    """Valida e retorna desconto do cupom."""
    codigo = codigo.upper().strip()
    if codigo in CUPONS_VALIDOS:
        return CUPONS_VALIDOS[codigo]
    return None


def aplicar_desconto(valor, codigo_cupom):
    """Aplica desconto e retorna (novo_valor, desconto_percentual)."""
    cupom = validar_cupom(codigo_cupom)
    if cupom:
        desconto_pct = cupom["desconto"]
        novo_valor = valor * (1 - desconto_pct / 100)
        return novo_valor, desconto_pct
    return valor, 0


async def show_cupom_menu(update, context):
    """Mostra como usar cupons."""
    text = (
        "🎁 *CUPONS DE DESCONTO*\\n"
        "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "*Como usar:*\\n"
        "1. Adicione produtos ao carrinho\\n"
        "2. No checkout, digite o codigo\\n"
        "3. Desconto aplicado automaticamente!\\n\\n"
        "🎟️ *CUPONS ATIVOS:*\\n\\n"
        "💚 `WELCOME10` - 10% OFF na 1a compra\\n"
        "🔥 `OFFER10` - 10% OFF geral\\n"
        "📱 `GRUPO15` - 15% OFF (WhatsApp)\\n"
        "⚡ `FLASH20` - 20% OFF (24h)\\n"
        "🎯 `INDICA20` - 20% OFF (indicacao)\\n\\n"
        "_Cupons especiais podem ser enviados!_"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Ver Carrinho", callback_data="cart")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


'''

if "CUPONS_VALIDOS" not in c:
    idx = c.find("async def show_support")
    if idx > 0:
        c = c[:idx] + cupons_code + "\n\n" + c[idx:]
        print("[OK] Sistema de cupons adicionado!")

# Adiciona botao no menu
if 'callback_data="cupons"' not in c:
    old = '[InlineKeyboardButton("🎁 Indique e Ganhe", callback_data="indique")]'
    new = '[InlineKeyboardButton("🎁 Indique e Ganhe", callback_data="indique"),\n         InlineKeyboardButton("🎟️ Cupons", callback_data="cupons")]'
    c = c.replace(old, new)
    print("[OK] Botao cupons adicionado!")

# Handler cupons
if 'elif data == "cupons":' not in c:
    c = c.replace(
        'elif data == "indique":',
        'elif data == "cupons":\n            await show_cupom_menu(update, context)\n        elif data == "indique":'
    )
    print("[OK] Handler cupons adicionado!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe OK!")
    print("\nRode: python bot.py")
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_cupons", "bot.py")
    print("[OK] Backup restaurado.")

print("=" * 60)