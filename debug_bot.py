"""
LIMPA TODOS BOTOES COM URL - SOLUCAO BRUTA
"""
import shutil
import re

print("=" * 60)
print("  LIMPANDO TODOS OS BOTOES COM URL")
print("=" * 60)

shutil.copy("bot.py", "bot.py.backup_limpar")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Conta antes
antes = len(re.findall(r'InlineKeyboardButton\([^)]*url\s*=', c))
print(f"[INFO] Botoes com URL antes: {antes}")

# REMOVE TODOS os botoes com url= (linha inteira ou em sequencia)
# Padrao 1: [InlineKeyboardButton(...url=...)]
c = re.sub(
    r'\[InlineKeyboardButton\([^\[\]]*url\s*=\s*[^\[\]]*\)\],?\s*\n',
    '',
    c
)

# Padrao 2: InlineKeyboardButton(...url=...) com virgula
c = re.sub(
    r'InlineKeyboardButton\([^)]*url\s*=\s*[^)]*\)\s*,?',
    '',
    c
)

# Limpa virgulas duplas, []
c = re.sub(r',\s*,', ',', c)
c = re.sub(r'\[\s*,', '[', c)
c = re.sub(r',\s*\]', ']', c)
c = re.sub(r'\[\s*\]', '', c)

# Conta depois
depois = len(re.findall(r'InlineKeyboardButton\([^)]*url\s*=', c))
print(f"[INFO] Botoes com URL depois: {depois}")
print(f"[OK] {antes - depois} botoes URL removidos!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("\n[OK] Sintaxe valida!")
    print("\nRode: py bot.py")
except SyntaxError as e:
    print(f"\n[ERRO] {e}")
    print("Restaurando backup...")
    shutil.copy("bot.py.backup_limpar", "bot.py")
    print("[OK] Backup restaurado.")