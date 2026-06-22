"""
Script para atualizar a funcao start() do bot.py
"""
import shutil
import re

print("=" * 60)
print("ATUALIZANDO TELA INICIAL DO BOT")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup-start")
print("[OK] Backup criado!")

# Le o arquivo
with open("bot.py", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Nova funcao start
nova_start = '''async def start(update, context):
    """Handler do comando /start - TELA INICIAL COM RESUMO DO CATALOGO."""
    user = update.effective_user
    get_or_create_customer(user.id, user.username)
    clear_user_state(user.id)

    total = len(GAMES_CATALOG)
    jogos = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎮 Jogo"])
    sistemas = len([g for g in GAMES_CATALOG if g.get("tipo") == "🖥️ Sistema"])
    office = len([g for g in GAMES_CATALOG if g.get("tipo") == "📄 Office"])
    design = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎨 Design"])
    engenharia = len([g for g in GAMES_CATALOG if g.get("tipo") == "🏗️ Engenharia"])
    antivirus = len([g for g in GAMES_CATALOG if g.get("tipo") == "🔒 Segurança"])
    ferramentas = len([g for g in GAMES_CATALOG if g.get("tipo") == "🛠️ Ferramenta"])
    streaming = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎬 Streaming"])
    musica = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎵 Música"])
    giftcards = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎁 Gift Card"])
    cloud = len([g for g in GAMES_CATALOG if g.get("tipo") == "☁️ Cloud"])
    cursos = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎓 Curso"])
    video = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎬 Vídeo"])
    design_total = design + video

    precos = [g["preco_oferta"] for g in GAMES_CATALOG]
    preco_min = min(precos)
    preco_max = max(precos)
    preco_medio = sum(precos) / len(precos)
    ofertas = len([g for g in GAMES_CATALOG if g["oferta"]])

    welcome = (
        f"🎮💻 *NEXUS DIGITAL SHOP*\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"Olá, *{user.first_name}*! 👋\\n\\n"
        f"🏆 *CATÁLOGO COMPLETO - {total} PRODUTOS*\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n"
        f"🎮 Jogos PC ............... `{jogos:>3} produtos`\\n"
        f"🖥️ Sistemas Operacionais .. `{sistemas:>3} produtos`\\n"
        f"📄 Microsoft Office ....... `{office:>3} produtos`\\n"
        f"🎨 Adobe/Design ........... `{design_total:>3} produtos`\\n"
        f"🏗️ Engenharia/3D .......... `{engenharia:>3} produtos`\\n"
        f"🔒 Antivírus .............. `{antivirus:>3} produtos`\\n"
        f"🛠️ Ferramentas ............ `{ferramentas:>3} produtos`\\n"
        f"🎬 Streaming .............. `{streaming:>3} produtos`\\n"
        f"🎵 Música ................. `{musica:>3} produtos`\\n"
        f"🎁 Gift Cards ............. `{giftcards:>3} produtos`\\n"
        f"☁️ Cloud Storage .......... `{cloud:>3} produtos`\\n"
        f"🎓 Cursos ................. `{cursos:>3} produtos`\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"📊 *INFORMAÇÕES:*\\n"
        f"• 📦 Total: *{total} produtos*\\n"
        f"• 🔥 Em oferta: *{ofertas} produtos*\\n"
        f"• 💰 Faixa: *R$ {preco_min:.2f}* a *R$ {preco_max:.2f}*\\n"
        f"• 💵 Ticket médio: *~R$ {preco_medio:.2f}*\\n\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n"
        f"⚡ Entrega imediata | 🔒 100% Seguro\\n"
        f"💚 PIX | 💳 Cartão | 📄 Boleto\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"👇 *Escolha uma opção:*"
    )

    keyboard = [
        [InlineKeyboardButton("🎮 Ver Catálogo Completo", callback_data="catalog_0")],
        [InlineKeyboardButton("🔥 Ofertas Imperdíveis", callback_data="offers_0"),
         InlineKeyboardButton("🔍 Buscar Produto", callback_data="search")],
        [InlineKeyboardButton("🏷️ Categorias", callback_data="categories"),
         InlineKeyboardButton("🛒 Meu Carrinho", callback_data="cart")],
        [InlineKeyboardButton("📦 Meus Pedidos", callback_data="my_orders"),
         InlineKeyboardButton("👤 Meu Cadastro", callback_data="my_profile")],
        [InlineKeyboardButton("❓ FAQ / Ajuda", callback_data="faq"),
         InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]

    if update.message:
        await update.message.reply_text(
            welcome, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                welcome, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception:
            await update.callback_query.message.reply_text(
                welcome, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )


'''

# Procura a funcao start atual
padrao = re.compile(
    r'async def start\(update, context\):.*?(?=\n\nasync def |\ndef |\nasync def )',
    re.DOTALL
)

match = padrao.search(conteudo)
if not match:
    print("[ERRO] Nao encontrei a funcao start!")
    exit()

# Substitui
novo_conteudo = conteudo[:match.start()] + nova_start + conteudo[match.end():]

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(novo_conteudo)

print("[OK] Funcao start() atualizada!")

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\n>>> Agora rode: python bot.py")
except SyntaxError as e:
    print(f"[ERRO] Sintaxe: {e}")
    shutil.copy("bot.py.backup-start", "bot.py")
    print("[OK] Backup restaurado.")

print("=" * 60)