"""
Corrige problema de timeout do bot
Aumenta o tempo de espera de conexao com Telegram
"""
import shutil

print("=" * 60)
print("CORRIGINDO TIMEOUT DO BOT")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_timeout")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Procura o builder do Application
# Versao SIMPLES
old1 = "Application.builder().token(TELEGRAM_BOT_TOKEN).build()"
new1 = """(
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .get_updates_connect_timeout(60)
        .get_updates_read_timeout(60)
        .build()
    )"""

if old1 in c:
    c = c.replace(old1, new1)
    print("[OK] Timeout aumentado para 60s!")
else:
    # Pode ja estar com timeout, vamos atualizar
    import re
    
    # Procura outras variacoes
    pattern = r"Application\.builder\(\)[\s\S]*?\.build\(\)"
    match = re.search(pattern, c)
    
    if match:
        novo = """(
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .get_updates_connect_timeout(60)
        .get_updates_read_timeout(60)
        .build()
    )"""
        c = c[:match.start()] + novo + c[match.end():]
        # Remove o "(" e ")" extras se existirem
        c = c.replace("app = ((", "app = (")
        c = c.replace("))", ")")
        print("[OK] Timeout atualizado!")

# Adiciona retry automatico se nao tiver
if "max_tentativas = 10" not in c:
    # Procura def main():
    old_main = "def main():"
    new_main = """def main():
    \"\"\"Wrapper com retry automatico de 10 tentativas.\"\"\"
    import time
    max_tentativas = 10
    
    for tentativa in range(max_tentativas):
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main_async())
            break
        except KeyboardInterrupt:
            print("\\n[OK] Bot parado pelo usuario.")
            break
        except Exception as e:
            erro = str(e).lower()
            if "timeout" in erro or "timed out" in erro or "network" in erro:
                print(f"\\n[AVISO] Conexao perdida ({tentativa+1}/{max_tentativas})")
                print(f"[INFO] Aguardando 15s para reconectar...")
                time.sleep(15)
                continue
            else:
                print(f"\\n[ERRO] {e}")
                import traceback
                traceback.print_exc()
                break
    
    if tentativa >= max_tentativas - 1:
        print("\\n[ERRO] Bot parou apos varias tentativas. Verifique sua internet.")


def _main_old():"""
    c = c.replace(old_main, new_main)
    print("[OK] Retry automatico adicionado!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\nAgora o bot:")
    print("  - Aguarda 60s antes de desistir (era 5s)")
    print("  - Reconecta automaticamente se cair")
    print("  - Tenta 10 vezes antes de parar")
    print("\nRode: python bot.py")
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_timeout", "bot.py")
    print("[OK] Backup restaurado.")

print("=" * 60)