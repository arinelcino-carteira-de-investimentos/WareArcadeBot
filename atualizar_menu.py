"""
Script para atualizar o menu de categorias
"""
import shutil
import re

print("=" * 60)
print("ATUALIZANDO MENU DE CATEGORIAS")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup-menu")
print("[OK] Backup criado!")

# Le o arquivo
with open("bot.py", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Nova funcao show_categories
nova_funcao = '''async def show_categories(update, context):
    """Exibe TODAS as categorias do catalogo - MENU PROFISSIONAL."""
    
    # Conta produtos por tipo
    contagem = {
        "🎮 Jogo": 0, "🖥️ Sistema": 0, "📄 Office": 0, "🎨 Design": 0,
        "🏗️ Engenharia": 0, "🔒 Segurança": 0, "🛠️ Ferramenta": 0,
        "🎬 Streaming": 0, "🎵 Música": 0, "🎁 Gift Card": 0,
        "☁️ Cloud": 0, "🎓 Curso": 0, "🎬 Vídeo": 0,
    }
    
    for g in GAMES_CATALOG:
        tipo = g.get("tipo", "🎮 Jogo")
        if tipo in contagem:
            contagem[tipo] += 1
    
    total = len(GAMES_CATALOG)
    ofertas = len([g for g in GAMES_CATALOG if g["oferta"]])
    
    # Soma video em design
    design_total = contagem["🎨 Design"] + contagem["🎬 Vídeo"]
    
    text = (
        f"🏷️ *MENU DE CATEGORIAS*\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"📦 *Total:* {total} produtos\\n"
        f"🔥 *Em oferta:* {ofertas} produtos\\n\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n"
        f"*ESCOLHA UMA CATEGORIA:*\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

    keyboard = [
        # Linha 1: Jogos (destaque)
        [InlineKeyboardButton(
            f"🎮 JOGOS PC ({contagem['🎮 Jogo']})",
            callback_data="cat_tipo_🎮 Jogo"
        )],
        
        # Linha 2: Sistemas e Office
        [
            InlineKeyboardButton(
                f"🖥️ Sistemas ({contagem['🖥️ Sistema']})",
                callback_data="cat_tipo_🖥️ Sistema"
            ),
            InlineKeyboardButton(
                f"📄 Office ({contagem['📄 Office']})",
                callback_data="cat_tipo_📄 Office"
            ),
        ],
        
        # Linha 3: Design e Engenharia
        [
            InlineKeyboardButton(
                f"🎨 Adobe/Design ({design_total})",
                callback_data="cat_tipo_🎨 Design"
            ),
            InlineKeyboardButton(
                f"🏗️ Engenharia ({contagem['🏗️ Engenharia']})",
                callback_data="cat_tipo_🏗️ Engenharia"
            ),
        ],
        
        # Linha 4: Antivirus e Ferramentas
        [
            InlineKeyboardButton(
                f"🔒 Antivírus ({contagem['🔒 Segurança']})",
                callback_data="cat_tipo_🔒 Segurança"
            ),
            InlineKeyboardButton(
                f"🛠️ Ferramentas ({contagem['🛠️ Ferramenta']})",
                callback_data="cat_tipo_🛠️ Ferramenta"
            ),
        ],
        
        # Linha 5: Streaming e Musica
        [
            InlineKeyboardButton(
                f"🎬 Streaming ({contagem['🎬 Streaming']})",
                callback_data="cat_tipo_🎬 Streaming"
            ),
            InlineKeyboardButton(
                f"🎵 Música ({contagem['🎵 Música']})",
                callback_data="cat_tipo_🎵 Música"
            ),
        ],
        
        # Linha 6: Gift Cards e Cloud
        [
            InlineKeyboardButton(
                f"🎁 Gift Cards ({contagem['🎁 Gift Card']})",
                callback_data="cat_tipo_🎁 Gift Card"
            ),
            InlineKeyboardButton(
                f"☁️ Cloud ({contagem['☁️ Cloud']})",
                callback_data="cat_tipo_☁️ Cloud"
            ),
        ],
        
        # Linha 7: Cursos (sozinho)
        [InlineKeyboardButton(
            f"🎓 Cursos Online ({contagem['🎓 Curso']})",
            callback_data="cat_tipo_🎓 Curso"
        )],
        
        # Linha 8: Especiais
        [
            InlineKeyboardButton("🔥 OFERTAS", callback_data="offers_0"),
            InlineKeyboardButton("🔍 BUSCAR", callback_data="search"),
        ],
        
        # Linha 9: Voltar
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

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


async def show_category_by_type(update, context, tipo, page=0):
    """Exibe produtos de um tipo especifico."""
    produtos = [g for g in GAMES_CATALOG if g.get("tipo") == tipo]
    
    # Tratamento especial para Design (inclui Video)
    if tipo == "🎨 Design":
        produtos = [g for g in GAMES_CATALOG if g.get("tipo") in ["🎨 Design", "🎬 Vídeo"]]
    
    if not produtos:
        await update.callback_query.answer(f"Nenhum produto na categoria {tipo}")
        return
    
    nomes_categoria = {
        "🎮 Jogo": "JOGOS PARA PC",
        "🖥️ Sistema": "SISTEMAS OPERACIONAIS",
        "📄 Office": "MICROSOFT OFFICE",
        "🎨 Design": "ADOBE / DESIGN",
        "🏗️ Engenharia": "ENGENHARIA & 3D",
        "🔒 Segurança": "ANTIVÍRUS & SEGURANÇA",
        "🛠️ Ferramenta": "FERRAMENTAS",
        "🎬 Streaming": "STREAMING",
        "🎵 Música": "MÚSICA",
        "🎁 Gift Card": "GIFT CARDS",
        "☁️ Cloud": "CLOUD STORAGE",
        "🎓 Curso": "CURSOS ONLINE",
    }
    
    nome_cat = nomes_categoria.get(tipo, tipo)
    import math
    total_pages = max(1, math.ceil(len(produtos) / ITEMS_PER_PAGE))
    
    text = (
        f"{tipo} *{nome_cat}*\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n"
        f"📦 {len(produtos)} produtos\\n"
        f"📄 Página {page + 1} de {total_pages}\\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"_Toque em um produto para ver detalhes:_"
    )
    
    keyboard = catalog_keyboard(page, produtos, f"tipopage_{tipo}")
    
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )


'''

# Procura a funcao show_categories atual
padrao = re.compile(
    r'async def show_categories\(update, context\):.*?(?=\n\nasync def |\ndef )',
    re.DOTALL
)

match = padrao.search(conteudo)
if not match:
    print("[ERRO] Nao encontrei show_categories!")
    exit()

# Substitui
novo_conteudo = conteudo[:match.start()] + nova_funcao + conteudo[match.end():]

# Adiciona o handler de "cat_tipo_" no callback_handler
# Procura "elif data.startswith(\"cat_\"):" para adicionar antes
if 'elif data.startswith("cat_tipo_"):' not in novo_conteudo:
    # Procura a linha "elif data.startswith(\"cat_\"):"
    padrao_handler = 'elif data.startswith("cat_"):'
    novo_handler = '''elif data.startswith("cat_tipo_"):
            tipo = data.replace("cat_tipo_", "")
            await show_category_by_type(update, context, tipo, 0)

        elif data.startswith("tipopage_"):
            parts = data.split("_")
            page = int(parts[-1])
            tipo = "_".join(parts[1:-1])
            await show_category_by_type(update, context, tipo, page)

        elif data.startswith("cat_"):'''
    
    novo_conteudo = novo_conteudo.replace(padrao_handler, novo_handler)
    print("[OK] Handler adicionado!")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(novo_conteudo)

print("[OK] bot.py atualizado!")

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\n>>> Agora rode: python bot.py")
except SyntaxError as e:
    print(f"[ERRO] Sintaxe: {e}")
    shutil.copy("bot.py.backup-menu", "bot.py")
    print("[OK] Backup restaurado.")

print("=" * 60)