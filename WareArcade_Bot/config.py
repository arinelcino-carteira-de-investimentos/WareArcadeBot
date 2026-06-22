"""
===============================================
WareArcadeBot - Configurações do Sistema
===============================================
Arquivo de configuração central do bot.
Todas as variáveis sensíveis são lidas do .env
===============================================
"""

import os
from dotenv import load_dotenv

# Força o carregamento do arquivo .env da pasta atual
load_dotenv()

# Token do Telegram obtido via .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ── Configurações de Email (Gmail SMTP) ──
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # App Password do Gmail
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "WareArcadeBot - Nexus Digital Shop")

# ── Configurações do Admin ──
try:
    ADMIN_CHAT_IDS = [int(x.strip()) for x in os.getenv("ADMIN_CHAT_IDS", "0").split(",") if x.strip()]
except ValueError:
    ADMIN_CHAT_IDS = [0]

# ── Link de download e expiração ──
DOWNLOAD_BASE_URL = os.getenv("DOWNLOAD_BASE_URL", "https://warearcadebot.com.br/downloads/")
DOWNLOAD_LINK_EXPIRY_HOURS = int(os.getenv("DOWNLOAD_LINK_EXPIRY_HOURS", "48"))

# ── Banco de dados ──
DATABASE_PATH = os.getenv("DATABASE_PATH", "warearcade.db")

# ── Itens por página no catálogo ──
ITEMS_PER_PAGE = 6

# ════════════════════════════════════════
# INFORMAÇÕES DA LOJA
# ════════════════════════════════════════
STORE_NAME = "🎮 WareArcadeBot - Nexus Digital Shop"
STORE_WEBSITE = "https://warearcadebot.com.br/"
STORE_EMAIL = "warearcadebot@gmail.com"
STORE_INSTAGRAM = "@warearcadebot"
STORE_HOURS = "Seg a Sex: 9h-19h | Sáb: 9h-14h"
STORE_WHATSAPP = "+5511940462611"

# ════════════════════════════════════════
# CONFIGURAÇÕES DE PIX
# ════════════════════════════════════════
PIX_CHAVE = os.getenv("PIX_CHAVE", "11940462611")
PIX_NOME = os.getenv("PIX_NOME", "Arinelcino Gonçalves de Sena")
PIX_CIDADE = os.getenv("PIX_CIDADE", "Sao Paulo")
PIX_TIPO = os.getenv("PIX_TIPO", "Celular")

# ════════════════════════════════════════
# DADOS BANCÁRIOS (Boleto / TED / DOC)
# ════════════════════════════════════════
BANCO_NOME = os.getenv("BANCO_NOME", "Neon Pagamentos - IP")
BANCO_CODIGO = os.getenv("BANCO_CODIGO", "536")
BANCO_AGENCIA = os.getenv("BANCO_AGENCIA", "0655")
BANCO_CONTA = os.getenv("BANCO_CONTA", "32691694-6")
BANCO_CNPJ = os.getenv("BANCO_CNPJ", "20.855.875/0001-82")
BANCO_TITULAR = os.getenv("BANCO_TITULAR", "Arinelcino Gonçalves de Sena")

# ════════════════════════════════════════
# FORMAS DE PAGAMENTO ACEITAS
# ════════════════════════════════════════
PAYMENT_METHODS = [
    "💰 PIX (Aprovação Imediata)",
    "💳 Cartão de Crédito",
    "🏦 Transferência Bancária (TED)",
    "📄 Boleto Bancário",
]