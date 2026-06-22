"""
SCRIPT COMPLETO - WareArcadeBot
Corrige nome, adiciona institucional, corrige imagens,
adiciona novos produtos e atualiza tela inicial.
"""
import shutil

print("=" * 60)
print("  WAREARCADEBOT - ATUALIZACAO COMPLETA")
print("=" * 60)

# ══════════════════════════════════════════
# PARTE 1: CORRIGIR BOT.PY
# ══════════════════════════════════════════
print("\n[1/3] CORRIGINDO bot.py...")

shutil.copy("bot.py", "bot.py.backup_total")
print("  Backup criado: bot.py.backup_total")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Corrige o nome em todo o arquivo
c = c.replace("NEXUS DIGITAL SHOP", "WareArcadeBot")
c = c.replace("Nexus Digital Shop", "WareArcadeBot")
c = c.replace("nexusdigitalshop", "warearcadebot")
print("  Nome corrigido para WareArcadeBot")

# 2. Funcao institucional
if "async def show_institutional" not in c:
    inst = '''

async def show_institutional(update, context):
    """Menu Institucional."""
    text = (
        "📋 *INSTITUCIONAL - WareArcadeBot*\\n"
        "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "Conhca nossas politicas e informacoes.\\n"
        "Escolha uma opcao:"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Sobre Nos", callback_data="inst_sobre")],
        [InlineKeyboardButton("🔒 Privacidade", callback_data="inst_privacidade")],
        [InlineKeyboardButton("📜 Termos de Uso", callback_data="inst_termos")],
        [InlineKeyboardButton("🚚 Entrega", callback_data="inst_entrega")],
        [InlineKeyboardButton("💰 Reembolso", callback_data="inst_reembolso")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📞 Contato", callback_data="support")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
        )


async def institutional_detail(update, context, page):
    """Paginas do institucional."""
    paginas = {
        "sobre": (
            "📋 *SOBRE NOS - WareArcadeBot*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "Somos uma loja digital completa com:\\n\\n"
            "🎮 92+ jogos para PC\\n"
            "🖥️ Sistemas operacionais originais\\n"
            "📄 Microsoft Office completo\\n"
            "🎨 Adobe e softwares de design\\n"
            "🏗️ AutoCAD, SketchUp e mais\\n"
            "🔒 Antivirus premium\\n"
            "🛠️ Ferramentas e utilitarios\\n"
            "🎬 Streaming (Netflix, Spotify)\\n"
            "🎁 Gift Cards (Steam, PSN, Xbox)\\n"
            "☁️ Armazenamento em nuvem\\n"
            "🎓 Cursos online\\n\\n"
            "🚀 Entrega 100% digital e imediata\\n"
            "💰 Os menores precos do Brasil\\n"
            "🔒 Pagamento 100% seguro\\n"
            "📞 Suporte humanizado\\n\\n"
            "Horario: Seg a Sex 9h-19h\\n"
            "Sab: 9h-14h"
        ),
        "privacidade": (
            "🔒 *POLITICA DE PRIVACIDADE*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "1. Coletamos apenas dados necessarios:\\n"
            "   nome, email e telefone.\\n\\n"
            "2. Nao armazenamos dados de cartao.\\n\\n"
            "3. Nao compartilhamos com terceiros.\\n\\n"
            "4. Voce pode solicitar exclusao a qualquer\\n"
            "   momento pelo suporte.\\n\\n"
            "5. Pagamentos via gateways seguros."
        ),
        "termos": (
            "📜 *TERMOS DE USO*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "1. Produtos sao digitais e entregues\\n"
            "   apos confirmacao do pagamento.\\n\\n"
            "2. Links validos por 48 horas.\\n\\n"
            "3. Uso pessoal apenas.\\n"
            "   Proibida redistribuicao.\\n\\n"
            "4. Suporte para ativacao e instalacao.\\n\\n"
            "5. Nao nos responsabilizamos por\\n"
            "   incompatibilidade do hardware."
        ),
        "entrega": (
            "🚚 *POLITICA DE ENTREGA*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "Como funciona:\\n\\n"
            "1. Escolha o produto\\n"
            "2. Faca o pagamento\\n"
            "3. Envie o comprovante\\n"
            "4. Apos aprovacao, receba:\\n"
            "   - Link aqui no Telegram\\n"
            "   - Link por email\\n\\n"
            "Tempo medio:\\n"
            "• PIX: 5-30 minutos\\n"
            "• Cartao: 5-15 minutos\\n"
            "• TED: 1-4 horas uteis\\n"
            "• Boleto: 1-3 dias uteis"
        ),
        "reembolso": (
            "💰 *POLITICA DE REEMBOLSO*\\n"
            "━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
            "1. Arrependimento: reembolso em 7 dias\\n"
            "   antes do download.\\n\\n"
            "2. Problema tecnico: substituicao ou\\n"
            "   reembolso.\\n\\n"
            "3. Apos download: sem reembolso.\\n\\n"
            "4. Produto errado: reembolso integral.\\n\\n"
            "Solicite pelo suporte no Telegram."
        ),
    }

    texto = paginas.get(page, "Pagina nao encontrada.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Voltar", callback_data="institutional")],
        [InlineKeyboardButton("🏠 Menu Principal", callback_data="main_menu")],
    ])
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                texto, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )
        except Exception:
            await update.callback_query.message.reply_text(
                texto, parse_mode=ParseMode.MARKDOWN, reply_markup=kb
            )

'''
    idx = c.find("async def show_support")
    if idx > 0:
        c = c[:idx] + inst + "\n\n" + c[idx:]
        print("  Menu Institucional adicionado!")

# 3. Botao institucional no menu
old_kb = '[InlineKeyboardButton("\u2753 FAQ / Ajuda", callback_data="faq"),'
new_kb = '[InlineKeyboardButton("\U0001f4cb Institucional", callback_data="institutional"),'
if "institutional" not in c and old_kb in c:
    c = c.replace(old_kb, new_kb)
    print("  Botao Institucional adicionado ao menu!")

# 4. Handlers institucionais
old_faq = 'elif data == "faq":'
new_faq = '''elif data == "institutional":
            await show_institutional(update, context)
        elif data.startswith("inst_"):
            page = data.replace("inst_", "")
            await institutional_detail(update, context, page)
        elif data == "faq":'''
if 'elif data == "institutional":' not in c:
    c = c.replace(old_faq, new_faq)
    print("  Handlers institucionais adicionados!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("  bot.py: Sintaxe OK!")
except SyntaxError as e:
    print(f"  ERRO bot.py: {e}")
    shutil.copy("bot.py.backup_total", "bot.py")
    print("  Backup restaurado!")

# ══════════════════════════════════════════
# PARTE 2: CORRIGIR CATALOG.PY
# ══════════════════════════════════════════
print("\n[2/3] CORRIGINDO catalog.py...")

shutil.copy("catalog.py", "catalog.py.backup_total")
print("  Backup criado: catalog.py.backup_total")

with open("catalog.py", "r", encoding="utf-8") as f:
    c2 = f.read()

# Corrige imagens que nao tem URL ou estao erradas
correcoes_img = {
    "Windows 11 Pro - Licenca Vitalicia": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg",
    "Windows 10 Pro - Licenca Vitalicia": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg",
    "Windows 11 Home - Licenca Original": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg",
    "Ubuntu 24.04 LTS + Suporte": "https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg",
    "Windows Server 2022": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg",
    "Office 2021 Pro Plus": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg",
    "Office 2019 Pro Plus": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg",
    "Microsoft 365 Family": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Microsoft_365_%282022%29.svg",
    "Project 2021": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Microsoft_Project_2019_Logo.svg",
    "Visio 2021": "https://upload.wikimedia.org/wikipedia/commons/1/14/Microsoft_Office_Visio_%282019%E2%80%93present%29.svg",
    "Photoshop 2024": "https://upload.wikimedia.org/wikipedia/commons/a/af/Adobe_Photoshop_CC_icon.svg",
    "Illustrator 2024": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Adobe_Illustrator_CC_icon.svg",
    "Premiere Pro 2024": "https://upload.wikimedia.org/wikipedia/commons/4/40/Adobe_Premiere_Pro_CC_icon.svg",
    "After Effects 2024": "https://upload.wikimedia.org/wikipedia/commons/0/05/Adobe_After_Effects_CC_icon.svg",
    "Creative Cloud COMPLETO": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Adobe_Creative_Cloud_rainbow_icon.svg",
    "CorelDRAW": "https://upload.wikimedia.org/wikipedia/commons/3/30/Coreldraw_2020_logo.svg",
    "Canva Pro": "https://upload.wikimedia.org/wikipedia/commons/0/08/Canva_icon_2021.svg",
    "AutoCAD 2024": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg",
    "AutoCAD LT 2024": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg",
    "SketchUp Pro 2024": "https://upload.wikimedia.org/wikipedia/commons/5/55/SketchUp_logo.svg",
    "Revit 2024": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Revit_2017_logo.png",
    "3ds Max 2024": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Autodesk_3ds_Max_2014_logo.png",
    "Maya 2024": "https://upload.wikimedia.org/wikipedia/commons/6/68/Autodesk_Maya_2017_logo.png",
    "SolidWorks 2024": "https://upload.wikimedia.org/wikipedia/commons/d/d3/SolidWorks_Logo.svg",
    "Lumion 2024": "https://upload.wikimedia.org/wikipedia/commons/d/dc/Lumion_logo.png",
    "Norton 360": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Norton_AntiVirus_logo.png",
    "Kaspersky Premium": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Kaspersky_logo.svg",
    "Bitdefender Total": "https://upload.wikimedia.org/wikipedia/commons/9/97/Bitdefender_2019_logo.svg",
    "McAfee Total": "https://upload.wikimedia.org/wikipedia/commons/9/9b/McAfee_logo_%282017%29.svg",
    "ESET NOD32": "https://upload.wikimedia.org/wikipedia/commons/9/9f/ESET_logo.svg",
    "Malwarebytes Premium": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Malwarebytes_logo.svg",
    "AVG Internet": "https://upload.wikimedia.org/wikipedia/commons/5/5c/AVG_logo_2016.svg",
    "Avast Premium": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Avast_logo_2021.svg",
    "WinRAR Premium": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg",
    "CCleaner Professional": "https://upload.wikimedia.org/wikipedia/commons/5/55/CCleaner-Logo.svg",
    "Driver Booster": "https://www.iobit.com/themes/iobit/img/iobit-logo.svg",
    "SystemCare Pro": "https://www.iobit.com/themes/iobit/img/iobit-logo.svg",
    "AnyDesk Premium": "https://upload.wikimedia.org/wikipedia/commons/d/d8/AnyDesk_logo.svg",
    "TeamViewer Business": "https://upload.wikimedia.org/wikipedia/commons/3/35/TeamViewer_logo.svg",
    "IDM - Internet": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg",
    "Filmora 13": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Wondershare_logo_2.svg",
    "Camtasia 2024": "https://upload.wikimedia.org/wikipedia/commons/9/9c/TechSmith_Logo.png",
    "NordVPN Premium": "https://upload.wikimedia.org/wikipedia/commons/0/0e/NordVPN_logo.svg",
    "Netflix Premium 4K": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
    "Disney+ Premium": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
    "HBO Max": "https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg",
    "Amazon Prime Video": "https://upload.wikimedia.org/wikipedia/commons/1/11/Amazon_Prime_Video_logo.svg",
    "COMBO MEGA": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
    "Spotify Premium - 30": "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg",
    "Spotify Premium - 90": "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg",
    "YouTube Premium": "https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg",
    "Steam Gift Card R$ 50": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg",
    "Steam Gift Card R$ 100": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg",
    "PlayStation Plus": "https://upload.wikimedia.org/wikipedia/commons/0/00/PlayStation_logo.svg",
    "Xbox Game Pass": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg",
    "Google One 2TB": "https://upload.wikimedia.org/wikipedia/commons/c/c6/Google_One_logo.svg",
    "iCloud+ 2TB": "https://upload.wikimedia.org/wikipedia/commons/5/57/ICloud_logo.svg",
    "Dropbox Plus": "https://upload.wikimedia.org/wikipedia/commons/7/78/Dropbox_Icon.svg",
    "Curso Completo Excel": "https://upload.wikimedia.org/wikipedia/commons/8/83/Microsoft_Excel_2013-2019_logo.svg",
    "Curso Completo AutoCAD": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg",
}

img_corrigidas = 0
for chave, url in correcoes_img.items():
    if chave in c2:
        idx = c2.find(chave)
        if idx > 0:
            idx_img = c2.find("imagem_url", idx, idx + 800)
            if idx_img > 0:
                idx_ini = c2.find('"', idx_img + 12) + 1
                idx_fim = c2.find('"', idx_ini)
                if idx_fim > idx_ini:
                    url_velha = c2[idx_ini:idx_fim]
                    if url_velha != url:
                        c2 = c2[:idx_ini] + url + c2[idx_fim:]
                        img_corrigidas += 1

print(f"  {img_corrigidas} imagens corrigidas!")

# Adiciona 20 novos produtos
if '"id": 180' not in c2:
    novos = '''
    {"id": 180, "nome": "Windows 10 Pro OEM", "preco_original": 499.90, "preco_oferta": 59.90, "descricao": "Windows 10 Pro OEM. Ativacao via digital license.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 181, "nome": "Windows 11 Home OEM", "preco_original": 399.90, "preco_oferta": 49.90, "descricao": "Windows 11 Home OEM. Ativacao online rapida.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 182, "nome": "Windows 11 Pro OEM", "preco_original": 599.90, "preco_oferta": 69.90, "descricao": "Windows 11 Pro OEM. Para empresas e profissionais.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 183, "nome": "Windows 11 Pro + Office 2021 COMBO", "preco_original": 999.90, "preco_oferta": 129.90, "descricao": "COMBO: Windows 11 Pro + Office 2021 Pro Plus!", "categorias": ["Sistema Operacional", "Office"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 184, "nome": "Windows 10 Pro + Office 2019 COMBO", "preco_original": 799.90, "preco_oferta": 109.90, "descricao": "COMBO: Windows 10 Pro + Office 2019 Pro Plus.", "categorias": ["Sistema Operacional", "Office"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 185, "nome": "Linux Mint 22 + Suporte", "preco_original": 149.90, "preco_oferta": 39.90, "descricao": "Linux Mint 22 com suporte premium.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Linux_Mint_logo_without_wordmark.svg"},
    {"id": 186, "nome": "Fedora Workstation 40 + Suporte", "preco_original": 149.90, "preco_oferta": 39.90, "descricao": "Fedora 40 com suporte. Linux moderno.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/33/Fedora_logo.svg"},
    {"id": 187, "nome": "Microsoft Office 2016 Pro Plus", "preco_original": 999.90, "preco_oferta": 49.90, "descricao": "Office 2016 Pro Plus vitalicio.", "categorias": ["Office"], "oferta": True, "plataforma": "PC", "tipo": "Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"},
    {"id": 188, "nome": "Microsoft Office 2024 Pro Plus", "preco_original": 2499.90, "preco_oferta": 129.90, "descricao": "Office 2024 Pro Plus. Ultima versao!", "categorias": ["Office"], "oferta": True, "plataforma": "PC", "tipo": "Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"},
    {"id": 189, "nome": "Adobe Acrobat Pro DC Vitalicio", "preco_original": 1299.90, "preco_oferta": 99.90, "descricao": "Adobe Acrobat Pro. Editar PDFs profissionalmente.", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Adobe_Creative_Cloud_rainbow_icon.svg"},
    {"id": 190, "nome": "AutoCAD + SketchUp COMBO", "preco_original": 12999.90, "preco_oferta": 449.90, "descricao": "COMBO: AutoCAD 2024 + SketchUp Pro 2024.", "categorias": ["Engenharia"], "oferta": True, "plataforma": "PC", "tipo": "Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg"},
    {"id": 191, "nome": "Pacote Adobe + CorelDRAW COMPLETO", "preco_original": 7999.90, "preco_oferta": 599.90, "descricao": "Todos os Adobe + CorelDRAW. O mais completo!", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Adobe_Creative_Cloud_rainbow_icon.svg"},
    {"id": 192, "nome": "Gerenciador de Senhas Premium", "preco_original": 199.90, "preco_oferta": 34.90, "descricao": "Gerenciador de senhas seguro com criptografia.", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "Multi", "tipo": "Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},
    {"id": 193, "nome": "Editor de PDF Completo", "preco_original": 399.90, "preco_oferta": 29.90, "descricao": "Editor PDF profissional. Editar, juntar, converter.", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},
    {"id": 194, "nome": "Gravador de Tela e Audio Pro", "preco_original": 299.90, "preco_oferta": 39.90, "descricao": "Gravador profissional de tela e audio.", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},
    {"id": 195, "nome": "Curso Python do Zero ao Avancado", "preco_original": 597.00, "preco_oferta": 69.90, "descricao": "Aprenda Python completo. 100h + projetos + certificado.", "categorias": ["Curso"], "oferta": True, "plataforma": "Online", "tipo": "Curso", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"},
    {"id": 196, "nome": "Curso Photoshop 2024 Completo", "preco_original": 497.00, "preco_oferta": 59.90, "descricao": "Domine o Photoshop. 60h + projetos + certificado.", "categorias": ["Curso"], "oferta": True, "plataforma": "Online", "tipo": "Curso", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/Adobe_Photoshop_CC_icon.svg"},
    {"id": 197, "nome": "Curso SketchUp Pro Completo", "preco_original": 497.00, "preco_oferta": 79.90, "descricao": "SketchUp do zero ao avancado. 80h + certificado.", "categorias": ["Curso"], "oferta": True, "plataforma": "Online", "tipo": "Curso", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/SketchUp_logo.svg"},
    {"id": 198, "nome": "Curso Adobe Creative Cloud", "preco_original": 697.00, "preco_oferta": 99.90, "descricao": "Todos os Adobe na pratica. Photoshop, Illustrator, Premiere. 120h.", "categorias": ["Curso"], "oferta": True, "plataforma": "Online", "tipo": "Curso", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Adobe_Creative_Cloud_rainbow_icon.svg"},
    {"id": 199, "nome": "COMBO SUPREMO Windows+Office+Antivirus", "preco_original": 1499.90, "preco_oferta": 159.90, "descricao": "Windows 11 Pro + Office 2021 + Norton 360. Economia 90%!", "categorias": ["Sistema Operacional", "Office", "Antivirus"], "oferta": True, "plataforma": "PC", "tipo": "Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
'''
    idx2 = c2.rfind("]")
    if idx2 > 0:
        t = c2[:idx2].rstrip()
        if not t.endswith(","):
            t += ","
        c2 = t + novos + "\\n]" + c2[idx2+1:]
    print("  20 novos produtos adicionados!")
else:
    print("  Produtos ja existem!")

with open("catalog.py", "w", encoding="utf-8") as f:
    f.write(c2)

try:
    with open("catalog.py", "r", encoding="utf-8") as f:
        compile(f.read(), "catalog.py", "exec")
    print("  catalog.py: Sintaxe OK!")
except SyntaxError as e:
    print(f"  ERRO catalog.py: {e}")
    shutil.copy("catalog.py.backup_total", "catalog.py")
    print("  Backup restaurado!")

# ══════════════════════════════════════════
# PARTE 3: RESUMO FINAL
# ══════════════════════════════════════════
print("\n[3/3] VERIFICANDO TUDO...")

try:
    from catalog import GAMES_CATALOG
    total = len(GAMES_CATALOG)
    ofertas = len([g for g in GAMES_CATALOG if g["oferta"]])
    tipos = {}
    for g in GAMES_CATALOG:
        t = g.get("tipo", "Outro")
        tipos[t] = tipos.get(t, 0) + 1

    print(f"\n{'=' * 60}")
    print(f"  WAREARCADEBOT - RESUMO FINAL")
    print(f"{'=' * 60}")
    for tipo, qtd in sorted(tipos.items()):
        print(f"  {tipo:<25} {qtd:>3} produtos")
    print(f"{'─' * 60}")
    print(f"  {'TOTAL':<25} {total:>3} produtos")
    print(f"  {'EM OFERTA':<25} {ofertas:>3} produtos")
    print(f"{'=' * 60}")
    print(f"\n  Para rodar: python bot.py")
except Exception as e:
    print(f"  Erro ao contar: {e}")

print(f"\n{'=' * 60}")