"""
================================================================
🎮 WareArcadeBot - Bot de Vendas de Jogos para Telegram
================================================================
Bot: @WareArcadeBot
Loja: WareArcadeBot
================================================================
"""
from urllib.parse import quote
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
# COMANDOS PRINCIPAIS
# ════════════════════════════════════════

async def start(update, context):
    """Tela Inicial Humanizada com Resumo Automático."""
    user = update.effective_user
    get_or_create_customer(user.id, user.username)
    clear_user_state(user.id)
    
    total = len(GAMES_CATALOG)
    jogos = len([g for g in GAMES_CATALOG if "Jogo" in g.get("tipo", "")])
    
    welcome = (
        f"🤖 *WareArcadeBot - Nexus Digital Shop*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Olá, *{user.first_name}*! 👋 Que bom te ter aqui!\n\n"
        f"🏆 *NOSSO CATÁLOGO HOJE:*\n"
        f"🎮 Jogos PC: `{jogos} títulos`\n"
        f"💻 Softwares: `{total - jogos} licenças`\n"
        f"📦 Total: *{total} itens prontos para entrega*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 *O que você procura hoje?*"
    )

    keyboard = [
        [InlineKeyboardButton("🎮 Catálogo de Jogos", callback_data="catalog_0"),
         InlineKeyboardButton("💻 Licenças de Software", callback_data="categories")],
        [InlineKeyboardButton("🛒 Meu Carrinho", callback_data="cart"),
         InlineKeyboardButton("📦 Pedidos", callback_data="my_orders")],
        [InlineKeyboardButton("🏛️ Institucional", callback_data="menu_inst"),
         InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message: 
        await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    else: 
        await update.callback_query.edit_message_text(welcome, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


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
    """Monta teclado de catálogo paginado com botão de busca integrado."""
    total_pages = max(1, math.ceil(len(games) / ITEMS_PER_PAGE))
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_games = games[start_idx:end_idx]

    keyboard = []
    for game in page_games:
        tag = " 🔥" if game["oferta"] else ""
        price = game["preco_oferta"]
        nome = game["nome"]
        if len(nome) > 30:
            nome = nome[:30] + "..."
        btn_text = f"🎮 {nome} R${price:.2f}{tag}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"game_{game['id']}")])

    # Linha de Navegação (Paginação)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"{prefix}_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Próximo", callback_data=f"{prefix}_{page + 1}"))
    keyboard.append(nav_buttons)

    # 🔍 Botão de Busca integrado embaixo das páginas do Catálogo
    keyboard.append([InlineKeyboardButton("🔍 Buscar Produto", callback_data="search_product")])
    
    # Botão Menu Principal
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
# HANDLERS DE CALLBACK (CLIQUES) E TEXTO
# ════════════════════════════════════════

async def search_product_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Acionado ao clicar em '🔍 Buscar Produto'."""
    query = update.callback_query
    try: await query.answer()
    except: pass
    
    user_id = query.from_user.id
    set_user_state(user_id, "AWAITING_SEARCH")
    
    await query.message.reply_text(
        "🔍 *Busca de Produtos*\n\n"
        "Digite abaixo o nome do jogo ou software que você deseja procurar:",
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gerencia a entrada de texto do usuário (Captura a Busca)."""
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    text = update.message.text

    if state == "AWAITING_SEARCH":
        clear_user_state(user_id)
        results = search_games(text) # Executa o filtro de busca do catálogo
        
        if not results:
            await update.message.reply_text(
                f"❌ Nenhum produto encontrado para: *{text}*\n"
                "Tente buscar usando outra palavra-chave.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=back_to_menu_keyboard()
            )
            return

        await update.message.reply_text(
            f"🔍 *Resultados para:* '{text}'\n"
            f"Encontramos {len(results)} item(ns):",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=catalog_keyboard(0, results, prefix="search_res")
        )
    else:
        # Se não estiver buscando, pode mandar a mensagem padrão do fluxo normal
        pass


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gerenciador central de cliques do Bot."""
    query = update.callback_query
    try: 
        await query.answer()
    except Exception: 
        pass
    
    data = query.data
    user_id = query.from_user.id

    # 1. Rota: Menu Principal
    if data == "main_menu":
        await start(update, context)

    # 2. Rota: Catálogo de Jogos (Paginação)
    elif data.startswith("catalog_"):
        page = int(data.split("_")[1])
        await query.edit_message_text(
            "🎮 *CATÁLOGO DE JOGOS PARA PC*\n\nSelecione um jogo para ver detalhes:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=catalog_keyboard(page, GAMES_CATALOG)
        )

    # 3. Rota: Licenças de Software (Categorias)
    elif data == "categories":
        keyboard = []
        for i in range(0, len(CATEGORIES), 2):
            row = [InlineKeyboardButton(CATEGORIES[i], callback_data=f"category_{CATEGORIES[i]}")]
            if i + 1 < len(CATEGORIES):
                row.append(InlineKeyboardButton(CATEGORIES[i+1], callback_data=f"category_{CATEGORIES[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])
        
        await query.edit_message_text(
            "💻 *LICENÇAS DE SOFTWARE & CATEGORIAS*\n\nEscolha uma categoria para explorar:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 4. Rota: Filtro por Categoria específica
    elif data.startswith("category_"):
        cat_name = data.replace("category_", "")
        filtered_games = [g for g in GAMES_CATALOG if cat_name in g.get("categorias", [])]
        await query.edit_message_text(
            f"📦 *PRODUTOS EM: {cat_name.upper()}*\n\nSelecione uma opção:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=catalog_keyboard(0, filtered_games, prefix=f"catfilter_{cat_name}")
        )

    # 5. Rota: Meu Carrinho
    elif data == "cart":
        cart_items = get_cart(user_id)
        if not cart_items:
            await query.edit_message_text(
                "🛒 *Meu Carrinho*\n\nSeu carrinho está vazio no momento. Que tal dar uma olhada no nosso catálogo?",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0")], [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]])
            )
            return
            
        total_cart = get_cart_total(user_id)
        text = "🛒 *SEU CARRINHO DE COMPRAS:*\n━━━━━━━━━━━━━━━━━━━━━━\n"
        keyboard = []
        for item in cart_items:
            text += f"• *{item['nome']}* - R${item['preco_oferta']:.2f}\n"
            keyboard.append([InlineKeyboardButton(f"❌ Remover {item['nome'][:15]}...", callback_data=f"remove_{item['id']}")])
            
        text += f"━━━━━━━━━━━━━━━━━━━━━━\n💰 *Total:* R${total_cart:.2f}"
        keyboard.append([InlineKeyboardButton("💰 Ir para o Pagamento", callback_data="checkout")])
        keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

    # 6. Rota: Pedidos
    elif data == "my_orders":
        orders = get_customer_orders(user_id)
        if not orders:
            await query.edit_message_text(
                "📦 *Meus Pedidos*\n\nVocê ainda não realizou nenhum pedido no nosso sistema.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=back_to_menu_keyboard()
            )
            return
            
        text = "📦 *SEUS PEDIDOS RECENTES:*\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for o in orders[:5]:
            text += f"🔑 *Código:* `{o['id']}`\n💰 *Valor:* R${o['total']:.2f}\n🚦 *Status:* {o['status']}\n──────────────────\n"
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu_keyboard())

    # 7. Rota: Institucional
    elif data == "menu_inst":
        text = (
            "🏛️ *INSTITUCIONAL - WareArcadeBot*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Segurança, agilidade e total transparência para sua compra digital.\n\n"
            "🛡️ *Garantia Nexus*: Todos os nossos softwares e jogos possuem chaves de ativação digitais válidas e suporte dedicado pós-venda."
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")]
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))

    # 8. Rota: Suporte (Link Direto WhatsApp)
       
    elif data == "support":
        text = (
            "📞 *SUPORTE AO CLIENTE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Precisa de ajuda com a instalação, chaves ou pagamento?\n\n"
            "🕒 *Horário:* Seg a Sex: 9h-19h | Sáb: 9h-14h\n"
            "💬 Clique no botão abaixo para falar direto conosco pelo WhatsApp!"
        )
        
        # Texto unificado em uma única string limpa para evitar falhas de concatenação
        mensagem_suporte = (
            "👋 Olá! Seja bem-vindo ao Suporte da Ware Arcade.\n\n"
            "Obrigado por entrar em contato! 😊\n\n"
            "Como podemos ajudar você hoje?\n\n"
            "Escolha uma das opções abaixo ou descreva sua necessidade:\n\n"
            "🛒 1. Informações sobre compra\n"
            "💳 2. Pagamento ou pedido não aprovado\n"
            "❌ 3. Venda cancelada\n"
            "📦 4. Pós-venda\n"
            "⬇️ 5. Dúvidas sobre download\n"
            "🔑 6. Data de expiração do download\n"
            "🔄 7. Renovação ou novo link de download\n"
            "🛠️ 8. Problemas técnicos ou instalação\n"
            "📱 9. Compatibilidade com dispositivos\n"
            "👤 10. Minha conta ou acesso\n"
            "💡 11. Outras dúvidas ou suporte geral\n\n"
            "Nossa equipe responderá assim que possível. Informe o número do seu pedido, se houver, para agilizar o atendimento."
        )

        # Codifica o texto garantindo compatibilidade total com navegadores e Telegram
        texto_codificado = quote(mensagem_suporte)

        keyboard = [
            [
                InlineKeyboardButton(
                    "💬 Falar com o Suporte Ware Arcade",
                    url=f"https://whatsapp.com{texto_codificado}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Menu Principal",
                    callback_data="main_menu"
                )
            ]
        ]
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(keyboard))


async def main_async():
    """Inicializa e roda o bot e seus handlers de forma assincrona."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 1. Comando principal /start
    app.add_handler(CommandHandler("start", start))

    # 2. Handler do Botao de Busca por clique
    app.add_handler(CallbackQueryHandler(search_product_click, pattern="^search_product$"))

    # 3. Handler do clique geral dos outros botoes (Menu, Catalogo, etc)
    app.add_handler(CallbackQueryHandler(button))

    # 4. Handler de entrada de texto (Captura o que o usuario digitou para buscar)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("==================================================")
    print("🎮 WareArcadeBot - Iniciando...")
    print("==================================================")
    print("✅ Banco de dados inicializado")
    print("📦 Catálogo carregado com sucesso")
    print("🚀 Bot rodando! Pressione Ctrl+C para parar.")
    print("==================================================")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    import asyncio
    while True:
        await asyncio.sleep(3600)

def main():
    """Ponto de entrada principal do script."""
    import asyncio
    try:
        asyncio.run(main_async())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot finalizado pelo administrador.")

if __name__ == "__main__":
    main()
