"""
Correcao DEFINITIVA do timeout
Aumenta timeout para 120 segundos
"""
import shutil
import re

print("=" * 60)
print("CORRECAO DEFINITIVA - TIMEOUT 120s")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_def")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Remove qualquer Application.builder antigo
padroes = [
    r"app = Application\.builder\(\)\.token\(TELEGRAM_BOT_TOKEN\)\.build\(\)",
    r"app = \(\s*Application\.builder\(\)[\s\S]*?\.build\(\)\s*\)",
]

for p in padroes:
    c = re.sub(p, "APP_PLACEHOLDER", c)

# Substitui pelo novo com timeout BIG
novo_app = """app = (
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
    )"""

c = c.replace("APP_PLACEHOLDER", novo_app, 1)

# Remove duplicatas se houver
c = c.replace("APP_PLACEHOLDER", "")

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

print("[OK] Timeout aumentado para 120s!")

try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\nAgora rode: python bot.py")
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_def", "bot.py")
    print("[OK] Backup restaurado.")

print("=" * 60)