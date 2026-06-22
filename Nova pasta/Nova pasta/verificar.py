sucessos = 5  # Exemplo de variável
erros = 0     # Exemplo de variável

print("=" * 60)
print(f"  Sucessos: {sucessos}")
print(f"  Erros: {erros}")
print("=" * 60)

if erros == 0:
    print("\n TUDO PRONTO! Você pode rodar o bot com:")
    print("  python bot.py\n")
else:
    print(f"\n Corrija os {erros} erro(s) acima antes de rodar o bot.\n")
