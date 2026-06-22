"""
Script para corrigir o bot.py automaticamente
"""
import shutil
import re

print("=" * 60)
print("CORRIGINDO bot.py - REMOVENDO LINHAS DUPLICADAS")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup-fix")
print("[OK] Backup criado: bot.py.backup-fix")

# Le o arquivo
with open("bot.py", "r", encoding="utf-8") as f:
    linhas = f.readlines()

print(f"[INFO] Arquivo tem {len(linhas)} linhas")

# Encontra a linha 1726 e arredores
print("\n[INFO] Mostrando linhas 1720-1740:")
for i in range(1720, min(1740, len(linhas))):
    marca = " <-- ERRO" if i == 1725 else ""
    print(f"  {i+1}: {linhas[i].rstrip()}{marca}")

print("\n[INFO] Procurando 'app = (' duplicado...")

# Encontra todas as ocorrencias de "app = ("
ocorrencias = []
for i, linha in enumerate(linhas):
    if "app = (" in linha or "app = Application.builder" in linha:
        ocorrencias.append((i, linha.rstrip()))

print(f"\n[INFO] Encontrei {len(ocorrencias)} declaracoes de 'app':")
for idx, (linha_num, conteudo) in enumerate(ocorrencias):
    print(f"  {idx+1}. Linha {linha_num+1}: {conteudo}")

if len(ocorrencias) > 1:
    print("\n[FIX] Vou remover as duplicacoes...")
    
    # Pega a posicao da PRIMEIRA declaracao correta de "app = ("
    # E remove tudo entre ela e a segunda (que esta duplicada)
    
    # Encontra "app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()"
    posicao_antiga = -1
    for i, linha in enumerate(linhas):
        if "app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()" in linha:
            posicao_antiga = i
            break
    
    if posicao_antiga >= 0:
        print(f"[INFO] Removendo linha antiga {posicao_antiga+1}: {linhas[posicao_antiga].rstrip()}")
        # Remove a linha antiga
        linhas.pop(posicao_antiga)
        
        # Remove tambem a linha em branco apos (se existir)
        if posicao_antiga < len(linhas) and linhas[posicao_antiga].strip() == "":
            linhas.pop(posicao_antiga)

# Corrige indentacao da linha "app = ("
print("\n[FIX] Corrigindo indentacao...")
for i, linha in enumerate(linhas):
    if "app = (" in linha and linha.startswith("        "):
        # Tem 8 espacos no inicio, deveria ter 4
        linhas[i] = "    " + linha.lstrip()
        print(f"[OK] Linha {i+1} corrigida")
    
    # Corrige tambem as linhas seguintes do bloco app = (...)
    if i > 0 and linhas[i-1].strip().endswith("Application.builder()"):
        # Linhas dentro do bloco devem ter 8 espacos
        if linha.startswith("            ."):
            linhas[i] = "        " + linha.lstrip()

# Salva
with open("bot.py", "w", encoding="utf-8") as f:
    f.writelines(linhas)

print("\n[OK] Arquivo salvo!")

# Valida sintaxe
print("\n[INFO] Validando sintaxe...")
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] SINTAXE PERFEITA!")
    print("\n>>> Agora rode: python bot.py")
except SyntaxError as e:
    print(f"\n[ERRO] Ainda tem erro de sintaxe: {e}")
    print(f"[ERRO] Linha: {e.lineno}")
    print("\nRestaurando backup...")
    shutil.copy("bot.py.backup-fix", "bot.py")
    print("[OK] Backup restaurado.")
    print("\n[INFO] Vou te mostrar as 10 linhas ao redor do erro:")
    
    with open("bot.py", "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    if e.lineno:
        inicio = max(0, e.lineno - 5)
        fim = min(len(linhas), e.lineno + 5)
        for i in range(inicio, fim):
            marca = " <-- ERRO" if i == e.lineno - 1 else ""
            print(f"  {i+1}: {linhas[i].rstrip()}{marca}")

print("=" * 60)