async def show_support(update, context):
    """Suporte ULTRA SIMPLES - sem botoes URL."""
    text = (
        "📞 SUPORTE AO CLIENTE\n\n"
        "🏪 WareArcadeBot\n\n"
        "📱 WhatsApp: +55 11 94046-2611\n"
        "📧 Email: warearcadebot@gmail.com\n"
        "📸 Instagram: @warearcadebot\n"
        "⏰ Seg a Sex: 9h-19h | Sab: 9h-14h\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔗 Links rapidos:\n\n"
        "WhatsApp: https://wa.me/5511940462611\n"
        "Instagram: https://instagram.com/warearcadebot\n\n"
        "💚 Atendimento humanizado!\n"
        "Respondemos em ate 30 minutos."
    )
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    
    try:
        if update.callback_query:
            await update.callback_query.message.reply_text(
                text, 
                reply_markup=kb,
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(
                text, 
                reply_markup=kb,
                disable_web_page_preview=True
            )
    except Exception as e:
        logger.error(f"Erro suporte: {e}", exc_info=True)
