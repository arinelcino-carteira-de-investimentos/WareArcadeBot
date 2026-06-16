"""
================================================================
🎮 WareArcadeBot - Bot de Vendas de Jogos para Telegram
================================================================
Bot: @WareArcadeBot
Loja: WareArcadeBot
================================================================
"""

import logging
import math
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

from config import (
    TELEGRAM_BOT_TOKEN, ITEMS_PER_PAGE, PAYMENT_METHODS,
    STORE_NAME, STORE_WEBSITE, STORE_EMAIL, STORE_INSTAGRAM,
    STORE_HOURS, STORE_WHATSAPP, DOWNLOAD_LINK_EXPIRY_HOURS, ADMIN_CHAT_IDS,
    PIX_CHAVE, PIX_NOME, PIX_CIDADE, PIX_TIPO,
    BANCO_NOME, BANCO_CODIGO, BANCO_AGENCIA, BANCO_CONTA,
    BANCO_CNPJ, BANCO_TITULAR
)
from catalog import (
    GAMES_CATALOG, CATEGORIES, get_game_by_id, search_games,
    get_games_by_category, get_offers, format_price, get_game_display
)
from database import (
    init_db, get_or_create_customer, update_customer, get_customer,
    is_customer_complete, add_to_cart, get_cart, get_cart_total,
    remove_from_cart, clear_cart, create_orders_from_cart,
    get_customer_orders, get_all_orders, get_user_state,
    set_user_state, clear_user_state,
    update_order_status, save_payment_proof, get_orders_by_codes,
    get_pending_orders, get_connection
)
from email_sender import send_purchase_email, send_multiple_purchase_email

# ── Logging ──
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ════════════════════════════════════════
# HELPERS - Teclados
# ════════════════════════════════════════

def main_menu_keyboard():
    """Teclado principal do bot."""
    keyboard = [
        [InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0"),
         InlineKeyboardButton("🔍 Buscar Jogo", callback_data="search")],
        [InlineKeyboardButton("🏷️ Categorias", callback_data="categories"),
         InlineKeyboardButton("🔥 Ofertas", callback_data="offers_0")],
        [InlineKeyboardButton("🛒 Meu Carrinho", callback_data="cart"),
         InlineKeyboardButton("📦 Meus Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("👤 Meu Cadastro", callback_data="my_profile"),
         InlineKeyboardButton("❓ Ajuda / FAQ", callback_data="faq")],
        [InlineKeyboardButton("📞 Falar com Suporte", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_to_menu_keyboard():
    """Botão de voltar ao menu."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")]
    ])


def catalog_keyboard(page, games, prefix="catalog"):
    """Monta teclado de catálogo paginado."""
    total_pages = max(1, math.ceil(len(games) / ITEMS_PER_PAGE))
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_games = games[start:end]

    keyboard = []
    for game in page_games:
        tag = " 🔥" if game["oferta"] else ""
        price = game["preco_oferta"]
        nome = game["nome"]
        if len(nome) > 30:
            nome = nome[:30] + "..."
        btn_text = f"🎮 {nome} R${price:.2f}{tag}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"game_{game['id']}")])

    # Navegação
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"{prefix}_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Próximo", callback_data=f"{prefix}_{page + 1}"))
    keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])

    return InlineKeyboardMarkup(keyboard)


def game_detail_keyboard(game_id):
    """Teclado de detalhes de um jogo."""
    keyboard = [
        [InlineKeyboardButton("🛒 Adicionar ao Carrinho", callback_data=f"add_cart_{game_id}")],
        [InlineKeyboardButton("⚡ Comprar Agora", callback_data=f"buy_now_{game_id}")],
        [InlineKeyboardButton("🔙 Voltar ao Catálogo", callback_data="catalog_0"),
         InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def payment_keyboard():
    """Teclado de seleção de pagamento."""
    keyboard = [
        [InlineKeyboardButton("💰 PIX (Imediato) ⚡", callback_data="pay_pix")],
        [InlineKeyboardButton("💳 Cartão de Crédito", callback_data="pay_cartao")],
        [InlineKeyboardButton("🏦 Transferência (TED)", callback_data="pay_ted")],
        [InlineKeyboardButton("📄 Boleto Bancário", callback_data="pay_boleto")],
        [InlineKeyboardButton("📱 PayPal", callback_data="pay_paypal")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def confirm_purchase_keyboard():
    """Teclado de confirmação de compra."""
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar Pedido", callback_data="confirm_purchase")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_purchase")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ════════════════════════════════════════
# COMANDOS PRINCIPAIS
# ════════════════════════════════════════

async def start(update, context):
    """Tela inicial HUMANIZADA com UX."""
    user = update.effective_user
    get_or_create_customer(user.id, user.username)
    clear_user_state(user.id)

    total = len(GAMES_CATALOG)
    jogos = len([g for g in GAMES_CATALOG if "Jogo" in g.get("tipo", "")])
    softwares = total - jogos
    ofertas = len([g for g in GAMES_CATALOG if g.get("oferta")])
    
    precos = [g["preco_oferta"] for g in GAMES_CATALOG]
    preco_min = min(precos)
    preco_max = max(precos)

    welcome = (
        f"🤖 *WareArcadeBot*\n"
        f"_A maior loja digital do Telegram_ ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Olá, *{user.first_name}*! 👋\n"
        f"Que bom te ver por aqui! 💚\n\n"
        f"🏆 *NOSSO CATALOGO HOJE:*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎮 Jogos PC ............. `{jogos:>3}` itens\n"
        f"💻 Softwares ............ `{softwares:>3}` itens\n"
        f"🔥 Em oferta ............ `{ofertas:>3}` itens\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 Total: *{total} produtos*\n"
        f"💰 De *R$ {preco_min:.2f}* a *R$ {preco_max:.2f}*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ *Entrega IMEDIATA*\n"
        f"🔒 *Pagamento 100% Seguro*\n"
        f"💚 PIX | 💳 Cartao | 📄 Boleto\n"
        f"📞 Suporte humanizado 24/7\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💡 *O que voce procura hoje?*"
    )

    keyboard = [
        [InlineKeyboardButton("🎮 Jogos para PC", callback_data="catalog_0"),
         InlineKeyboardButton("💻 Softwares", callback_data="categories")],
        [InlineKeyboardButton("🔥 Ofertas HOT", callback_data="offers_0"),
         InlineKeyboardButton("🔍 Buscar", callback_data="search")],
        [InlineKeyboardButton("🛒 Carrinho", callback_data="cart"),
         InlineKeyboardButton("📦 Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("👤 Cadastro", callback_data="my_profile"),
         InlineKeyboardButton("🎁 Indique e Ganhe", callback_data="indique")],
        [InlineKeyboardButton("🏛️ Institucional", callback_data="institutional"),
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



async def help_command(update, context):
    """Handler do comando /help."""
    text = (
        "🎮 *WAREARCADEBOT - COMANDOS*\n\n"
        "🔹 /start - Iniciar o bot\n"
        "🔹 /catalogo - Ver catálogo de jogos\n"
        "🔹 /buscar <nome> - Buscar um jogo\n"
        "🔹 /ofertas - Ver jogos em oferta\n"
        "🔹 /carrinho - Ver meu carrinho\n"
        "🔹 /pedidos - Ver meus pedidos\n"
        "🔹 /perfil - Meu cadastro\n"
        "🔹 /faq - Perguntas frequentes\n"
        "🔹 /suporte - Falar com suporte\n"
        "🔹 /help - Esta mensagem\n"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ════════════════════════════════════════
# CATÁLOGO
# ════════════════════════════════════════

async def show_catalog(update, context, page=0):
    """Exibe o catálogo de jogos paginado."""
    total = len(GAMES_CATALOG)
    total_pages = max(1, math.ceil(total / ITEMS_PER_PAGE))

    text = (
        f"🎮 *CATÁLOGO DE JOGOS PARA PC*\n\n"
        f"📦 {total} jogos disponíveis\n"
        f"📄 Página {page + 1} de {total_pages}\n\n"
        f"Selecione um jogo para ver detalhes:"
    )

    keyboard = catalog_keyboard(page, GAMES_CATALOG, "catalog")

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
            )
    elif update.message:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
        )

async def catalogo_command(update, context):
    """Comando /catalogo."""
    await show_catalog(update, context, 0)

async def show_game_detail(update, context, game_id):
    """Exibe detalhes de um jogo COM IMAGEM."""
    game = get_game_by_id(game_id)
    if not game:
        await update.callback_query.answer("❌ Jogo não encontrado!", show_alert=True)
        return

    text = get_game_display(game)
    text += "\n\n━━━━━━━━━━━━━━━━━━━━━━"
    text += "\n✅ Entrega digital imediata"
    text += "\n🔒 Pagamento 100% seguro"
    text += f"\n📧 Link válido por {DOWNLOAD_LINK_EXPIRY_HOURS}h"

    imagem_url = game.get("imagem_url", "")
    keyboard = game_detail_keyboard(game_id)

    # Apaga a mensagem anterior
    try:
        await update.callback_query.message.delete()
    except Exception:
        pass

    # Envia mensagem nova COM IMAGEM (se tiver) ou só texto
    chat_id = update.callback_query.message.chat_id

    if imagem_url:
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=imagem_url,
                caption=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )
            return
        except Exception as e:
            logger.warning(f"Não foi possível carregar imagem do jogo {game_id}: {e}")
            # Se a imagem falhar, manda só o texto

    # Fallback: envia só texto
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

# ════════════════════════════════════════
# BUSCA
# ════════════════════════════════════════

async def search_start(update, context):
    """Inicia o fluxo de busca."""
    user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
    set_user_state(user_id, "waiting_search")

    text = (
        "🔍 *BUSCAR JOGO*\n\n"
        "Digite o nome do jogo que você está procurando:\n\n"
        "💡 _Exemplos: FIFA, GTA, Elden Ring, Sims_"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")]
    ])

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
        )


async def buscar_command(update, context):
    """Comando /buscar <nome>."""
    if context.args:
        query = " ".join(context.args)
        results = search_games(query)
        await show_search_results(update, context, query, results)
    else:
        await search_start(update, context)


async def show_search_results(update, context, query, results):
    """Exibe resultados de busca."""
    if not results:
        text = (
            f"🔍 *Busca: \"{query}\"*\n\n"
            f"❌ Nenhum jogo encontrado.\n\n"
            f"💡 Tente outro nome ou veja o catálogo completo."
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Buscar Novamente", callback_data="search")],
            [InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0")],
            [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
        ])
        if update.message:
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        return

    text = f"🔍 *Resultados para: \"{query}\"*\n\n📦 {len(results)} jogo(s) encontrado(s):\n"

    keyboard = []
    for game in results[:15]:
        tag = " 🔥" if game["oferta"] else ""
        price = game["preco_oferta"]
        nome = game["nome"]
        if len(nome) > 35:
            nome = nome[:35] + "..."
        btn_text = f"🎮 {nome} - R${price:.2f}{tag}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"game_{game['id']}")])

    keyboard.append([InlineKeyboardButton("🔍 Nova Busca", callback_data="search")])
    keyboard.append([InlineKeyboardButton("🏠 Menu", callback_data="main_menu")])

    if update.message:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ════════════════════════════════════════
# CATEGORIAS
# ════════════════════════════════════════

async def show_categories(update, context):
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
        f"🏷️ *MENU DE CATEGORIAS*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 *Total:* {total} produtos\n"
        f"🔥 *Em oferta:* {ofertas} produtos\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"*ESCOLHA UMA CATEGORIA:*\n"
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
        f"{tipo} *{nome_cat}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 {len(produtos)} produtos\n"
        f"📄 Página {page + 1} de {total_pages}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
        f"{tipo} *{nome_cat}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 {len(produtos)} produtos\n"
        f"📄 Página {page + 1} de {total_pages}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
        f"{tipo} *{nome_cat}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 {len(produtos)} produtos\n"
        f"📄 Página {page + 1} de {total_pages}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
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




async def show_category_games(update, context, category, page=0):
    """Exibe jogos de uma categoria."""
    games = get_games_by_category(category)

    if not games:
        await update.callback_query.answer(f"Nenhum jogo na categoria {category}")
        return

    total_pages = max(1, math.ceil(len(games) / ITEMS_PER_PAGE))
    text = f"🏷️ *Categoria: {category}*\n📦 {len(games)} jogos | Página {page + 1}/{total_pages}"

    keyboard = catalog_keyboard(page, games, f"catpage_{category}")

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )


# ════════════════════════════════════════
# OFERTAS
# ════════════════════════════════════════

async def show_offers(update, context, page=0):
    """Exibe jogos em oferta."""
    offers = get_offers()
    total_pages = max(1, math.ceil(len(offers) / ITEMS_PER_PAGE))

    text = (
        f"🔥 *JOGOS EM OFERTA!*\n\n"
        f"🏷️ {len(offers)} jogos com desconto!\n"
        f"📄 Página {page + 1} de {total_pages}\n"
    )

    keyboard = catalog_keyboard(page, offers, "offers")

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
        )
    elif update.message:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
        )


async def ofertas_command(update, context):
    """Comando /ofertas."""
    await show_offers(update, context, 0)


# ════════════════════════════════════════
# CARRINHO
# ════════════════════════════════════════

async def show_cart(update, context):
    """Exibe o carrinho do usuário."""
    user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
    cart = get_cart(user_id)
    total = get_cart_total(user_id)

    if not cart:
        text = (
            "🛒 *SEU CARRINHO*\n\n"
            "📦 Seu carrinho está vazio.\n\n"
            "Vá ao catálogo para adicionar jogos!"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0")],
            [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
        ])
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        return

    text = "🛒 *SEU CARRINHO*\n\n"
    for i, item in enumerate(cart, 1):
        text += f"{i}. 🎮 {item['game_name']}\n   💰 R$ {item['price']:.2f}\n\n"

    text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"💰 *TOTAL: R$ {total:.2f}*\n"
    text += f"📦 {len(cart)} item(ns)"

    keyboard = []
    for item in cart:
        nome = item['game_name']
        if len(nome) > 25:
            nome = nome[:25] + "..."
        keyboard.append([InlineKeyboardButton(
            f"❌ Remover: {nome}",
            callback_data=f"rm_cart_{item['id']}"
        )])

    keyboard.append([InlineKeyboardButton("💳 Finalizar Compra", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("🗑️ Limpar Carrinho", callback_data="clear_cart")])
    keyboard.append([InlineKeyboardButton("🎮 Continuar Comprando", callback_data="catalog_0")])
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


async def carrinho_command(update, context):
    """Comando /carrinho."""
    await show_cart(update, context)


# ════════════════════════════════════════
# PERFIL / CADASTRO
# ════════════════════════════════════════

async def show_profile(update, context):
    """Exibe perfil do cliente."""
    user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
    customer = get_customer(user_id)

    nome = customer.get("nome_completo") or "❌ Não informado"
    email = customer.get("email") or "❌ Não informado"
    telefone = customer.get("telefone") or "❌ Não informado"
    cpf = customer.get("cpf") or "Não informado"

    complete = is_customer_complete(user_id)
    status = "✅ Completo" if complete else "⚠️ Incompleto"

    text = (
        f"👤 *MEU CADASTRO* ({status})\n\n"
        f"📛 *Nome:* {nome}\n"
        f"📧 *Email:* {email}\n"
        f"📱 *Telefone:* {telefone}\n"
        f"🆔 *CPF:* {cpf}\n"
        f"\n🔑 *Telegram ID:* `{user_id}`"
    )

    keyboard = [
        [InlineKeyboardButton("✏️ Editar Cadastro", callback_data="edit_profile")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def perfil_command(update, context):
    """Comando /perfil."""
    await show_profile(update, context)


async def start_profile_edit(update, context):
    """Inicia a edição do perfil."""
    user_id = update.callback_query.from_user.id
    set_user_state(user_id, "edit_name")

    text = (
        "✏️ *EDITAR CADASTRO*\n\n"
        "Vamos atualizar seus dados.\n\n"
        "📛 *Passo 1/4:* Digite seu *nome completo:*"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭️ Pular", callback_data="skip_name")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
    ])

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
    )


async def start_registration_for_checkout(update, context):
    """Inicia cadastro obrigatório para checkout."""
    user_id = update.callback_query.from_user.id
    set_user_state(user_id, "register_name")

    text = (
        "📋 *CADASTRO NECESSÁRIO*\n\n"
        "Para finalizar sua compra, precisamos de alguns dados.\n\n"
        "📛 *Passo 1/3:* Digite seu *nome completo:*"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancelar Compra", callback_data="main_menu")],
    ])

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
    )


# ════════════════════════════════════════
# CHECKOUT / PAGAMENTO
# ════════════════════════════════════════

async def start_checkout(update, context):
    """Inicia o processo de checkout."""
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)

    if not cart:
        await update.callback_query.answer("🛒 Seu carrinho está vazio!", show_alert=True)
        return

    if not is_customer_complete(user_id):
        await start_registration_for_checkout(update, context)
        return

    customer = get_customer(user_id)
    total = get_cart_total(user_id)

    text = "💳 *FINALIZAR COMPRA*\n\n"
    text += f"👤 *Cliente:* {customer['nome_completo']}\n"
    text += f"📧 *Email:* {customer['email']}\n\n"
    text += "🛒 *Itens do carrinho:*\n"

    for i, item in enumerate(cart, 1):
        text += f"  {i}. 🎮 {item['game_name']} - R$ {item['price']:.2f}\n"

    text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"💰 *TOTAL: R$ {total:.2f}*\n\n"
    text += "Selecione a forma de pagamento:"

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=payment_keyboard()
    )


async def process_payment(update, context, method):
    """Processa a seleção de pagamento e exibe os dados reais."""
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)
    total = get_cart_total(user_id)
    customer = get_customer(user_id)

    method_names = {
        "pix": "💰 PIX",
        "cartao": "💳 Cartão de Crédito",
        "ted": "🏦 Transferência Bancária (TED)",
        "boleto": "📄 Boleto Bancário",
        "paypal": "📱 PayPal",
    }

    method_name = method_names.get(method, method)

    set_user_state(user_id, "confirming_purchase", {
        "payment_method": method,
        "payment_method_name": method_name,
    })

    text = "📋 *INSTRUÇÕES DE PAGAMENTO*\n\n"
    text += f"👤 *Cliente:* {customer['nome_completo']}\n"
    text += f"📧 *Email:* {customer['email']}\n\n"
    text += "🛒 *Itens:*\n"
    for i, item in enumerate(cart, 1):
        text += f"  {i}. 🎮 {item['game_name']} - R$ {item['price']:.2f}\n"
    text += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"💰 *TOTAL: R$ {total:.2f}*\n"
    text += f"💳 *Pagamento:* {method_name}\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if method == "pix":
        text += (
            f"💚 *DADOS DO PIX*\n\n"
            f"🔑 *Chave PIX ({PIX_TIPO}):*\n"
            f"`{PIX_CHAVE}`\n\n"
            f"👤 *Titular:* {PIX_NOME}\n"
            f"🏙️ *Cidade:* {PIX_CIDADE}\n\n"
            f"💵 *Valor a pagar:* `R$ {total:.2f}`\n\n"
            f"⚡ *Aprovação imediata após o pagamento!*\n\n"
            f"📸 *Após pagar, clique em CONFIRMAR* e nos envie o comprovante."
        )
    elif method == "ted":
        text += (
            f"🏦 *DADOS BANCÁRIOS*\n\n"
            f"🏛️ *Banco:* {BANCO_NOME}\n"
            f"🔢 *Código:* {BANCO_CODIGO}\n"
            f"🏪 *Agência:* {BANCO_AGENCIA}\n"
            f"💳 *Conta:* {BANCO_CONTA}\n"
            f"📄 *CNPJ:* {BANCO_CNPJ}\n"
            f"👤 *Titular:* {BANCO_TITULAR}\n\n"
            f"💵 *Valor:* `R$ {total:.2f}`\n\n"
            f"📸 *Após a transferência, clique em CONFIRMAR* e envie o comprovante."
        )
    elif method == "boleto":
        text += (
            f"📄 *BOLETO BANCÁRIO*\n\n"
            f"🏛️ *Banco emissor:* {BANCO_NOME}\n"
            f"👤 *Beneficiário:* {BANCO_TITULAR}\n"
            f"📄 *CNPJ:* {BANCO_CNPJ}\n\n"
            f"💵 *Valor:* `R$ {total:.2f}`\n"
            f"📅 *Vencimento:* 3 dias úteis\n\n"
            f"📧 O boleto será enviado para: *{customer['email']}*\n"
            f"⏰ *Aprovação:* Até 3 dias úteis após o pagamento.\n\n"
            f"✅ *Clique em CONFIRMAR para gerar seu boleto.*"
        )
    elif method == "cartao":
        text += (
            f"💳 *PAGAMENTO COM CARTÃO*\n\n"
            f"🔐 Você será redirecionado para um link seguro de pagamento.\n\n"
            f"💵 *Valor:* `R$ {total:.2f}`\n"
            f"🏷️ Aceitamos: Visa, Mastercard, Amex, Elo\n"
            f"💰 Em até 12x (consulte taxas)\n\n"
            f"⚡ *Aprovação imediata!*\n\n"
            f"✅ *Clique em CONFIRMAR para receber o link.*"
        )
    elif method == "paypal":
        text += (
            f"📱 *PAGAMENTO PAYPAL*\n\n"
            f"📧 *Email PayPal:* {STORE_EMAIL}\n\n"
            f"💵 *Valor:* `R$ {total:.2f}`\n\n"
            f"⚡ *Aprovação imediata após o pagamento!*\n\n"
            f"📸 *Após pagar, clique em CONFIRMAR* e nos envie o comprovante."
        )

    text += "\n\n❓ Dúvidas? Chame nosso suporte!"

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=confirm_purchase_keyboard()
    )


async def confirm_purchase(update, context):
    """Confirma o pedido e aguarda envio do comprovante."""
    user_id = update.callback_query.from_user.id
    state, data = get_user_state(user_id)

    if state != "confirming_purchase":
        await update.callback_query.answer("❌ Sessão expirada. Tente novamente.", show_alert=True)
        return

    payment_method = data.get("payment_method_name", "N/A")
    customer = get_customer(user_id)
    cart = get_cart(user_id)

    if not cart:
        await update.callback_query.answer("🛒 Carrinho vazio!", show_alert=True)
        return

    orders = create_orders_from_cart(user_id, payment_method)

    if not orders:
        await update.callback_query.message.reply_text(
            "❌ Erro ao processar pedido. Tente novamente.",
            reply_markup=back_to_menu_keyboard()
        )
        return

    for order in orders:
        update_order_status(order["order_code"], "aguardando_aprovacao")

    total = sum(o["price"] for o in orders)
    order_codes = [o["order_code"] for o in orders]

    set_user_state(user_id, "waiting_proof", {
        "order_codes": order_codes,
        "payment_method": payment_method,
        "total": total,
    })

    text = (
        f"⏳ *PEDIDO CRIADO - AGUARDANDO PAGAMENTO*\n\n"
        f"👤 *Cliente:* {customer['nome_completo']}\n"
        f"💳 *Pagamento:* {payment_method}\n"
        f"💰 *Total:* R$ {total:.2f}\n\n"
        f"📋 *Códigos dos pedidos:*\n"
    )
    for order in orders:
        text += f"  • `{order['order_code']}` - {order['game_name']}\n"

    text += (
        f"\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📸 *ENVIE O COMPROVANTE AGORA*\n\n"
        f"Após realizar o pagamento, envie aqui no chat:\n"
        f"📷 Uma *foto* do comprovante, OU\n"
        f"📄 Um *PDF* do comprovante\n\n"
        f"⚡ Assim que aprovarmos seu pagamento, "
        f"o link de download será liberado automaticamente!\n\n"
        f"⏰ Prazo de aprovação:\n"
        f"  • PIX: até 30 minutos\n"
        f"  • TED: até 1 hora\n"
        f"  • Boleto: até 3 dias úteis"
    )

    keyboard = [
        [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancel_pending_order")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buy_now(update, context, game_id):
    """Compra direta de um jogo."""
    user_id = update.callback_query.from_user.id
    game = get_game_by_id(game_id)

    if not game:
        await update.callback_query.answer("❌ Jogo não encontrado!", show_alert=True)
        return

    clear_cart(user_id)
    add_to_cart(user_id, game["id"], game["nome"], game["preco_oferta"])
    await start_checkout(update, context)


# ════════════════════════════════════════
# COMPROVANTES E APROVAÇÃO
# ════════════════════════════════════════

async def receive_proof_handler(update, context):
    """Recebe foto ou documento (comprovante) do cliente."""
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)

    if state != "waiting_proof":
        await update.message.reply_text(
            "🤔 Recebi sua mídia, mas não há nenhum pagamento aguardando comprovante.\n\n"
            "Use o menu para fazer uma compra!",
            reply_markup=main_menu_keyboard()
        )
        return

    order_codes = data.get("order_codes", [])
    payment_method = data.get("payment_method", "N/A")
    total = data.get("total", 0.0)
    customer = get_customer(user_id)

    file_id = None
    file_type = None
    caption = update.message.caption or ""

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_type = "photo"
    elif update.message.document:
        file_id = update.message.document.file_id
        file_type = "document"
    else:
        await update.message.reply_text(
            "❌ Por favor, envie uma *foto* ou *PDF* do comprovante.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    save_payment_proof(order_codes, file_id, file_type)

    confirm_text = (
        "✅ *COMPROVANTE RECEBIDO!*\n\n"
        f"📸 Recebemos seu comprovante para {len(order_codes)} pedido(s).\n\n"
        "⏳ *Aguarde a aprovação da nossa equipe.*\n\n"
        "Você receberá uma notificação aqui no Telegram assim que "
        "o pagamento for aprovado, junto com o link de download. 🎮\n\n"
        "⏰ Prazo médio: 30 minutos (horário comercial)\n"
        "📞 Dúvidas? Fale com nosso suporte!"
    )

    keyboard = [
        [InlineKeyboardButton("📦 Ver Meus Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("📞 Falar com Suporte", callback_data="support")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    await update.message.reply_text(
        confirm_text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    clear_user_state(user_id)

    # Notifica admins
    admin_caption = (
        f"🔔 *NOVO PAGAMENTO PARA APROVAR!*\n\n"
        f"👤 *Cliente:* {customer.get('nome_completo', 'N/A')}\n"
        f"📧 *Email:* {customer.get('email', 'N/A')}\n"
        f"📱 *Telefone:* {customer.get('telefone', 'N/A')}\n"
        f"🆔 *Telegram ID:* `{user_id}`\n"
        f"👤 *Username:* @{customer.get('telegram_username') or 'N/A'}\n\n"
        f"💳 *Pagamento:* {payment_method}\n"
        f"💰 *Total:* R$ {total:.2f}\n\n"
        f"🎮 *Jogos:*\n"
    )

    orders = get_orders_by_codes(order_codes)
    for order in orders:
        admin_caption += f"  • {order['game_name']} (R$ {order['price']:.2f})\n"

    admin_caption += "\n📋 *Códigos:*\n"
    for code in order_codes:
        admin_caption += f"  • `{code}`\n"

    if caption:
        admin_caption += f"\n💬 *Mensagem do cliente:*\n_{caption}_"

    main_code = order_codes[0]
    admin_keyboard = [
        [
            InlineKeyboardButton("✅ APROVAR", callback_data=f"approve_{main_code}"),
            InlineKeyboardButton("❌ REJEITAR", callback_data=f"reject_{main_code}"),
        ],
        [
            InlineKeyboardButton("💬 Falar c/ Cliente", url=f"tg://user?id={user_id}"),
        ]
    ]

    for admin_id in ADMIN_CHAT_IDS:
        if not admin_id:
            continue
        try:
            if file_type == "photo":
                await context.bot.send_photo(
                    chat_id=admin_id,
                    photo=file_id,
                    caption=admin_caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(admin_keyboard)
                )
            else:
                await context.bot.send_document(
                    chat_id=admin_id,
                    document=file_id,
                    caption=admin_caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(admin_keyboard)
                )
        except Exception as e:
            logger.error(f"Erro ao notificar admin {admin_id}: {e}")


async def approve_payment(update, context, main_order_code):
    """Admin aprova o pagamento e libera o download."""
    query = update.callback_query
    admin_id = query.from_user.id

    if admin_id not in ADMIN_CHAT_IDS:
        await query.answer("❌ Apenas admins podem aprovar pagamentos!", show_alert=True)
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (main_order_code,))
    main_order = cursor.fetchone()

    if not main_order:
        conn.close()
        await query.answer("❌ Pedido não encontrado!", show_alert=True)
        return

    main_order = dict(main_order)
    telegram_id = main_order["telegram_id"]

    cursor.execute("""
        SELECT * FROM orders
        WHERE telegram_id = ?
        AND status = 'aguardando_aprovacao'
        ORDER BY created_at DESC
    """, (telegram_id,))
    pending_orders = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not pending_orders:
        await query.answer("⚠️ Nenhum pedido pendente encontrado.", show_alert=True)
        return

    for order in pending_orders:
        update_order_status(order["order_code"], "aprovado")

    customer = get_customer(telegram_id)
    total = sum(o["price"] for o in pending_orders)

    try:
        original_caption = query.message.caption or ""
        admin_username = query.from_user.username or query.from_user.first_name
        new_caption = f"✅ *APROVADO* por @{admin_username}\n\n{original_caption}"
        await query.edit_message_caption(
            caption=new_caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
        )
    except Exception as e:
        logger.error(f"Erro ao editar mensagem admin: {e}")

    await query.answer("✅ Pagamento aprovado! Cliente notificado.", show_alert=True)

    client_text = "🎉 *PAGAMENTO APROVADO!*\n\n"
    client_text += f"Olá *{customer.get('nome_completo', 'cliente')}*! 👋\n\n"
    client_text += "Seu pagamento foi confirmado e seus jogos já estão liberados!\n\n"
    client_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    client_text += "🎮 *SEUS DOWNLOADS:*\n\n"

    for order in pending_orders:
        client_text += (
            f"📋 Pedido: `{order['order_code']}`\n"
            f"🎮 *{order['game_name']}*\n"
            f"⬇️ [BAIXAR AQUI]({order['download_url']})\n\n"
        )

    client_text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    client_text += f"💰 *Total pago:* R$ {total:.2f}\n"
    client_text += f"⏰ Links válidos por {DOWNLOAD_LINK_EXPIRY_HOURS} horas\n\n"
    client_text += f"📧 Os links também foram enviados para: {customer.get('email', '')}\n\n"
    client_text += "Aproveite seus jogos! 🎮🚀\n\n"
    client_text += "_Obrigado por comprar conosco!_"

    client_keyboard = [
        [InlineKeyboardButton("📦 Ver Meus Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("🎮 Comprar Mais Jogos", callback_data="catalog_0")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    try:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=client_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(client_keyboard),
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Erro ao notificar cliente {telegram_id}: {e}")

    if customer.get("email"):
        try:
            send_multiple_purchase_email(
                customer["email"],
                customer.get("nome_completo", "Cliente"),
                pending_orders
            )
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")


async def reject_payment(update, context, main_order_code):
    """Admin rejeita o pagamento."""
    query = update.callback_query
    admin_id = query.from_user.id

    if admin_id not in ADMIN_CHAT_IDS:
        await query.answer("❌ Apenas admins podem rejeitar!", show_alert=True)
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (main_order_code,))
    main_order = cursor.fetchone()

    if not main_order:
        conn.close()
        await query.answer("❌ Pedido não encontrado!", show_alert=True)
        return

    main_order = dict(main_order)
    telegram_id = main_order["telegram_id"]

    cursor.execute("""
        SELECT * FROM orders
        WHERE telegram_id = ?
        AND status = 'aguardando_aprovacao'
    """, (telegram_id,))
    pending_orders = [dict(r) for r in cursor.fetchall()]
    conn.close()

    for order in pending_orders:
        update_order_status(order["order_code"], "rejeitado")

    customer = get_customer(telegram_id)

    try:
        original_caption = query.message.caption or ""
        admin_username = query.from_user.username or query.from_user.first_name
        new_caption = f"❌ *REJEITADO* por @{admin_username}\n\n{original_caption}"
        await query.edit_message_caption(
            caption=new_caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
        )
    except Exception as e:
        logger.error(f"Erro ao editar mensagem admin: {e}")

    await query.answer("❌ Pagamento rejeitado! Cliente notificado.", show_alert=True)

    client_text = (
        "⚠️ *PROBLEMA COM SEU PAGAMENTO*\n\n"
        f"Olá *{customer.get('nome_completo', 'cliente')}*,\n\n"
        "Infelizmente não conseguimos confirmar seu pagamento.\n\n"
        "*Possíveis motivos:*\n"
        "• Comprovante ilegível ou inválido\n"
        "• Valor pago diferente do total do pedido\n"
        "• Dados do destinatário incorretos\n"
        "• Pagamento ainda não compensado\n\n"
        "💬 *Por favor, entre em contato com nosso suporte* "
        "para resolver a situação.\n\n"
        f"📱 WhatsApp: {STORE_WHATSAPP}\n"
        f"📧 Email: {STORE_EMAIL}"
    )

    client_keyboard = [
        [InlineKeyboardButton("📞 Falar com Suporte", callback_data="support")],
        [InlineKeyboardButton("🛒 Tentar Novamente", callback_data="catalog_0")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    try:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=client_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(client_keyboard)
        )
    except Exception as e:
        logger.error(f"Erro ao notificar cliente {telegram_id}: {e}")


# ════════════════════════════════════════
# PEDIDOS
# ════════════════════════════════════════

async def show_orders(update, context):
    """Exibe os pedidos do cliente."""
    user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
    orders = get_customer_orders(user_id)

    if not orders:
        text = "📦 *MEUS PEDIDOS*\n\n❌ Você ainda não tem pedidos."
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0")],
            [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
        ])
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        return

    text = f"📦 *MEUS PEDIDOS* ({len(orders)} pedido(s))\n\n"
    for order in orders[:10]:
        status_emoji = {
            "aprovado": "✅",
            "aguardando_aprovacao": "⏳",
            "rejeitado": "❌",
            "cancelado": "🚫",
            "pendente": "⏳",
            "confirmado": "✅",
        }.get(order["status"], "❓")

        text += (
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{status_emoji} `{order['order_code']}`\n"
            f"🎮 {order['game_name']}\n"
            f"💰 R$ {order['price']:.2f}\n"
            f"📅 {order['created_at'][:10]}\n"
            f"📊 Status: {order['status'].upper()}\n"
        )
        if order["status"] in ["aprovado", "confirmado"]:
            text += f"⬇️ [Download]({order['download_url']})\n"

    keyboard = [
        [InlineKeyboardButton("🎮 Continuar Comprando", callback_data="catalog_0")],
        [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
    ]

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )


async def pedidos_command(update, context):
    """Comando /pedidos."""
    await show_orders(update, context)


# ════════════════════════════════════════
# FAQ E SUPORTE
# ════════════════════════════════════════

async def show_faq(update, context):
    """Exibe perguntas frequentes."""
    text = (
        "❓ *PERGUNTAS FREQUENTES*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "*🔹 O envio é imediato após a compra?*\n"
        "Sim! Após a confirmação do pagamento, o link de download é enviado "
        "imediatamente pelo Telegram e também por email.\n\n"
        "*🔹 Quais as formas de pagamento?*\n"
        "💰 PIX (aprovação imediata) ⚡\n"
        "💳 Cartão de Crédito\n"
        "🏦 Transferência Bancária (TED)\n"
        "📄 Boleto Bancário\n"
        "📱 PayPal\n\n"
        "*🔹 Como receberei meu jogo?*\n"
        "Você receberá um link de download exclusivo aqui no Telegram e "
        f"no email cadastrado. O link é válido por {DOWNLOAD_LINK_EXPIRY_HOURS} horas.\n\n"
        "*🔹 Os jogos são originais?*\n"
        "Sim! Todos os jogos são licenciados e verificados.\n\n"
        "*🔹 Posso comprar com segurança?*\n"
        "Totalmente! Utilizamos sistemas de pagamento seguros.\n\n"
        "*🔹 Há custo de envio?*\n"
        "Não! A entrega é 100% digital.\n\n"
        "*🔹 Qual o prazo de aprovação?*\n"
        "• PIX: Imediato ⚡\n"
        "• Cartão: Imediato\n"
        "• TED: Até 1 hora útil\n"
        "• Boleto: Até 3 dias úteis\n\n"
        "*🔹 Como entrar em contato?*\n"
        f"📧 {STORE_EMAIL}\n"
        f"📱 WhatsApp: {STORE_WHATSAPP}\n"
        f"📸 Instagram: {STORE_INSTAGRAM}\n"
        f"⏰ {STORE_HOURS}\n"
    )

    keyboard = [
        [InlineKeyboardButton("📞 Falar com Suporte", callback_data="support")],
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


async def faq_command(update, context):
    """Comando /faq."""
    await show_faq(update, context)




async def show_institutional(update, context):
    """Menu Institucional completo."""
    text = (
        "🏛️ *INSTITUCIONAL - WareArcadeBot*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Conheca nossa loja e politicas.\n"
        "Sua seguranca e prioridade!\n\n"
        "*Escolha uma opcao:*"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Sobre Nos", callback_data="inst_sobre"),
         InlineKeyboardButton("🎯 Missao", callback_data="inst_missao")],
        [InlineKeyboardButton("🔒 Privacidade", callback_data="inst_privacidade"),
         InlineKeyboardButton("📜 Termos", callback_data="inst_termos")],
        [InlineKeyboardButton("🚚 Entrega", callback_data="inst_entrega"),
         InlineKeyboardButton("💰 Reembolso", callback_data="inst_reembolso")],
        [InlineKeyboardButton("🛡️ Garantias", callback_data="inst_garantia"),
         InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)


async def institutional_detail(update, context, page):
    """Paginas detalhadas do institucional."""
    paginas = {
        "sobre": (
            "📖 *SOBRE NOS - WareArcadeBot*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Somos a *maior loja digital* do Telegram!\n\n"
            "🎮 92+ jogos PC originais\n"
            "🖥️ Sistemas operacionais\n"
            "📄 Microsoft Office completo\n"
            "🎨 Adobe Creative Cloud\n"
            "🏗️ AutoCAD, SketchUp, Revit\n"
            "🔒 Antivirus premium\n"
            "🛠️ Ferramentas profissionais\n"
            "🎬 Streaming (Netflix, Disney+)\n"
            "🎵 Spotify, YouTube Premium\n"
            "🎁 Gift Cards (Steam, PSN, Xbox)\n"
            "☁️ Cloud (Google, iCloud, Dropbox)\n"
            "🎓 Cursos online completos\n\n"
            "🏆 *DIFERENCIAIS:*\n"
            "⚡ Entrega 100% imediata\n"
            "💰 Os menores precos do Brasil\n"
            "🔒 Pagamento via PIX/Cartao\n"
            "📞 Suporte humano via WhatsApp\n"
            "✅ +2.500 clientes satisfeitos"
        ),
        "missao": (
            "🎯 *NOSSA MISSAO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*MISSAO:*\n"
            "Democratizar o acesso a softwares e jogos\n"
            "premium com precos justos e entrega imediata.\n\n"
            "*VISAO:*\n"
            "Ser a maior loja digital do Telegram BR ate 2026.\n\n"
            "*VALORES:*\n"
            "✅ Honestidade nos precos\n"
            "✅ Entrega rapida e segura\n"
            "✅ Atendimento humanizado\n"
            "✅ Produtos 100% originais\n"
            "✅ Suporte pos-venda completo"
        ),
        "privacidade": (
            "🔒 *POLITICA DE PRIVACIDADE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Seus dados sao *protegidos* por nos!\n\n"
            "1️⃣ Coletamos apenas o necessario:\n"
            "   nome, email e telefone.\n\n"
            "2️⃣ NUNCA armazenamos dados de cartao.\n\n"
            "3️⃣ NUNCA compartilhamos com terceiros.\n\n"
            "4️⃣ Voce pode pedir exclusao a qualquer\n"
            "   momento pelo suporte.\n\n"
            "5️⃣ Pagamentos processados por gateways\n"
            "   seguros (PIX, Mercado Pago).\n\n"
            "6️⃣ Cumprimos a LGPD integralmente.\n\n"
            "_Atualizado em: 2025_"
        ),
        "termos": (
            "📜 *TERMOS DE USO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ao comprar conosco, voce concorda:\n\n"
            "1️⃣ Produtos sao digitais e entregues\n"
            "   apos confirmacao do pagamento.\n\n"
            "2️⃣ Links validos por 48 horas.\n\n"
            "3️⃣ Uso *pessoal* apenas.\n"
            "   Proibida redistribuicao.\n\n"
            "4️⃣ Oferecemos suporte para ativacao\n"
            "   e instalacao por 30 dias.\n\n"
            "5️⃣ Nao nos responsabilizamos por\n"
            "   incompatibilidade do hardware.\n\n"
            "6️⃣ Reembolso conforme nossa politica."
        ),
        "entrega": (
            "🚚 *POLITICA DE ENTREGA*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Como funciona:*\n\n"
            "1️⃣ Voce escolhe o produto\n"
            "2️⃣ Adiciona ao carrinho\n"
            "3️⃣ Faz o pagamento\n"
            "4️⃣ Envia o comprovante\n"
            "5️⃣ Apos aprovacao, recebe:\n"
            "   📱 Link aqui no Telegram\n"
            "   📧 Link por email\n\n"
            "*Tempo medio:*\n"
            "⚡ PIX: 5 a 30 minutos\n"
            "💳 Cartao: 5 a 15 minutos\n"
            "🏦 TED: 1 a 4 horas uteis\n"
            "📄 Boleto: 1 a 3 dias uteis\n\n"
            "_*Entrega garantida em 100% dos casos!*_"
        ),
        "reembolso": (
            "💰 *POLITICA DE REEMBOLSO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Voce esta seguro conosco!*\n\n"
            "✅ *7 dias de garantia* (CDC)\n\n"
            "1️⃣ Arrependimento: reembolso em 7 dias\n"
            "   ANTES de baixar/ativar o produto.\n\n"
            "2️⃣ Problema tecnico: substituicao ou\n"
            "   reembolso integral.\n\n"
            "3️⃣ Apos download/ativacao:\n"
            "   reembolso nao se aplica.\n\n"
            "4️⃣ Produto errado: reembolso 100%.\n\n"
            "*Como solicitar:*\n"
            "Entre em contato com nosso suporte\n"
            "pelo Telegram ou WhatsApp."
        ),
        "garantia": (
            "🛡️ *NOSSAS GARANTIAS*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔒 *PRODUTO ORIGINAL*\n"
            "Todos sao licenciados e verificados.\n\n"
            "⚡ *ENTREGA IMEDIATA*\n"
            "Apos pagamento, voce recebe na hora.\n\n"
            "💚 *SUPORTE HUMANIZADO*\n"
            "Atendimento real, sem robos chatos.\n\n"
            "🔄 *TROCA GARANTIDA*\n"
            "Se nao funcionar, trocamos sem custo.\n\n"
            "🎯 *MELHOR PRECO*\n"
            "Achou mais barato? Cobrimos a oferta!\n\n"
            "✅ *+2.500 CLIENTES SATISFEITOS*\n"
            "Avaliacao 5 estrelas em todas redes!"
        ),
    }

    texto = paginas.get(page, "Pagina nao encontrada.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Voltar", callback_data="institutional")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(texto, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        except Exception:
            await update.callback_query.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)






async def show_indique(update, context):
    """Programa Indique e Ganhe - HUMANIZADO."""
    user_id = update.callback_query.from_user.id if update.callback_query else update.effective_user.id
    
    text = (
        "🎁 *INDIQUE E GANHE R$ 15!*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Compartilhe a alegria! 💚\n\n"
        "*Como funciona:*\n\n"
        "1️⃣ Compartilhe nosso bot com amigos\n"
        "2️⃣ Quando ele comprar, voce ganha R$ 15\n"
        "3️⃣ Use o credito em qualquer produto\n\n"
        "🔗 *Seu link exclusivo:*\n"
        f"`https://t.me/WareArcadeBot?start=ref_{user_id}`\n\n"
        "💚 *Voce indica, todos ganham!*\n\n"
        "_Sem limites de indicacoes!_"
    )
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📲 Compartilhar Agora", 
            url=f"https://t.me/share/url?url=https://t.me/WareArcadeBot?start=ref_{user_id}&text=🎮 Achei uma loja TOP de jogos e softwares baratos! Vem comigo!")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
        except Exception:
            await update.callback_query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)






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
        "🎁 *CUPONS DE DESCONTO*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "*Como usar:*\n"
        "1. Adicione produtos ao carrinho\n"
        "2. No checkout, digite o codigo\n"
        "3. Desconto aplicado automaticamente!\n\n"
        "🎟️ *CUPONS ATIVOS:*\n\n"
        "💚 `WELCOME10` - 10% OFF na 1a compra\n"
        "🔥 `OFFER10` - 10% OFF geral\n"
        "📱 `GRUPO15` - 15% OFF (WhatsApp)\n"
        "⚡ `FLASH20` - 20% OFF (24h)\n"
        "🎯 `INDICA20` - 20% OFF (indicacao)\n\n"
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




async def show_support(update, context):
    """Exibe informações de suporte."""
    whatsapp_clean = "".join(filter(str.isdigit, STORE_WHATSAPP))
    instagram_clean = STORE_INSTAGRAM.replace("@", "")

    text = (
        f"📞 *SUPORTE AO CLIENTE*\n\n"
        f"🏪 *{STORE_NAME}*\n\n"
        f"📧 *Email:* {STORE_EMAIL}\n"
        f"📱 *WhatsApp:* {STORE_WHATSAPP}\n"
        f"📸 *Instagram:* {STORE_INSTAGRAM}\n"
        f"🌐 *Site:* {STORE_WEBSITE}\n"
        f"⏰ *Horário:* {STORE_HOURS}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 *Precisa de ajuda?*\n"
        "Envie uma mensagem descrevendo seu problema "
        "que nossa equipe responderá o mais rápido possível!"
    )

    keyboard = [
        [InlineKeyboardButton("📱 Chamar no WhatsApp", url=f"https://wa.me/{whatsapp_clean}")],
        [InlineKeyboardButton("📧 Enviar Email", url=f"mailto:{STORE_EMAIL}")],
        [InlineKeyboardButton("🌐 Visitar Site", url=STORE_WEBSITE)],
        [InlineKeyboardButton("📸 Instagram", url=f"https://instagram.com/{instagram_clean}")],
        [InlineKeyboardButton("❓ Ver FAQ", callback_data="faq")],
        [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def suporte_command(update, context):
    """Comando /suporte."""
    await show_support(update, context)


# ════════════════════════════════════════
# ADMIN
# ════════════════════════════════════════

async def admin_command(update, context):
    """Comando /admin - Painel administrativo."""
    user_id = update.effective_user.id
    if user_id not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ Acesso negado.")
        return

    orders = get_all_orders()
    pending = get_pending_orders()
    total_revenue = sum(o["price"] for o in orders if o["status"] == "aprovado")
    total_orders = len(orders)
    approved_orders = len([o for o in orders if o["status"] == "aprovado"])

    text = (
        f"🔧 *PAINEL ADMINISTRATIVO*\n\n"
        f"📊 *Estatísticas:*\n"
        f"📦 Total de pedidos: {total_orders}\n"
        f"✅ Pedidos aprovados: {approved_orders}\n"
        f"⏳ Pendentes de aprovação: *{len(pending)}*\n"
        f"💰 Receita confirmada: R$ {total_revenue:.2f}\n\n"
    )

    if pending:
        text += "⏳ *PEDIDOS AGUARDANDO APROVAÇÃO:*\n"
        for order in pending[:10]:
            customer = get_customer(order["telegram_id"])
            nome = customer.get("nome_completo", "?") if customer else "?"
            text += (
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 `{order['order_code']}`\n"
                f"👤 {nome}\n"
                f"🎮 {order['game_name']}\n"
                f"💰 R$ {order['price']:.2f}\n"
                f"💳 {order['payment_method']}\n"
            )
    else:
        text += "✅ Nenhum pedido aguardando aprovação!\n\n"
        if orders:
            text += "*Últimos 5 pedidos:*\n"
            for order in orders[:5]:
                status_emoji = {
                    "aprovado": "✅",
                    "aguardando_aprovacao": "⏳",
                    "rejeitado": "❌",
                    "cancelado": "🚫",
                }.get(order["status"], "❓")
                text += (
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"{status_emoji} `{order['order_code']}`\n"
                    f"🎮 {order['game_name']}\n"
                    f"💰 R$ {order['price']:.2f}\n"
                )

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ════════════════════════════════════════
# CALLBACK QUERY HANDLER CENTRAL
# ════════════════════════════════════════

async def callback_handler(update, context):
    """Handler central para todos os callback queries."""
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == "main_menu":
            clear_user_state(query.from_user.id)
            await start(update, context)

        elif data == "noop":
            pass

        elif data.startswith("catalog_"):
            page = int(data.split("_")[1])
            await show_catalog(update, context, page)

        elif data.startswith("game_"):
            game_id = int(data.split("_")[1])
            await show_game_detail(update, context, game_id)

        elif data.startswith("add_cart_"):
            game_id = int(data.split("_")[2])
            game = get_game_by_id(game_id)
            if game:
                add_to_cart(query.from_user.id, game["id"], game["nome"], game["preco_oferta"])
                await query.answer(f"✅ {game['nome']} adicionado ao carrinho!", show_alert=True)
                await show_cart(update, context)

        elif data.startswith("buy_now_"):
            game_id = int(data.split("_")[2])
            await buy_now(update, context, game_id)

        elif data.startswith("rm_cart_"):
            cart_item_id = int(data.split("_")[2])
            remove_from_cart(query.from_user.id, cart_item_id)
            await query.answer("✅ Item removido!")
            await show_cart(update, context)

        elif data == "clear_cart":
            clear_cart(query.from_user.id)
            await query.answer("🗑️ Carrinho limpo!")
            await show_cart(update, context)

        elif data == "cart":
            await show_cart(update, context)

        elif data == "search":
            await search_start(update, context)

        elif data == "categories":
            await show_categories(update, context)

        elif data.startswith("catpage_"):
            parts = data.split("_")
            page = int(parts[-1])
            category = "_".join(parts[1:-1])
            await show_category_games(update, context, category, page)

        elif data.startswith("cat_tipo_"):
            tipo = data.replace("cat_tipo_", "")
            await show_category_by_type(update, context, tipo, 0)

        elif data.startswith("tipopage_"):
            parts = data.split("_")
            page = int(parts[-1])
            tipo = "_".join(parts[1:-1])
            await show_category_by_type(update, context, tipo, page)

        elif data.startswith("cat_"):
            category = data[4:]
            await show_category_games(update, context, category, 0)

        elif data.startswith("offers_"):
            page = int(data.split("_")[1])
            await show_offers(update, context, page)

        elif data == "checkout":
            await start_checkout(update, context)

        elif data.startswith("pay_"):
            method = data[4:]
            await process_payment(update, context, method)

        elif data == "confirm_purchase":
            await confirm_purchase(update, context)

        elif data == "cancel_purchase":
            clear_user_state(query.from_user.id)
            await query.answer("❌ Compra cancelada.")
            await start(update, context)

        elif data == "my_orders":
            await show_orders(update, context)

        elif data == "my_profile":
            await show_profile(update, context)

        elif data == "edit_profile":
            await start_profile_edit(update, context)

        elif data == "skip_name":
            set_user_state(query.from_user.id, "edit_email")
            await query.edit_message_text(
                "📧 *Passo 2/4:* Digite seu *email:*",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏭️ Pular", callback_data="skip_email")],
                    [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
                ])
            )

        elif data == "skip_email":
            set_user_state(query.from_user.id, "edit_phone")
            await query.edit_message_text(
                "📱 *Passo 3/4:* Digite seu *telefone:*\n_Exemplo: (11) 99999-9999_",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏭️ Pular", callback_data="skip_phone")],
                    [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
                ])
            )

        elif data == "skip_phone":
            set_user_state(query.from_user.id, "edit_cpf")
            await query.edit_message_text(
                "🆔 *Passo 4/4:* Digite seu *CPF:* (opcional)",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏭️ Pular / Finalizar", callback_data="finish_profile")],
                    [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
                ])
            )

        elif data == "finish_profile":
            clear_user_state(query.from_user.id)
            await query.answer("✅ Cadastro atualizado!")
            await show_profile(update, context)

        elif data.startswith("approve_"):
            order_code = data.replace("approve_", "")
            await approve_payment(update, context, order_code)

        elif data.startswith("reject_"):
            order_code = data.replace("reject_", "")
            await reject_payment(update, context, order_code)

        elif data == "cancel_pending_order":
            user_id = query.from_user.id
            state, data_state = get_user_state(user_id)
            if state == "waiting_proof":
                order_codes = data_state.get("order_codes", [])
                for code in order_codes:
                    update_order_status(code, "cancelado")
                clear_user_state(user_id)
                await query.answer("❌ Pedido cancelado!", show_alert=True)
                await start(update, context)
            else:
                await query.answer("Nenhum pedido pendente.")

        elif data == "cupons":
            await show_cupom_menu(update, context)
        elif data == "indique":
            await show_indique(update, context)
        elif data == "institutional":
            await show_institutional(update, context)
        elif data.startswith("inst_"):
            page = data.replace("inst_", "")
            await institutional_detail(update, context, page)
        elif data == "faq":
            await show_faq(update, context)

        elif data == "support":
            await show_support(update, context)

    except Exception as e:
        logger.error(f"Erro no callback_handler: {e}", exc_info=True)
        try:
            await query.message.reply_text(
                "⚠️ Ocorreu um erro. Tente novamente.",
                reply_markup=back_to_menu_keyboard()
            )
        except Exception:
            pass


# ════════════════════════════════════════
# MESSAGE HANDLER - Textos livres
# ════════════════════════════════════════

async def message_handler(update, context):
    """Handler para mensagens de texto."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    state, data = get_user_state(user_id)

    if state == "waiting_search":
        clear_user_state(user_id)
        results = search_games(text)
        await show_search_results(update, context, text, results)
        return

    if state == "edit_name":
        update_customer(user_id, nome_completo=text)
        set_user_state(user_id, "edit_email")
        await update.message.reply_text(
            f"✅ Nome salvo: *{text}*\n\n📧 *Passo 2/4:* Digite seu *email:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ Pular", callback_data="skip_email")],
                [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
            ])
        )
        return

    if state == "edit_email":
        if "@" not in text or "." not in text:
            await update.message.reply_text("❌ Email inválido. Digite um email válido:")
            return
        update_customer(user_id, email=text)
        set_user_state(user_id, "edit_phone")
        await update.message.reply_text(
            f"✅ Email salvo: *{text}*\n\n📱 *Passo 3/4:* Digite seu *telefone:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ Pular", callback_data="skip_phone")],
                [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
            ])
        )
        return

    if state == "edit_phone":
        update_customer(user_id, telefone=text)
        set_user_state(user_id, "edit_cpf")
        await update.message.reply_text(
            f"✅ Telefone salvo: *{text}*\n\n🆔 *Passo 4/4:* Digite seu *CPF:* (opcional)",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ Pular / Finalizar", callback_data="finish_profile")],
                [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
            ])
        )
        return

    if state == "edit_cpf":
        update_customer(user_id, cpf=text)
        clear_user_state(user_id)
        await update.message.reply_text(
            "✅ *Cadastro atualizado com sucesso!*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 Ver Cadastro", callback_data="my_profile")],
                [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
            ])
        )
        return

    if state == "register_name":
        update_customer(user_id, nome_completo=text)
        set_user_state(user_id, "register_email")
        await update.message.reply_text(
            f"✅ Nome: *{text}*\n\n📧 *Passo 2/3:* Digite seu *email:*\n"
            f"_(O link de download será enviado para este email)_",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
            ])
        )
        return

    if state == "register_email":
        if "@" not in text or "." not in text:
            await update.message.reply_text("❌ Email inválido. Digite um email válido:")
            return
        update_customer(user_id, email=text)
        set_user_state(user_id, "register_phone")
        await update.message.reply_text(
            f"✅ Email: *{text}*\n\n📱 *Passo 3/3:* Digite seu *telefone:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancelar", callback_data="main_menu")],
            ])
        )
        return

    if state == "register_phone":
        update_customer(user_id, telefone=text)
        clear_user_state(user_id)
        await update.message.reply_text(
            "✅ *Cadastro completo!*\n\nRedirecionando para o pagamento...",
            parse_mode=ParseMode.MARKDOWN
        )
        cart = get_cart(user_id)
        if cart:
            customer = get_customer(user_id)
            total = get_cart_total(user_id)

            text_checkout = "💳 *FINALIZAR COMPRA*\n\n"
            text_checkout += f"👤 *Cliente:* {customer['nome_completo']}\n"
            text_checkout += f"📧 *Email:* {customer['email']}\n\n"
            text_checkout += "🛒 *Itens do carrinho:*\n"

            for i, item in enumerate(cart, 1):
                text_checkout += f"  {i}. 🎮 {item['game_name']} - R$ {item['price']:.2f}\n"

            text_checkout += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
            text_checkout += f"💰 *TOTAL: R$ {total:.2f}*\n\n"
            text_checkout += "Selecione a forma de pagamento:"

            await update.message.reply_text(
                text_checkout, parse_mode=ParseMode.MARKDOWN,
                reply_markup=payment_keyboard()
            )
        return

    # Mensagem sem contexto - tenta buscar
    results = search_games(text)
    if results:
        await show_search_results(update, context, text, results)
    else:
        await update.message.reply_text(
            "🤔 Não entendi. Use o menu abaixo ou digite o nome de um jogo!",
            reply_markup=main_menu_keyboard()
        )


# ════════════════════════════════════════
# MAIN - Inicialização do Bot
# ════════════════════════════════════════
# ════════════════════════════════════════
# MAIN - Inicialização do Bot (Compatível Python 3.14)
# ════════════════════════════════════════

import asyncio
import sys

async def main_async():
    """Função principal assíncrona."""
    print("=" * 50)
    print("🎮 WareArcadeBot - Iniciando...")
    print("=" * 50)

    init_db()
    print("✅ Banco de dados inicializado")
    print(f"📦 {len(GAMES_CATALOG)} jogos no catálogo")

    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN não configurado!")
        print("Configure o token no arquivo .env")
        return

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(120)
        .read_timeout(120)
        .write_timeout(120)
        .pool_timeout(120)
        .get_updates_connect_timeout(120)
        .get_updates_read_timeout(120)
        .get_updates_pool_timeout(120)
        .build()
    )

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("catalogo", catalogo_command))
    app.add_handler(CommandHandler("buscar", buscar_command))
    app.add_handler(CommandHandler("ofertas", ofertas_command))
    app.add_handler(CommandHandler("carrinho", carrinho_command))
    app.add_handler(CommandHandler("pedidos", pedidos_command))
    app.add_handler(CommandHandler("perfil", perfil_command))
    app.add_handler(CommandHandler("faq", faq_command))
    app.add_handler(CommandHandler("suporte", suporte_command))
    app.add_handler(CommandHandler("admin", admin_command))

    # Callbacks (botões inline)
    app.add_handler(CallbackQueryHandler(callback_handler))

    # Fotos e Documentos (comprovantes)
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receive_proof_handler))

    # Mensagens de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Handlers registrados")
    print("🚀 Bot rodando! Pressione Ctrl+C para parar.")
    print("🤖 Bot: @WareArcadeBot")
    print("=" * 50)

    # Inicializa e roda o bot manualmente (compatível com Python 3.14)
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    # Mantém rodando até Ctrl+C
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Parando o bot...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        print("✅ Bot parado com sucesso!")


def main():
    """Wrapper que cria event loop manualmente (Python 3.14)."""
    try:
        # Cria novo event loop (compatível com Python 3.14)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main_async())
    except KeyboardInterrupt:
        print("\n🛑 Bot interrompido pelo usuário.")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()