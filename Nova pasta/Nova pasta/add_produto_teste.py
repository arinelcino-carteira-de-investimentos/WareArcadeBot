"""
═══════════════════════════════════════════════════════════
ADICIONA PRODUTO DE TESTE - WareArcadeBot
═══════════════════════════════════════════════════════════
Cria produto "TESTE DO ARI" por R$ 1,50 para testes
═══════════════════════════════════════════════════════════
"""
import shutil

print("=" * 60)
print("  ADICIONANDO PRODUTO DE TESTE - R$ 1,50")
print("=" * 60)

# Backup
shutil.copy("catalog.py", "catalog.py.backup_teste")
print("[OK] Backup criado: catalog.py.backup_teste")

with open("catalog.py", "r", encoding="utf-8") as f:
    c = f.read()

# Verifica se ja existe
if '"id": 999' in c or 'TESTE DO ARI' in c:
    print("[AVISO] Produto teste ja existe! Removendo antigo...")
    import re
    # Remove produto teste antigo
    padrao = re.compile(
        r'\s*\{"id":\s*999,[^}]+\},?',
        re.DOTALL
    )
    c = padrao.sub("", c)

# Produto de teste
produto_teste = '''    {
        "id": 999,
        "nome": "TESTE DO ARI",
        "preco_original": 1.50,
        "preco_oferta": 1.50,
        "descricao": "Produto de teste para validar o fluxo de compra completo no Telegram. Compre, pague o PIX, envie o comprovante e receba o link de download! Valor simbólico de R$ 1,50.",
        "categorias": ["Destaques"],
        "oferta": True,
        "plataforma": "PC",
        "tipo": "🧪 Teste",
        "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/440/header.jpg"
    },
'''

# Insere ANTES do fechamento da lista
idx = c.rfind("]")
if idx > 0:
    # Pega tudo antes do ]
    antes = c[:idx].rstrip()
    
    # Adiciona virgula se nao tiver
    if not antes.endswith(","):
        antes += ","
    
    # Monta novo catalogo
    c_novo = antes + "\n" + produto_teste + "\n]" + c[idx+1:]
    
    with open("catalog.py", "w", encoding="utf-8") as f:
        f.write(c_novo)
    
    print("[OK] Produto TESTE DO ARI adicionado!")
else:
    print("[ERRO] Nao encontrei o fim da lista!")
    exit()

# Valida sintaxe
try:
    with open("catalog.py", "r", encoding="utf-8") as f:
        compile(f.read(), "catalog.py", "exec")
    print("[OK] Sintaxe valida!")
    
    # Conta produtos
    from catalog import GAMES_CATALOG
    total = len(GAMES_CATALOG)
    
    # Procura o produto teste
    teste = next((g for g in GAMES_CATALOG if g["id"] == 999), None)
    
    print("\n" + "=" * 60)
    print("  PRODUTO ADICIONADO COM SUCESSO!")
    print("=" * 60)
    print(f"\n  ID: {teste['id']}")
    print(f"  Nome: {teste['nome']}")
    print(f"  Preço: R$ {teste['preco_oferta']:.2f}")
    print(f"  Tipo: {teste['tipo']}")
    print(f"  Categoria: {', '.join(teste['categorias'])}")
    print(f"  Plataforma: {teste['plataforma']}")
    print(f"\n  Total de produtos no catalogo: {total}")
    print("\n" + "=" * 60)
    print("\n  COMO TESTAR:")
    print("  1. Pare o bot atual (Ctrl+C)")
    print("  2. Rode: py bot.py")
    print("  3. No Telegram, envie: /start")
    print("  4. Clique em: 🔥 Ofertas HOT")
    print("  5. Procure: 🧪 TESTE DO ARI - R$ 1,50")
    print("  6. Adicione ao carrinho")
    print("  7. Finalize a compra")
    print("  8. Escolha PIX")
    print("  9. Envie qualquer foto como comprovante")
    print("  10. Aprove como admin")
    print("  11. Receba o link de download!")
    print("=" * 60)
    
except SyntaxError as e:
    print(f"[ERRO] Sintaxe: {e}")
    shutil.copy("catalog.py.backup_teste", "catalog.py")
    print("[OK] Backup restaurado.")