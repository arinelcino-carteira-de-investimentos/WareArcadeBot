"""
================================================================
🎮 WareArcadeBot - Bot de Vendas de Jogos para Telegram
================================================================
Bot: @WareArcadeBot
Versão: 3.0 - Completa e Unificada
================================================================
"""

import logging
import math
import asyncio
import time
import re
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

from config import (
    TELEGRAM_BOT_TOKEN, ITEMS_PER_PAGE, PAYMENT_METHODS,
    STORE_NAME, STORE_WEBSITE, STORE_EMAIL, STORE_INSTAGRAM,
    STORE_HOURS, STORE_WHATSAPP, DOWNLOAD_LINK_EXPIRY_HOURS, ADMIN_CHAT_IDS,
    PIX_CHAVE, PIX_NOME, PIX_CIDADE
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
    get_pending_orders
)
from email_sender import send_purchase_email, send_multiple_purchase_email
from qrcode_pix import enviar_qrcode_pix

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
    jogos = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎮 Jogo"])
    sistemas = len([g for g in GAMES_CATALOG if g.get("tipo") == "🖥️ Sistema"])
    office = len([g for g in GAMES_CATALOG if g.get("tipo") == "📄 Office"])
    design = len([g for g in GAMES_CATALOG if g.get("tipo") in ["🎨 Design", "🎬 Vídeo"]])
    engenharia = len([g for g in GAMES_CATALOG if g.get("tipo") == "🏗️ Engenharia"])
    antivirus = len([g for g in GAMES_CATALOG if g.get("tipo") == "🔒 Segurança"])
    ferramentas = len([g for g in GAMES_CATALOG if g.get("tipo") == "🛠️ Ferramenta"])
    streaming = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎬 Streaming"])
    musica = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎵 Música"])
    giftcards = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎁 Gift Card"])
    cloud = len([g for g in GAMES_CATALOG if g.get("tipo") == "☁️ Cloud"])
    cursos = len([g for g in GAMES_CATALOG if g.get("tipo") == "🎓 Curso"])
    ofertas = len([g for g in GAMES_CATALOG if g["oferta"]])

    precos = [g["preco_oferta"] for g in GAMES_CATALOG]
    preco_min = min(precos) if precos else 0
    preco_max = max(precos) if precos else 0

    welcome = (
        f"🎮💻 *{STORE_NAME}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Olá, *{user.first_name}*! 👋\n\n"
        f"🏆 *CATÁLOGO COMPLETO - {total} PRODUTOS*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎮 Jogos PC ............... `{jogos:>3}`\n"
        f"🖥️ Sistemas Operacionais .. `{sistemas:>3}`\n"
        f"📄 Microsoft Office ....... `{office:>3}`\n"
        f"🎨 Adobe/Design ........... `{design:>3}`\n"
        f"🏗️ Engenharia/3D .......... `{engenharia:>3}`\n"
        f"🔒 Antivírus .............. `{antivirus:>3}`\n"
        f"🛠️ Ferramentas ............ `{ferramentas:>3}`\n"
        f"🎬 Streaming .............. `{streaming:>3}`\n"
        f"🎵 Música ................. `{musica:>3}`\n"
        f"🎁 Gift Cards ............. `{giftcards:>3}`\n"
        f"☁️ Cloud Storage .......... `{cloud:>3}`\n"
        f"🎓 Cursos ................. `{cursos:>3}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📊 *INFORMAÇÕES:*\n"
        f"• 📦 Total: *{total} produtos*\n"
        f"• 🔥 Em oferta: *{ofertas} produtos*\n"
        f"• 💰 Faixa: *R$ {preco_min:.2f}* a *R$ {preco_max:.2f}*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ Entrega imediata | 🔒 100% Seguro\n"
        f"💚 PIX | 💳 Cartão | 📄 Boleto\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
        [InlineKeyboardButton("🏛️ Institucional", callback_data="institutional"),
         InlineKeyboardButton("📞 Suporte", callback_data="support")],
    ]

    if update.message:
        await update.message.reply_text(
            welcome, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            welcome, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ════════════════════════════════════════
# MENU INSTITUCIONAL
# ════════════════════════════════════════

async def show_institutional(update, context):
    """Menu Institucional completo."""
    text = (
        "🏛️ *INSTITUCIONAL - WareArcadeBot*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Conheça nossa loja e políticas.\n"
        "Sua segurança é prioridade!\n\n"
        "*Escolha uma opção:*"
    )
    
    keyboard = [
        [InlineKeyboardButton("📖 Sobre Nós", callback_data="inst_sobre"),
         InlineKeyboardButton("🎯 Missão", callback_data="inst_missao")],
        [InlineKeyboardButton("🔒 Privacidade", callback_data="inst_privacidade"),
         InlineKeyboardButton("📜 Termos de Uso", callback_data="inst_termos")],
        [InlineKeyboardButton("🚚 Política de Entrega", callback_data="inst_entrega"),
         InlineKeyboardButton("💰 Reembolso", callback_data="inst_reembolso")],
        [InlineKeyboardButton("🛡️ Garantias", callback_data="inst_garantia"),
         InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]
    
    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def institutional_detail(update, context, page):
    """Páginas detalhadas do institucional."""
    paginas = {
        "sobre": (
            "📖 *SOBRE NÓS - WareArcadeBot*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Somos a *maior loja digital* do Telegram! 🚀\n\n"
            "🎮 92+ jogos PC originais\n"
            "🖥️ Sistemas operacionais\n"
            "📄 Microsoft Office completo\n"
            "🎨 Adobe Creative Cloud\n"
            "🏗️ AutoCAD, SketchUp, Revit\n"
            "🔒 Antivírus premium\n"
            "🛠️ Ferramentas profissionais\n"
            "🎬 Streaming (Netflix, Disney+)\n"
            "🎵 Spotify, YouTube Premium\n"
            "🎁 Gift Cards (Steam, PSN, Xbox)\n"
            "☁️ Cloud (Google, iCloud, Dropbox)\n"
            "🎓 Cursos online completos\n\n"
            "🏆 *DIFERENCIAIS:*\n"
            "⚡ Entrega 100% imediata\n"
            "💰 Os menores preços do Brasil\n"
            "🔒 Pagamento via PIX/Cartão\n"
            "📞 Suporte humano via WhatsApp\n"
            "✅ +2.500 clientes satisfeitos"
        ),
        "missao": (
            "🎯 *NOSSA MISSÃO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*MISSÃO:*\n"
            "Democratizar o acesso a softwares e jogos\n"
            "premium com preços justos e entrega imediata.\n\n"
            "*VISÃO:*\n"
            "Ser a maior loja digital do Telegram BR até 2026.\n\n"
            "*VALORES:*\n"
            "✅ Honestidade nos preços\n"
            "✅ Entrega rápida e segura\n"
            "✅ Atendimento humanizado\n"
            "✅ Produtos 100% originais\n"
            "✅ Suporte pós-venda completo"
        ),
        "privacidade": (
            "🔒 *POLÍTICA DE PRIVACIDADE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Seus dados são *protegidos* por nós!\n\n"
            "1️⃣ Coletamos apenas o necessário:\n"
            "   nome, email e telefone.\n\n"
            "2️⃣ NUNCA armazenamos dados de cartão.\n\n"
            "3️⃣ NUNCA compartilhamos com terceiros.\n\n"
            "4️⃣ Você pode pedir exclusão a qualquer\n"
            "   momento pelo suporte.\n\n"
            "5️⃣ Pagamentos processados por gateways\n"
            "   seguros (PIX, Mercado Pago).\n\n"
            "6️⃣ Cumprimos a LGPD integralmente."
        ),
        "termos": (
            "📜 *TERMOS DE USO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ao comprar conosco, você concorda:\n\n"
            "1️⃣ Produtos são digitais e entregues\n"
            "   após confirmação do pagamento.\n\n"
            "2️⃣ Links válidos por 48 horas.\n\n"
            "3️⃣ Uso *pessoal* apenas.\n"
            "   Proibida redistribuição.\n\n"
            "4️⃣ Oferecemos suporte para ativação\n"
            "   e instalação por 30 dias.\n\n"
            "5️⃣ Não nos responsabilizamos por\n"
            "   incompatibilidade do hardware.\n\n"
            "6️⃣ Reembolso conforme nossa política."
        ),
        "entrega": (
            "🚚 *POLÍTICA DE ENTREGA*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Como funciona:*\n\n"
            "1️⃣ Você escolhe o produto\n"
            "2️⃣ Adiciona ao carrinho\n"
            "3️⃣ Faz o pagamento\n"
            "4️⃣ Envia o comprovante\n"
            "5️⃣ Após aprovação, recebe:\n"
            "   📱 Link aqui no Telegram\n"
            "   📧 Link por email\n\n"
            "*Tempo médio:*\n"
            "⚡ PIX: 5 a 30 minutos\n"
            "💳 Cartão: 5 a 15 minutos\n"
            "🏦 TED: 1 a 4 horas úteis\n"
            "📄 Boleto: 1 a 3 dias úteis\n\n"
            "_*Entrega garantida em 100% dos casos!*_"
        ),
        "reembolso": (
            "💰 *POLÍTICA DE REEMBOLSO*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Você está seguro conosco!*\n\n"
            "✅ *7 dias de garantia* (CDC)\n\n"
            "1️⃣ Arrependimento: reembolso em 7 dias\n"
            "   ANTES de baixar/ativar o produto.\n\n"
            "2️⃣ Problema técnico: substituição ou\n"
            "   reembolso integral.\n\n"
            "3️⃣ Após download/ativação:\n"
            "   reembolso não se aplica.\n\n"
            "4️⃣ Produto errado: reembolso 100%.\n\n"
            "*Como solicitar:*\n"
            "Entre em contato com nosso suporte\n"
            "pelo Telegram ou WhatsApp."
        ),
        "garantia": (
            "🛡️ *NOSSAS GARANTIAS*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔒 *PRODUTO ORIGINAL*\n"
            "Todos são licenciados e verificados.\n\n"
            "⚡ *ENTREGA IMEDIATA*\n"
            "Após pagamento, você recebe na hora.\n\n"
            "💚 *SUPORTE HUMANIZADO*\n"
            "Atendimento real, sem robôs chatos.\n\n"
            "🔄 *TROCA GARANTIDA*\n"
            "Se não funcionar, trocamos sem custo.\n\n"
            "🎯 *MELHOR PREÇO*\n"
            "Achou mais barato? Cobrimos a oferta!\n\n"
            "✅ *+2.500 CLIENTES SATISFEITOS*\n"
            "Avaliação 5 estrelas em todas redes!"
        ),
    }

    texto = paginas.get(page, "Página não encontrada.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Voltar", callback_data="institutional")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    
    await update.callback_query.edit_message_text(
        texto, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
    )


async def show_support(update, context):
    """Exibe informações de suporte."""
    whatsapp_clean = "".join(filter(str.isdigit, STORE_WHATSAPP))
    if whatsapp_clean and not whatsapp_clean.startswith("55"):
        whatsapp_clean = "55" + whatsapp_clean

    ig_clean = STORE_INSTAGRAM.replace("@", "").replace(" ", "")

    text = (
        f"📞 *SUPORTE AO CLIENTE*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏪 *{STORE_NAME}*\n\n"
        f"💬 *Fale conosco:*\n\n"
        f"📱 *WhatsApp:* {STORE_WHATSAPP}\n"
        f"📧 *Email:* {STORE_EMAIL}\n"
        f"📸 *Instagram:* {STORE_INSTAGRAM}\n"
        f"⏰ *Horário:* {STORE_HOURS}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💚 *Atendimento humanizado!*\n"
        f"Respondemos em até 30 minutos."
    )

    keyboard = []
    if whatsapp_clean and len(whatsapp_clean) >= 12:
        keyboard.append([InlineKeyboardButton("📱 Chamar no WhatsApp", url=f"https://wa.me/{whatsapp_clean}")])
    if ig_clean:
        keyboard.append([InlineKeyboardButton("📸 Seguir no Instagram", url=f"https://instagram.com/{ig_clean}")])
    keyboard.append([InlineKeyboardButton("❓ FAQ", callback_data="faq")])
    keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_faq(update, context):
    """Exibe perguntas frequentes."""
    text = (
        "❓ *PERGUNTAS FREQUENTES (FAQ)*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔹 *Como funciona a compra?*\n"
        "1. Escolha o produto\n"
        "2. Adicione ao carrinho\n"
        "3. Finalize e escolha o pagamento\n"
        "4. Envie o comprovante\n"
        "5. Receba o link de download\n\n"
        "🔹 *Quais formas de pagamento?*\n"
        "✅ PIX (aprovado em minutos)\n"
        "✅ Cartão de Crédito\n"
        "✅ Transferência (TED)\n"
        "✅ Boleto Bancário\n\n"
        "🔹 *Recebo o produto como?*\n"
        "📱 Por aqui no Telegram\n"
        "📧 Por email (link de download)\n\n"
        "🔹 *E se o download não funcionar?*\n"
        "Entre em contato pelo suporte que resolvemos!\n\n"
        "🔹 *Os produtos são originais?*\n"
        "✅ Sim! Todos são licenciados e garantidos.\n\n"
        "🔹 *Tenho direito a reembolso?*\n"
        "Sim, em até 7 dias antes do download.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💚 *Ainda tem dúvidas? Fale conosco!*"
    )

    keyboard = [
        [InlineKeyboardButton("📞 Falar com Suporte", callback_data="support")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ════════════════════════════════════════
# CATÁLOGO E BUSCA
# ════════════════════════════════════════

async def catalog(update, context, page=0):
    """Exibe o catálogo paginado."""
    await update.callback_query.edit_message_text(
        "🎮 *CATÁLOGO DE JOGOS E SOFTWARES*\n\nSelecione um produto para ver detalhes:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=catalog_keyboard(page, GAMES_CATALOG)
    )


async def show_offers(update, context, page=0):
    """Exibe produtos em oferta."""
    offers = get_offers()
    if not offers:
        await update.callback_query.edit_message_text(
            "🔥 *Ofertas*\n\nNenhum produto em oferta no momento.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_menu_keyboard()
        )
        return
    
    await update.callback_query.edit_message_text(
        "🔥 *OFERTAS IMPERDÍVEIS!*\n\nConfira os produtos com desconto:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=catalog_keyboard(page, offers, prefix="offers")
    )


async def show_categories(update, context):
    """Exibe todas as categorias."""
    contagem = {
        "🎮 Jogo": 0, "🖥️ Sistema": 0, "📄 Office": 0, "🎨 Design": 0,
        "🏗️ Engenharia": 0, "🔒 Segurança": 0, "🛠️ Ferramenta": 0,
        "🎬 Streaming": 0, "🎵 Música": 0, "🎁 Gift Card": 0,
        "☁️ Cloud": 0, "🎓 Curso": 0,
    }
    for g in GAMES_CATALOG:
        tipo = g.get("tipo", "🎮 Jogo")
        if tipo in contagem:
            contagem[tipo] += 1

    design_total = contagem["🎨 Design"] + contagem.get("🎬 Vídeo", 0)

    text = (
        f"🏷️ *CATEGORIAS*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 *{len(GAMES_CATALOG)} produtos* disponíveis\n\n"
        f"*Escolha uma categoria:*"
    )

    keyboard = [
        [InlineKeyboardButton(f"🎮 Jogos PC ({contagem['🎮 Jogo']})", callback_data="cat_tipo_🎮 Jogo")],
        [InlineKeyboardButton(f"🖥️ Sistemas ({contagem['🖥️ Sistema']})", callback_data="cat_tipo_🖥️ Sistema"),
         InlineKeyboardButton(f"📄 Office ({contagem['📄 Office']})", callback_data="cat_tipo_📄 Office")],
        [InlineKeyboardButton(f"🎨 Design ({design_total})", callback_data="cat_tipo_🎨 Design"),
         InlineKeyboardButton(f"🏗️ Engenharia ({contagem['🏗️ Engenharia']})", callback_data="cat_tipo_🏗️ Engenharia")],
        [InlineKeyboardButton(f"🔒 Antivírus ({contagem['🔒 Segurança']})", callback_data="cat_tipo_🔒 Segurança"),
         InlineKeyboardButton(f"🛠️ Ferramentas ({contagem['🛠️ Ferramenta']})", callback_data="cat_tipo_🛠️ Ferramenta")],
        [InlineKeyboardButton(f"🎬 Streaming ({contagem['🎬 Streaming']})", callback_data="cat_tipo_🎬 Streaming"),
         InlineKeyboardButton(f"🎵 Música ({contagem['🎵 Música']})", callback_data="cat_tipo_🎵 Música")],
        [InlineKeyboardButton(f"🎁 Gift Cards ({contagem['🎁 Gift Card']})", callback_data="cat_tipo_🎁 Gift Card"),
         InlineKeyboardButton(f"☁️ Cloud ({contagem['☁️ Cloud']})", callback_data="cat_tipo_☁️ Cloud")],
        [InlineKeyboardButton(f"🎓 Cursos ({contagem['🎓 Curso']})", callback_data="cat_tipo_🎓 Curso")],
        [InlineKeyboardButton("🔥 Ofertas", callback_data="offers_0"),
         InlineKeyboardButton("🔍 Buscar", callback_data="search")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ]

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_category_by_type(update, context, tipo, page=0):
    """Exibe produtos de um tipo específico."""
    if tipo == "🎨 Design":
        produtos = [g for g in GAMES_CATALOG if g.get("tipo") in ["🎨 Design", "🎬 Vídeo"]]
    else:
        produtos = [g for g in GAMES_CATALOG if g.get("tipo") == tipo]

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
    total_pages = max(1, math.ceil(len(produtos) / ITEMS_PER_PAGE))

    text = (
        f"{tipo} *{nome_cat}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 {len(produtos)} produtos | 📄 Página {page + 1} de {total_pages}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"_Toque em um produto para ver detalhes:_"
    )

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=catalog_keyboard(page, produtos, f"tipopage_{tipo}")
    )


async def handle_user_message(update, context):
    """Gerencia a entrada de texto do usuário (Captura a Busca)."""
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)
    text = update.message.text

    if state == "AWAITING_SEARCH":
        clear_user_state(user_id)
        results = search_games(text)
        
        # Salva os resultados no contexto para paginação
        context.user_data["last_search_results"] = results
        
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


async def show_game_detail(update, context, game_id):
    """Exibe detalhes de um produto."""
    game = get_game_by_id(game_id)
    if not game:
        await update.callback_query.answer("Produto não encontrado!", show_alert=True)
        return

    nome = game["nome"].replace("*", "").replace("_", "").replace("`", "")
    desc = game.get("descricao", "")[:300]
    preco = game["preco_oferta"]
    preco_orig = game.get("preco_original", preco)

    if game.get("oferta") and preco_orig != preco:
        preco_text = f"De R$ {preco_orig:.2f} por R$ {preco:.2f}"
        desconto = int((1 - preco / preco_orig) * 100)
        preco_text += f" ({desconto}% OFF)"
    else:
        preco_text = f"R$ {preco:.2f}"

    text = f"""
🎮 *{nome}*

💰 {preco_text}
🖥️ Plataforma: {game.get('plataforma', 'PC')}
🏷️ Categorias: {', '.join(game.get('categorias', []))}

📝 {desc}

━━━━━━━━━━━━━━━━━━━━━━
✅ Entrega digital imediata
🔒 Pagamento 100% seguro
📧 Link válido por 48h
"""

    try:
        await update.callback_query.message.delete()
    except Exception:
        pass

    imagem_url = game.get("imagem_url", "")
    if imagem_url and imagem_url.startswith("http"):
        try:
            await context.bot.send_photo(
                chat_id=update.callback_query.message.chat_id,
                photo=imagem_url,
                caption=text,
                reply_markup=game_detail_keyboard(game_id)
            )
            return
        except Exception as e:
            logger.warning(f"Imagem falhou: {e}")

    await context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text=text,
        reply_markup=game_detail_keyboard(game_id)
    )


# ════════════════════════════════════════
# CARRINHO E CHECKOUT
# ════════════════════════════════════════

async def show_cart(update, context):
    """Exibe o carrinho do usuário."""
    user_id = update.callback_query.from_user.id
    cart_items = get_cart(user_id)

    if not cart_items:
        await update.callback_query.edit_message_text(
            "🛒 *Meu Carrinho*\n\nSeu carrinho está vazio. Que tal dar uma olhada no catálogo?",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎮 Ver Catálogo", callback_data="catalog_0")],
                [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]
            ])
        )
        return

    total = get_cart_total(user_id)
    text = "🛒 *SEU CARRINHO*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    keyboard = []

    for i, item in enumerate(cart_items, 1):
        nome = item["game_name"].replace("*", "").replace("_", "")
        text += f"{i}. {nome} - R$ {item['price']:.2f}\n"
        keyboard.append([InlineKeyboardButton(f"❌ Remover #{i}", callback_data=f"remove_{item['id']}")])

    text += f"\n━━━━━━━━━━━━━━━━━━━━━━\n💰 *Total: R$ {total:.2f}*\n"

    keyboard.append([InlineKeyboardButton("💰 Finalizar Compra", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")])

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def add_to_cart(update, context, game_id):
    """Adiciona um produto ao carrinho."""
    user_id = update.callback_query.from_user.id
    game = get_game_by_id(game_id)

    if not game:
        await update.callback_query.answer("Produto não encontrado!")
        return

    add_to_cart(user_id, game_id, game["nome"], game["preco_oferta"])
    await update.callback_query.answer(f"✅ {game['nome']} adicionado ao carrinho!", show_alert=False)

    await update.callback_query.edit_message_text(
        f"🛒 *Item adicionado!*\n\n"
        f"✅ {game['nome']} foi adicionado ao seu carrinho.\n\n"
        f"💰 Valor: R$ {game['preco_oferta']:.2f}\n\n"
        f"O que deseja fazer agora?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Ver Carrinho", callback_data="cart")],
            [InlineKeyboardButton("🎮 Continuar Comprando", callback_data="catalog_0")],
            [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
        ])
    )


async def buy_now(update, context, game_id):
    """Compra direta de um produto."""
    user_id = update.callback_query.from_user.id
    game = get_game_by_id(game_id)

    if not game:
        await update.callback_query.answer("Produto não encontrado!", show_alert=True)
        return

    clear_cart(user_id)
    add_to_cart(user_id, game_id, game["nome"], game["preco_oferta"])

    if not is_customer_complete(user_id):
        await start_registration(update, context, "checkout")
        return

    await start_checkout(update, context)


async def start_checkout(update, context):
    """Inicia o processo de checkout."""
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)

    if not cart:
        await update.callback_query.answer("Carrinho vazio!", show_alert=True)
        return

    if not is_customer_complete(user_id):
        await start_registration(update, context, "checkout")
        return

    customer = get_customer(user_id)
    total = get_cart_total(user_id)

    text = (
        f"💳 *FINALIZAR COMPRA*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 *Cliente:* {customer.get('nome_completo', 'Cliente')}\n"
        f"📧 *Email:* {customer.get('email', '')}\n"
        f"📱 *Telefone:* {customer.get('telefone', '')}\n\n"
        f"📦 *Itens:*\n"
    )

    for item in cart:
        nome = item["game_name"].replace("*", "").replace("_", "")
        text += f"  🎮 {nome} - R$ {item['price']:.2f}\n"

    text += (
        f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *TOTAL: R$ {total:.2f}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*Selecione a forma de pagamento:*"
    )

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=payment_keyboard()
    )


async def process_payment(update, context, method):
    """Processa o pagamento selecionado."""
    user_id = update.callback_query.from_user.id
    cart = get_cart(user_id)
    total = get_cart_total(user_id)

    if not cart:
        await update.callback_query.answer("Carrinho vazio!", show_alert=True)
        return

    # Cria os pedidos
    orders = create_orders_from_cart(user_id, method)

    if not orders:
        await update.callback_query.edit_message_text(
            "❌ Erro ao processar pedido. Tente novamente.",
            reply_markup=back_to_menu_keyboard()
        )
        return

    order_codes = [o["order_code"] for o in orders]
    context.user_data["pending_orders"] = order_codes

    if method == "pix":
        text = (
            f"💚 *PAGAMENTO VIA PIX*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 *Valor: R$ {total:.2f}*\n\n"
            f"📋 *Código do Pedido:*\n"
        )
        for o in orders:
            text += f"  `{o['order_code']}`\n"

        text += (
            f"\n📱 *Chave PIX (Celular):*\n"
            f"`{PIX_CHAVE}`\n\n"
            f"👤 *Nome:* {PIX_NOME}\n\n"
            f"📲 *Como pagar:*\n"
            f"1️⃣ Abra o app do seu banco\n"
            f"2️⃣ Escolha PIX → Copiar e Colar\n"
            f"3️⃣ Use a chave acima ou leia o QR Code\n"
            f"4️⃣ Pague o valor de *R$ {total:.2f}*\n"
            f"5️⃣ Envie o *comprovante* aqui no chat\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏳ *Aguardando pagamento...*"
        )

        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=confirm_purchase_keyboard()
        )

        # Envia QR Code
        try:
            await enviar_qrcode_pix(
                context=context,
                chat_id=update.callback_query.message.chat_id,
                valor=total,
                txid=f"WA{user_id}"
            )
        except Exception as e:
            logger.warning(f"QR Code não gerado: {e}")

        set_user_state(user_id, "AWAITING_PROOF", {"order_codes": order_codes})

    else:
        text = (
            f"💳 *OUTRAS FORMAS DE PAGAMENTO*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 *Total: R$ {total:.2f}*\n\n"
            f"📋 *Código do Pedido:*\n"
        )
        for o in orders:
            text += f"  `{o['order_code']}`\n"

        text += (
            f"\n📝 *Como finalizar:*\n"
            f"1️⃣ Faça o pagamento conforme as instruções abaixo\n"
            f"2️⃣ Envie o comprovante aqui no chat\n\n"
            f"💚 *Pagamento via Cartão / TED:*\n"
            f"Entre em contato pelo suporte para informações."
        )

        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📞 Suporte", callback_data="support")],
                [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]
            ])
        )

        set_user_state(user_id, "AWAITING_PROOF", {"order_codes": order_codes})


# ════════════════════════════════════════
# CADASTRO E PEDIDOS
# ════════════════════════════════════════

async def start_registration(update, context, redirect_to=None):
    """Inicia o cadastro do usuário."""
    user_id = update.callback_query.from_user.id
    set_user_state(user_id, "REGISTERING", {"redirect": redirect_to})

    text = (
        "📝 *CADASTRO NECESSÁRIO*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Para finalizar sua compra, precisamos de alguns dados.\n\n"
        "🔒 *Seus dados estão seguros!*\n"
        "✅ Não armazenamos dados de cartão\n"
        "✅ Protegidos pela LGPD\n\n"
        "*Digite seu nome completo:*"
    )

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN
    )


async def handle_registration(update, context):
    """Processa as respostas do cadastro."""
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)
    text = update.message.text

    if state == "REGISTERING":
        if "nome" not in data:
            update_customer(user_id, nome_completo=text)
            data["nome"] = text
            set_user_state(user_id, "REGISTERING", data)
            await update.message.reply_text(
                f"✅ Nome salvo: *{text}*\n\n📧 Agora digite seu *email*:",
                parse_mode=ParseMode.MARKDOWN
            )
        elif "email" not in data:
            if "@" not in text:
                await update.message.reply_text("❌ Email inválido. Digite um email válido:")
                return
            update_customer(user_id, email=text)
            data["email"] = text
            set_user_state(user_id, "REGISTERING", data)
            await update.message.reply_text(
                f"✅ Email salvo: *{text}*\n\n📱 Agora digite seu *telefone* (com DDD):",
                parse_mode=ParseMode.MARKDOWN
            )
        elif "telefone" not in data:
            telefone_clean = "".join(filter(str.isdigit, text))
            if len(telefone_clean) < 10:
                await update.message.reply_text("❌ Telefone inválido. Digite com DDD (ex: 11999999999):")
                return
            update_customer(user_id, telefone=telefone_clean)
            clear_user_state(user_id)

            await update.message.reply_text(
                f"✅ Cadastro completo!\n\n"
                f"📛 Nome: {data.get('nome')}\n"
                f"📧 Email: {data.get('email')}\n"
                f"📱 Telefone: {telefone_clean}\n\n"
                "🔒 Seus dados estão seguros conosco!\n\n"
                "Agora vamos finalizar sua compra! 🚀"
            )

            redirect = data.get("redirect")
            if redirect == "checkout":
                await start_checkout_direct(update, context)
            else:
                await start(update, context)


async def start_checkout_direct(update, context):
    """Inicia checkout diretamente (sem callback)."""
    user_id = update.effective_user.id
    cart = get_cart(user_id)

    if not cart:
        await update.message.reply_text("🛒 Carrinho vazio!", reply_markup=back_to_menu_keyboard())
        return

    if not is_customer_complete(user_id):
        await start_registration(update, context, "checkout")
        return

    customer = get_customer(user_id)
    total = get_cart_total(user_id)

    text = (
        f"💳 *FINALIZAR COMPRA*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 *Cliente:* {customer.get('nome_completo', 'Cliente')}\n"
        f"📧 *Email:* {customer.get('email', '')}\n"
        f"📱 *Telefone:* {customer.get('telefone', '')}\n\n"
        f"📦 *Itens:*\n"
    )

    for item in cart:
        nome = item["game_name"].replace("*", "").replace("_", "")
        text += f"  🎮 {nome} - R$ {item['price']:.2f}\n"

    text += (
        f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *TOTAL: R$ {total:.2f}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*Selecione a forma de pagamento:*"
    )

    await update.message.reply_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=payment_keyboard()
    )


async def show_orders(update, context):
    """Exibe os pedidos do usuário."""
    user_id = update.callback_query.from_user.id
    orders = get_customer_orders(user_id)

    if not orders:
        await update.callback_query.edit_message_text(
            "📦 *Meus Pedidos*\n\nVocê ainda não realizou nenhum pedido.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_menu_keyboard()
        )
        return

    text = "📦 *MEUS PEDIDOS*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    status_emoji = {
        "pendente": "⏳",
        "confirmado": "✅",
        "aprovado": "✅",
        "rejeitado": "❌",
        "aguardando_aprovacao": "⏳"
    }

    for o in orders[:5]:
        emoji = status_emoji.get(o["status"], "📦")
        text += f"{emoji} *Código:* `{o['order_code']}`\n"
        text += f"🎮 {o['game_name']}\n"
        text += f"💰 R$ {o['price']:.2f} | {o['status'].upper()}\n"
        text += f"📅 {o['created_at'][:10]}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━\n"

    if len(orders) > 5:
        text += f"\n_+{len(orders) - 5} pedidos anteriores_"

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard()
    )


async def show_profile(update, context):
    """Exibe o perfil do usuário."""
    user_id = update.callback_query.from_user.id
    customer = get_customer(user_id)

    if not customer:
        await update.callback_query.answer("Erro ao carregar dados.")
        return

    text = (
        f"👤 *MEU CADASTRO*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📛 Nome: {customer.get('nome_completo', 'Não informado')}\n"
        f"📧 Email: {customer.get('email', 'Não informado')}\n"
        f"📱 Telefone: {customer.get('telefone', 'Não informado')}\n"
        f"🆔 Telegram: @{customer.get('telegram_username', 'Não informado')}\n\n"
        f"📅 Cadastro: {customer.get('created_at', '')[:10]}\n"
    )

    keyboard = [
        [InlineKeyboardButton("✏️ Editar Cadastro", callback_data="edit_profile")],
        [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")],
    ]

    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ════════════════════════════════════════
# COMPROVANTES E ADMIN
# ════════════════════════════════════════

async def handle_payment_proof(update, context):
    """Processa o envio de comprovante de pagamento."""
    user_id = update.effective_user.id
    state, data = get_user_state(user_id)

    if state != "AWAITING_PROOF":
        return

    file_id = None
    file_type = None

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_type = "photo"
    elif update.message.document:
        file_id = update.message.document.file_id
        file_type = "document"

    if not file_id:
        await update.message.reply_text(
            "📎 *Envie o comprovante de pagamento*\n\n"
            "Envie uma foto ou documento do comprovante para aprovação.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    order_codes = data.get("order_codes", [])
    if not order_codes:
        await update.message.reply_text("❌ Pedido não encontrado. Inicie novamente.")
        clear_user_state(user_id)
        return

    save_payment_proof(order_codes, file_id, file_type)

    for code in order_codes:
        update_order_status(code, "aguardando_aprovacao")

    clear_user_state(user_id)

    await update.message.reply_text(
        f"✅ *Comprovante recebido!*\n\n"
        f"📋 Pedido: `{', '.join(order_codes)}`\n"
        f"⏳ Aguardando aprovação do administrador.\n\n"
        f"💰 Pagamento: PIX\n\n"
        f"Assim que aprovado, você receberá o link de download!\n\n"
        f"📞 Dúvidas? Fale conosco.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Suporte", callback_data="support")],
            [InlineKeyboardButton("🏠 Menu", callback_data="main_menu")]
        ])
    )

    # Notifica admin
    if ADMIN_CHAT_IDS:
        admin_text = (
            f"🛒 *NOVO PEDIDO PARA APROVAÇÃO*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📋 Código: `{', '.join(order_codes)}`\n"
            f"👤 Usuário: {user_id}\n"
            f"💰 Total: R$ {sum(o['price'] for o in get_orders_by_codes(order_codes)):.2f}\n"
            f"📎 Comprovante enviado!\n\n"
            f"Use /aprovar `{order_codes[0]}` para aprovar."
        )
        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(admin_id, admin_text, parse_mode=ParseMode.MARKDOWN)
                if file_type == "photo":
                    await context.bot.send_photo(admin_id, file_id)
                else:
                    await context.bot.send_document(admin_id, file_id)
            except Exception as e:
                logger.error(f"Erro ao notificar admin: {e}")


async def admin_approve(update, context):
    """Aprova um pedido pendente."""
    if update.effective_user.id not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ Acesso negado.")
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "📋 *Aprovar Pedido*\n\n"
            "Use: /aprovar CODIGO\n\n"
            "Exemplo: /aprovar WA-ABC12345",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    order_code = args[0].upper()
    order = get_order_by_code(order_code)

    if not order:
        await update.message.reply_text(f"❌ Pedido `{order_code}` não encontrado.")
        return

    if order["status"] == "aprovado":
        await update.message.reply_text(f"✅ Pedido `{order_code}` já foi aprovado.")
        return

    update_order_status(order_code, "aprovado")

    telegram_id = order["telegram_id"]
    download_url = order["download_url"]

    try:
        await context.bot.send_message(
            telegram_id,
            f"🎉 *PEDIDO APROVADO!*\n\n"
            f"Seu pedido `{order_code}` foi aprovado!\n\n"
            f"🎮 *{order['game_name']}*\n"
            f"⬇️ *Link para download:*\n"
            f"{download_url}\n\n"
            f"⏳ Link válido por {DOWNLOAD_LINK_EXPIRY_HOURS} horas.\n\n"
            f"💚 Aproveite! Qualquer dúvida, fale conosco.",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Erro ao enviar link para {telegram_id}: {e}")

    customer = get_customer(telegram_id)
    if customer and customer.get("email"):
        send_purchase_email(
            to_email=customer["email"],
            customer_name=customer.get("nome_completo", "Cliente"),
            order_code=order_code,
            game_name=order["game_name"],
            price=order["price"],
            download_url=download_url
        )

    await update.message.reply_text(
        f"✅ Pedido `{order_code}` aprovado!\n"
        f"📧 Link enviado para o cliente.",
        parse_mode=ParseMode.MARKDOWN
    )


async def admin_orders(update, context):
    """Lista pedidos pendentes."""
    if update.effective_user.id not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ Acesso negado.")
        return

    pending = get_pending_orders()

    if not pending:
        await update.message.reply_text("📋 Nenhum pedido pendente.")
        return

    text = "📋 *PEDIDOS PENDENTES*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for o in pending[:10]:
        text += f"📌 `{o['order_code']}` - {o['game_name']}\n"
        text += f"   R$ {o['price']:.2f} | 👤 {o['telegram_id']}\n\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ════════════════════════════════════════
# KEYBOARDS
# ════════════════════════════════════════

def catalog_keyboard(page, games, prefix="catalog"):
    """Monta teclado de catálogo paginado."""
    total_pages = max(1, math.ceil(len(games) / ITEMS_PER_PAGE))
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_games = games[start_idx:end_idx]

    keyboard = []
    for game in page_games:
        tag = " 🔥" if game["oferta"] else ""
        nome = game["nome"][:30] + "..." if len(game["nome"]) > 30 else game["nome"]
        btn_text = f"🎮 {nome} - R$ {game['preco_oferta']:.2f}{tag}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"game_{game['id']}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"{prefix}_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Próximo", callback_data=f"{prefix}_{page + 1}"))
    keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("🔍 Buscar Produto", callback_data="search_product")])
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


def back_to_menu_keyboard():
    """Botão de voltar ao menu."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")]
    ])


# ════════════════════════════════════════
# HANDLER PRINCIPAL
# ════════════════════════════════════════

async def button(update, context):
    """Gerenciador central de cliques."""
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass

    data = query.data
    user_id = query.from_user.id

    # ── Menu Principal ──
    if data == "main_menu":
        await start(update, context)

    # ── Catálogo ──
    elif data.startswith("catalog_"):
        page = int(data.split("_")[1])
        await query.edit_message_text(
            "🎮 *CATÁLOGO DE JOGOS E SOFTWARES*\n\nSelecione um produto para ver detalhes:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=catalog_keyboard(page, GAMES_CATALOG)
        )

    # ── Ofertas ──
    elif data.startswith("offers_"):
        page = int(data.split("_")[1])
        await show_offers(update, context, page)

    # ── Busca ──
    elif data == "search":
        await search_product_click(update, context)

    elif data == "search_product":
        await search_product_click(update, context)

    # ── Categorias ──
    elif data == "categories":
        await show_categories(update, context)

    elif data.startswith("cat_tipo_"):
        tipo = data.replace("cat_tipo_", "")
        await show_category_by_type(update, context, tipo, 0)

    elif data.startswith("tipopage_"):
        parts = data.split("_")
        page = int(parts[-1])
        tipo = "_".join(parts[1:-1])
        await show_category_by_type(update, context, tipo, page)

    # ── Resultados da Busca ──
elif data.startswith("search_res_"):
    page = int(data.split("_")[2])
    results = context.user_data.get("last_search_results", GAMES_CATALOG)
    await query.edit_message_text(
        "🔍 *RESULTADOS DA BUSCA*\n\nSelecione um produto para ver detalhes:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=catalog_keyboard(page, results, prefix="search_res")
    )

    # ── Detalhe do Produto ──
    elif data.startswith("game_"):
        game_id = int(data.split("_")[1])
        await show_game_detail(update, context, game_id)

    # ── Carrinho ──
    elif data == "cart":
        await show_cart(update, context)

    elif data.startswith("remove_"):
        cart_item_id = int(data.split("_")[1])
        remove_from_cart(user_id, cart_item_id)
        await show_cart(update, context)

    elif data.startswith("add_cart_"):
        game_id = int(data.split("_")[2])
        await add_to_cart(update, context, game_id)

    elif data.startswith("buy_now_"):
        game_id = int(data.split("_")[2])
        await buy_now(update, context, game_id)

    elif data == "checkout":
        await start_checkout(update, context)

    # ── Pagamento ──
    elif data.startswith("pay_"):
        method = data.split("_")[1]
        await process_payment(update, context, method)

    elif data == "confirm_purchase":
        await query.answer("✅ Pagamento confirmado! Aguardando comprovante...")
        await query.edit_message_text(
            "📎 *Envie o comprovante de pagamento*\n\n"
            "Envie uma foto ou documento do comprovante para aprovação.\n\n"
            "⏳ Após o envio, aguarde a aprovação do administrador.",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "cancel_purchase":
        clear_cart(user_id)
        clear_user_state(user_id)
        await query.edit_message_text(
            "❌ *Compra cancelada*\n\n"
            "Seu carrinho foi limpo. Caso mude de ideia, estamos aqui! 💚",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_menu_keyboard()
        )

    # ── Pedidos ──
    elif data == "my_orders":
        await show_orders(update, context)

    # ── Perfil ──
    elif data == "my_profile":
        await show_profile(update, context)

    elif data == "edit_profile":
        await query.edit_message_text(
            "✏️ *Editar Cadastro*\n\n"
            "Para atualizar seus dados, use os comandos:\n\n"
            "/nome Seu Nome Completo\n"
            "/email seu@email.com\n"
            "/telefone 11999999999\n\n"
            "Ou fale com o suporte.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_to_menu_keyboard()
        )

    # ── Institucional ──
    elif data == "institutional":
        await show_institutional(update, context)

    elif data.startswith("inst_"):
        page = data.replace("inst_", "")
        await institutional_detail(update, context, page)

    # ── Suporte ──
    elif data == "support":
        await show_support(update, context)

    # ── FAQ ──
    elif data == "faq":
        await show_faq(update, context)

    # ── No-op ──
    elif data == "noop":
        pass

# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════

async def main_async():
    """Inicializa e roda o bot."""
    print("=" * 60)
    print("🎮 WareArcadeBot - Iniciando...")
    print("=" * 60)

    init_db()
    print(f"✅ Banco de dados: warearcade.db")
    print(f"📦 Catálogo: {len(GAMES_CATALOG)} produtos")
    print("🚀 Bot rodando! Pressione Ctrl+C para parar.")
    print("=" * 60)

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(120)
        .read_timeout(120)
        .write_timeout(120)
        .pool_timeout(120)
        .get_updates_connect_timeout(120)
        .get_updates_read_timeout(120)
        .build()
    )

    # ── Comandos ──
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("catalogo", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("ofertas", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("carrinho", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("pedidos", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("perfil", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("suporte", lambda u, c: button(u, c)))
    app.add_handler(CommandHandler("faq", lambda u, c: button(u, c)))

    # ── Comandos Admin ──
    app.add_handler(CommandHandler("aprovar", admin_approve))
    app.add_handler(CommandHandler("pendentes", admin_orders))
    app.add_handler(CommandHandler("admin", lambda u, c: button(u, c)))

    # ── Handlers ──
    app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_payment_proof))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_registration))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Bot finalizado.")


def main():
    """Ponto de entrada principal com reconexão automática."""
    tentativas = 0
    max_tentativas = 10

    while tentativas < max_tentativas:
        try:
            asyncio.run(main_async())
            break
        except KeyboardInterrupt:
            print("\n🛑 Bot parado pelo usuário.")
            break
        except Exception as e:
            error_str = str(e).lower()
            if "timeout" in error_str or "network" in error_str or "connection" in error_str:
                tentativas += 1
                print(f"\n⚠️ Erro de rede ({tentativas}/{max_tentativas}): {e}")
                print(f"⏳ Tentando novamente em {tentativas * 5} segundos...")
                time.sleep(tentativas * 5)
            else:
                print(f"\n❌ Erro inesperado: {e}")
                import traceback
                traceback.print_exc()
                break

    if tentativas >= max_tentativas:
        print("\n❌ Bot parou após várias tentativas de reconexão.")
        print("   Verifique sua conexão com a internet e tente novamente.")


if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN não configurado!")
        print("   Crie um arquivo .env com: TELEGRAM_BOT_TOKEN=seu_token")
    else:
        main()