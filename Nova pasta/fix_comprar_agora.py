"""
CORRIGE ERRO AO CLICAR EM COMPRAR AGORA
"""
import shutil
import re

print("=" * 60)
print("  CORRIGINDO ERRO COMPRAR AGORA")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_compra")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Funcao buy_now BLINDADA contra erros
nova_buy_now = '''async def buy_now(update, context, game_id):
    """Compra direta de um produto - BLINDADO."""
    try:
        user_id = update.callback_query.from_user.id
        game = get_game_by_id(game_id)

        if not game:
            await update.callback_query.answer("Produto nao encontrado!", show_alert=True)
            return

        # Limpa carrinho e adiciona o produto
        try:
            clear_cart(user_id)
            add_to_cart(user_id, game["id"], game["nome"], game["preco_oferta"])
        except Exception as e:
            logger.error(f"Erro ao adicionar ao carrinho: {e}")
            await update.callback_query.answer("Erro ao adicionar produto. Tente novamente.", show_alert=True)
            return

        # Verifica cadastro
        if not is_customer_complete(user_id):
            await start_registration_for_checkout(update, context)
            return

        # Vai direto pro checkout
        await start_checkout(update, context)

    except Exception as e:
        logger.error(f"Erro em buy_now: {e}", exc_info=True)
        try:
            await update.callback_query.message.reply_text(
                "Ocorreu um erro. Tente clicar em Adicionar ao Carrinho.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Menu", callback_data="main_menu")
                ]])
            )
        except Exception:
            pass

'''

# Substitui buy_now antigo
padrao = re.compile(
    r'async def buy_now\(update, context, game_id\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)
if padrao.search(c):
    c = padrao.sub(nova_buy_now, c)
    print("[OK] buy_now blindado!")
else:
    print("[INFO] buy_now nao encontrado, adicionando...")
    # Adiciona apos buy_now ou show_game_detail
    idx = c.find("async def show_orders")
    if idx > 0:
        c = c[:idx] + nova_buy_now + "\n\n" + c[idx:]

# Funcao start_checkout BLINDADA
nova_checkout = '''async def start_checkout(update, context):
    """Inicia o processo de checkout - BLINDADO."""
    try:
        if update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            user_id = update.effective_user.id

        cart = get_cart(user_id)

        if not cart:
            if update.callback_query:
                await update.callback_query.answer("Carrinho vazio!", show_alert=True)
            return

        if not is_customer_complete(user_id):
            await start_registration_for_checkout(update, context)
            return

        customer = get_customer(user_id)
        total = get_cart_total(user_id)

        nome = customer.get('nome_completo', 'Cliente')
        email = customer.get('email', '')

        text = "💳 *FINALIZAR COMPRA*\\n\\n"
        text += f"👤 Cliente: {nome}\\n"
        text += f"📧 Email: {email}\\n\\n"
        text += "🛒 *Itens:*\\n"

        for i, item in enumerate(cart, 1):
            nome_item = item['game_name'].replace("*", "").replace("_", "").replace("`", "")
            text += f"  {i}. {nome_item} - R$ {item['price']:.2f}\\n"

        text += f"\\n━━━━━━━━━━━━━━━━━━━━━━\\n"
        text += f"💰 *TOTAL: R$ {total:.2f}*\\n\\n"
        text += "Selecione o pagamento:"

        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    text, parse_mode=ParseMode.MARKDOWN, reply_markup=payment_keyboard()
                )
            except Exception:
                # Se nao conseguir editar, envia nova
                await update.callback_query.message.reply_text(
                    text, parse_mode=ParseMode.MARKDOWN, reply_markup=payment_keyboard()
                )
        else:
            await update.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=payment_keyboard()
            )

    except Exception as e:
        logger.error(f"Erro em start_checkout: {e}", exc_info=True)
        try:
            if update.callback_query:
                await update.callback_query.message.reply_text(
                    "Erro ao finalizar. Tente novamente.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("Menu", callback_data="main_menu")
                    ]])
                )
        except Exception:
            pass

'''

# Substitui start_checkout
padrao2 = re.compile(
    r'async def start_checkout\(update, context\):.*?(?=\nasync def |\ndef )',
    re.DOTALL
)
if padrao2.search(c):
    c = padrao2.sub(nova_checkout, c)
    print("[OK] start_checkout blindado!")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\n" + "=" * 60)
    print("  CORRECAO APLICADA COM SUCESSO!")
    print("=" * 60)
    print("\n  O que foi feito:")
    print("  - buy_now blindado contra todos os erros")
    print("  - start_checkout blindado")
    print("  - Caracteres especiais sanitizados")
    print("  - Fallback automatico em caso de erro")
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_compra", "bot.py")
    print("[OK] Backup restaurado.")