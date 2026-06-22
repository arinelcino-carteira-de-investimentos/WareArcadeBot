"""
ADICIONA PRODUTO TESTE - VERSAO 2 (CORRIGIDA)
"""
import shutil
import re

print("=" * 60)
print("  ADICIONANDO PRODUTO TESTE - V2")
print("=" * 60)

# Backup
shutil.copy("catalog.py", "catalog.py.backup_v2")
print("[OK] Backup criado")

with open("catalog.py", "r", encoding="utf-8") as f:
    c = f.read()

# Remove TODOS os produtos teste antigos (limpa primeiro)
padroes_remover = [
    r'\s*\{[^{}]*"id":\s*999[^{}]*\}\s*,?\s*',
    r'\s*\{[^{}]*"TESTE DO ARI"[^{}]*\}\s*,?\s*',
]

for p in padroes_remover:
    c_novo = re.sub(p, '', c)
    if c_novo != c:
        print("[INFO] Produto antigo removido!")
        c = c_novo

# Localiza onde a lista GAMES_CATALOG TERMINA
# Procura por ] (que fecha a lista)
# Vamos procurar pela ultima chave } seguida de ,? e depois ]
padrao_final = re.compile(r'(\}\s*,?)\s*(\n\s*\])', re.DOTALL)
match = padrao_final.search(c)

if not match:
    print("[ERRO] Nao encontrei o fim da lista GAMES_CATALOG!")
    exit()

# Pega a posicao onde inserir
pos_inserir = match.start(1) + len(match.group(1))

# Produto teste (formatado correto)
produto = '''
    {
        "id": 999,
        "nome": "TESTE DO ARI",
        "preco_original": 1.50,
        "preco_oferta": 1.50,
        "descricao": "Produto de teste para validar fluxo completo. Pague R$ 1,50 via PIX!",
        "categorias": ["Destaques"],
        "oferta": True,
        "plataforma": "PC",
        "tipo": "Teste",
        "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/440/header.jpg"
    },'''

# Insere o produto
c_novo = c[:pos_inserir] + produto + c[pos_inserir:]

# Garante que ha virgula antes do produto inserido
# Procura "}\s*\n\s*{" para garantir virgulas
c_novo = re.sub(r'\}\s*\n\s*\{', '},\n    {', c_novo)

# Salva
with open("catalog.py", "w", encoding="utf-8") as f:
    f.write(c_novo)

print("[OK] Arquivo salvo!")

# Valida sintaxe
try:
    with open("catalog.py", "r", encoding="utf-8") as f:
        compile(f.read(), "catalog.py", "exec")
    print("[OK] Sintaxe valida!")
except SyntaxError as e:
    print(f"[ERRO] Sintaxe: {e}")
    print("Restaurando backup...")
    shutil.copy("catalog.py.backup_v2", "catalog.py")
    exit()

# RECARREGA o modulo para verificar
import sys
if 'catalog' in sys.modules:
    del sys.modules['catalog']

# Importa novamente
import catalog
total = len(catalog.GAMES_CATALOG)

# Procura o produto
teste = None
for g in catalog.GAMES_CATALOG:
    if g.get("id") == 999:
        teste = g
        break

print("\n" + "=" * 60)
if teste:
    print("  PRODUTO ADICIONADO COM SUCESSO!")
    print("=" * 60)
    print(f"  ID:        {teste['id']}")
    print(f"  Nome:      {teste['nome']}")
    print(f"  Preco:     R$ {teste['preco_oferta']:.2f}")
    print(f"  Categoria: {teste['categorias']}")
    print(f"  Tipo:      {teste['tipo']}")
    print(f"  Oferta:    {teste['oferta']}")
    print("=" * 60)
    print(f"\n  TOTAL DE PRODUTOS NO CATALOGO: {total}")
    print("\n  PROXIMO PASSO:")
    print("  1. py bot.py")
    print("  2. No Telegram: /start")
    print("  3. Buscar: TESTE")
    print("=" * 60)
else:
    print("  ERRO: PRODUTO NAO FOI ADICIONADO!")
    print("=" * 60)
    print(f"  Total atual: {total} produtos")
    print("  O script falhou. Vou tentar abordagem diferente...")
    print("=" * 60)
    
    # ABORDAGEM ALTERNATIVA: Edita diretamente
    print("\n[INFO] Tentando metodo alternativo...")
    
    # Restaura backup
    shutil.copy("catalog.py.backup_v2", "catalog.py")
    
    with open("catalog.py", "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    # Procura a ultima linha que tem } (final de produto)
    ultima_linha_produto = -1
    for i, linha in enumerate(linhas):
        if linha.strip() in ['},', '}']:
            ultima_linha_produto = i
    
    if ultima_linha_produto > 0:
        # Garante virgula
        if linhas[ultima_linha_produto].strip() == '}':
            linhas[ultima_linha_produto] = linhas[ultima_linha_produto].replace('}', '},')
        
        # Insere produto teste
        novo_produto = [
            '    {\n',
            '        "id": 999,\n',
            '        "nome": "TESTE DO ARI",\n',
            '        "preco_original": 1.50,\n',
            '        "preco_oferta": 1.50,\n',
            '        "descricao": "Produto de teste",\n',
            '        "categorias": ["Destaques"],\n',
            '        "oferta": True,\n',
            '        "plataforma": "PC",\n',
            '        "tipo": "Teste",\n',
            '        "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/440/header.jpg"\n',
            '    },\n',
        ]
        
        # Insere logo apos a ultima linha de produto
        linhas[ultima_linha_produto+1:ultima_linha_produto+1] = novo_produto
        
        with open("catalog.py", "w", encoding="utf-8") as f:
            f.writelines(linhas)
        
        print("[OK] Metodo alternativo aplicado!")
        
        # Recarrega
        if 'catalog' in sys.modules:
            del sys.modules['catalog']
        import catalog
        
        teste2 = next((g for g in catalog.GAMES_CATALOG if g.get("id") == 999), None)
        
        if teste2:
            print(f"\n[OK] SUCESSO! Total: {len(catalog.GAMES_CATALOG)} produtos")
            print(f"[OK] {teste2['nome']} - R$ {teste2['preco_oferta']:.2f}")
        else:
            print("[ERRO] Falhou novamente. Vamos editar manualmente...")