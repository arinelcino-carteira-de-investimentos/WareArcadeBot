import shutil

print("Iniciando correcao...")

# Backup
shutil.copy("bot.py", "bot.py.backup")
print("Backup criado!")

# Le o arquivo
with open("bot.py", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Procura a funcao main
idx = conteudo.rfind("def main()")
if idx == -1:
    idx = conteudo.rfind("async def main_async")

if idx == -1:
    print("ERRO: nao achei a funcao main!")
    exit()

# Recua ate o comentario
sec = conteudo.rfind("# ==", 0, idx)
if sec > 0 and (idx - sec) < 300:
    idx = sec

# Pega tudo antes
antes = conteudo[:idx].rstrip()

# Novo codigo do MAIN
novo = """


# ========================================
# MAIN
# ========================================

import asyncio


async def main_async():
    print("WareArcadeBot iniciando...")
    init_db()
    print(f"Banco OK | {len(GAMES_CATALOG)} jogos")
    
    if not TELEGRAM_BOT_TOKEN:
        print("ERRO: Token vazio!")
        return
    
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .get_updates_connect_timeout(30)
        .get_updates_read_timeout(30)
        .build()
    )
    
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
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receive_proof_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    print("Bot rodando! @WareArcadeBot")
    
    try:
        await app.initialize()
        await app.start()
        await app.updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            print("Parando...")
    finally:
        try:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
        except Exception:
            pass


def main():
    import time
    for t in range(5):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main_async())
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            if "timeout" in str(e).lower():
                print(f"Tentativa {t+1}/5: {e}")
                time.sleep(10)
            else:
                import traceback
                traceback.print_exc()
                break


if __name__ == "__main__":
    main()
"""

# Junta e salva
final = antes + novo

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(final)

print("Arquivo salvo!")

# Valida sintaxe
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("\nSUCESSO! Sintaxe OK!")
    print("Agora rode: python bot.py")
except SyntaxError as e:
    print(f"\nErro de sintaxe: {e}")
    print("Restaurando backup...")
    shutil.copy("bot.py.backup", "bot.py")
    print("Backup restaurado.")