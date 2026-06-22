"""
===============================================
WareArcadeBot - CATÁLOGO COMPLETO
===============================================
🎮 Jogos PC + 🖥️ Sistemas + 📄 Office +
🎨 Design + 🏗️ Engenharia + 🔒 Antivírus +
🛠️ Ferramentas + 🎬 Streaming + 🎵 Música +
🎁 Gift Cards + ☁️ Cloud + 🎓 Cursos
===============================================
"""

# ── Categorias disponíveis ──
CATEGORIES = [
    # Jogos
    "Ação", "Aventura", "Casuais", "Construção", "Corrida",
    "Destaques", "Esporte", "Estratégia", "Indie", "Mais Vendidos",
    "Puzzle", "RPG", "Simulação", "Terror",
    # Software
    "Sistema Operacional", "Office", "Design", "Engenharia",
    "Antivírus", "Ferramentas", "Edição de Vídeo", "Produtividade",
    "Streaming", "Música", "Gift Card", "Cloud", "Curso",
]

# ════════════════════════════════════════
# CATÁLOGO COMPLETO
# ════════════════════════════════════════

GAMES_CATALOG = [
    # ═══════════════════════════════════════════════════════
    # 🎮 JOGOS PARA PC (92 produtos - IDs 1 a 92)
    # ═══════════════════════════════════════════════════════
    {"id": 1, "nome": "House Flipper Remastered Collection", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Coleção remasterizada do simulador de reformas.", "categorias": ["Simulação", "Casuais"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/613100/header.jpg"},
    {"id": 2, "nome": "Manor Lords", "preco_original": 26.90, "preco_oferta": 26.90, "descricao": "Jogo de estratégia e construção medieval.", "categorias": ["Estratégia", "Construção"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1363080/header.jpg"},
    {"id": 3, "nome": "Need for Speed Most Wanted Limited Edition", "preco_original": 34.90, "preco_oferta": 24.90, "descricao": "Edição limitada do clássico de corrida.", "categorias": ["Corrida", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/24740/header.jpg"},
    {"id": 4, "nome": "Marvel Ultimate Alliance", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "RPG de ação com heróis Marvel.", "categorias": ["Ação", "RPG"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/56000/header.jpg"},
    {"id": 5, "nome": "Red Dead Redemption 2", "preco_original": 64.90, "preco_oferta": 38.90, "descricao": "Ação e aventura no Velho Oeste.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1174180/header.jpg"},
    {"id": 6, "nome": "MEGAMAN COMPLETE PACK", "preco_original": 69.90, "preco_oferta": 29.90, "descricao": "Pacote completo da franquia Mega Man.", "categorias": ["Ação", "Indie"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/363440/header.jpg"},
    {"id": 7, "nome": "Hollow Knight Silksong", "preco_original": 29.90, "preco_oferta": 19.90, "descricao": "Sequência do aclamado metroidvania.", "categorias": ["Ação", "Aventura", "Indie"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1030300/header.jpg"},
    {"id": 8, "nome": "Farming Simulator 22 Platinum", "preco_original": 39.90, "preco_oferta": 32.90, "descricao": "Simulação agrícola com conteúdo extra.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1248130/header.jpg"},
    {"id": 9, "nome": "Pragmata", "preco_original": 62.99, "preco_oferta": 34.90, "descricao": "Ação/aventura futurista da Capcom.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1382330/header.jpg"},
    {"id": 10, "nome": "Subnautica 2", "preco_original": 48.99, "preco_oferta": 29.90, "descricao": "Simulação subaquática offline.", "categorias": ["Aventura", "Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/848450/header.jpg"},
    {"id": 11, "nome": "Tomb Raider IV-VI Remastered", "preco_original": 24.90, "preco_oferta": 24.90, "descricao": "Remaster dos clássicos Tomb Raider.", "categorias": ["Ação", "Aventura"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2508510/header.jpg"},
    {"id": 12, "nome": "Sonic Frontiers Digital Deluxe", "preco_original": 44.99, "preco_oferta": 29.90, "descricao": "Ação e plataforma em mundo aberto com o Sonic!", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1237320/header.jpg"},
    {"id": 13, "nome": "Core Keeper + Todas DLCs", "preco_original": 24.90, "preco_oferta": 24.90, "descricao": "Survival sandbox com todas as expansões.", "categorias": ["Aventura", "Indie"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1621690/header.jpg"},
    {"id": 14, "nome": "Spyro Reignited Trilogy", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Trilogia remasterizada do dragão Spyro.", "categorias": ["Ação", "Aventura", "Casuais"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/996580/header.jpg"},
    {"id": 15, "nome": "Marvel Cosmic Invasion", "preco_original": 39.90, "preco_oferta": 26.90, "descricao": "Ação com heróis cósmicos da Marvel.", "categorias": ["Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2630700/header.jpg"},
    {"id": 16, "nome": "GTA Vice City Definitive", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Versão definitiva do clássico GTA Vice City.", "categorias": ["Ação", "Aventura"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1547000/header.jpg"},
    {"id": 17, "nome": "PES 2013", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Simulador de futebol clássico de 2013.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/207580/header.jpg"},
    {"id": 18, "nome": "Stellar Blade", "preco_original": 54.90, "preco_oferta": 34.90, "descricao": "Ação em terceira pessoa futurista.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3489700/header.jpg"},
    {"id": 19, "nome": "Tony Hawks Pro Skater 1+2", "preco_original": 54.90, "preco_oferta": 29.90, "descricao": "Remaster dos clássicos de skate.", "categorias": ["Esporte", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2725150/header.jpg"},
    {"id": 20, "nome": "Farming Simulator 22 Year 1 Bundle", "preco_original": 36.90, "preco_oferta": 29.90, "descricao": "Bundle com primeiro ano de conteúdo.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1248130/header.jpg"},
    {"id": 21, "nome": "The Witcher 3 Complete Edition", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "RPG completo com todas as expansões.", "categorias": ["RPG", "Aventura", "Destaques", "Mais Vendidos"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg"},
    {"id": 22, "nome": "FIFA 12 + UEFA EURO 2012", "preco_original": 36.99, "preco_oferta": 29.90, "descricao": "Futebol com a Eurocopa 2012.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/47900/header.jpg"},
    {"id": 23, "nome": "Dead Space Remake", "preco_original": 64.99, "preco_oferta": 32.90, "descricao": "Terror espacial refeito do zero.", "categorias": ["Terror", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1693980/header.jpg"},
    {"id": 24, "nome": "Assetto Corsa Rally", "preco_original": 49.99, "preco_oferta": 27.90, "descricao": "Simulador de corrida de rali.", "categorias": ["Corrida", "Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/244210/header.jpg"},
    {"id": 25, "nome": "Prison Architect Total Lockdown", "preco_original": 57.99, "preco_oferta": 34.90, "descricao": "Simulador de prisão completo.", "categorias": ["Simulação", "Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/233450/header.jpg"},
    {"id": 26, "nome": "Slay the Spire 2", "preco_original": 29.99, "preco_oferta": 19.90, "descricao": "Roguelike de cartas (sequência).", "categorias": ["Indie", "Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/646570/header.jpg"},
    {"id": 27, "nome": "FORZA HORIZON 6", "preco_original": 72.90, "preco_oferta": 37.90, "descricao": "Corrida em mundo aberto.", "categorias": ["Corrida", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1551360/header.jpg"},
    {"id": 28, "nome": "TOMB RAIDER I-III REMASTERED", "preco_original": 32.90, "preco_oferta": 19.90, "descricao": "Remaster dos primeiros Tomb Raider.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2478970/header.jpg"},
    {"id": 29, "nome": "Kingdom Come Deliverance II", "preco_original": 62.90, "preco_oferta": 32.90, "descricao": "RPG histórico medieval realista.", "categorias": ["RPG", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1771300/header.jpg"},
    {"id": 30, "nome": "EUROPA UNIVERSALIS V", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Grande estratégia mundial.", "categorias": ["Estratégia"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3450310/header.jpg"},
    {"id": 31, "nome": "Elden Ring", "preco_original": 45.90, "preco_oferta": 32.90, "descricao": "RPG de ação em mundo aberto.", "categorias": ["RPG", "Ação", "Destaques", "Mais Vendidos"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg"},
    {"id": 32, "nome": "Elden Ring Nightreign Deluxe", "preco_original": 54.90, "preco_oferta": 29.90, "descricao": "Edição de luxo com conteúdo extra.", "categorias": ["RPG", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2622380/header.jpg"},
    {"id": 33, "nome": "Sekiro Shadows Die Twice GOTY", "preco_original": 39.90, "preco_oferta": 29.90, "descricao": "Ação e desafio no Japão feudal.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/814380/header.jpg"},
    {"id": 34, "nome": "Elden Ring + Shadow Of The Erdtree", "preco_original": 72.90, "preco_oferta": 36.90, "descricao": "Jogo base + expansão completa.", "categorias": ["RPG", "Ação", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2778580/header.jpg"},
    {"id": 35, "nome": "Crash Bandicoot 4", "preco_original": 42.90, "preco_oferta": 29.90, "descricao": "Plataforma com o marsupial louco.", "categorias": ["Ação", "Aventura", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1453090/header.jpg"},
    {"id": 36, "nome": "Resident Evil 2 Remake Deluxe", "preco_original": 49.90, "preco_oferta": 29.90, "descricao": "Terror e sobrevivência em Raccoon City.", "categorias": ["Terror", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/883710/header.jpg"},
    {"id": 37, "nome": "The Sims 2 Legacy Collection", "preco_original": 27.90, "preco_oferta": 27.90, "descricao": "Clássico simulador de vida.", "categorias": ["Simulação", "Casuais"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3314060/header.jpg"},
    {"id": 38, "nome": "Victoria 3", "preco_original": 46.90, "preco_oferta": 32.90, "descricao": "Grande estratégia do século XIX.", "categorias": ["Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/529340/header.jpg"},
    {"id": 39, "nome": "Ready Or Not + Todas DLCs", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Tático policial com todas expansões.", "categorias": ["Ação", "Simulação"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1144200/header.jpg"},
    {"id": 40, "nome": "LEGO Batman O Legado", "preco_original": 62.90, "preco_oferta": 34.90, "descricao": "Ação e humor com LEGO Batman.", "categorias": ["Ação", "Aventura", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/502820/header.jpg"},
    {"id": 41, "nome": "Crash Bandicoot N Sane Trilogy", "preco_original": 42.90, "preco_oferta": 29.90, "descricao": "Trilogia clássica remasterizada.", "categorias": ["Ação", "Aventura", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/731490/header.jpg"},
    {"id": 42, "nome": "Command Conquer Generals Zero Hour", "preco_original": 34.90, "preco_oferta": 22.90, "descricao": "RTS de guerra moderna.", "categorias": ["Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2229850/header.jpg"},
    {"id": 43, "nome": "Cities Skylines", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Simulador de cidade.", "categorias": ["Simulação", "Construção"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg"},
    {"id": 44, "nome": "Spider-Man Miles Morales", "preco_original": 42.40, "preco_oferta": 29.90, "descricao": "Ação com o Homem-Aranha Miles Morales.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1817190/header.jpg"},
    {"id": 45, "nome": "Resident Evil Requiem Deluxe", "preco_original": 72.90, "preco_oferta": 37.90, "descricao": "Edição de luxo de Resident Evil Requiem.", "categorias": ["Terror", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3273940/header.jpg"},
    {"id": 46, "nome": "inZOI", "preco_original": 59.90, "preco_oferta": 34.90, "descricao": "Simulador de vida realista.", "categorias": ["Simulação", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2456740/header.jpg"},
    {"id": 47, "nome": "GTA San Andreas Definitive", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Clássico do GTA remasterizado.", "categorias": ["Ação", "Aventura"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1547001/header.jpg"},
    {"id": 48, "nome": "The Last of Us Part II Remastered", "preco_original": 59.90, "preco_oferta": 36.90, "descricao": "Ação e drama pós-apocalíptico.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2531310/header.jpg"},
    {"id": 49, "nome": "Cities Skylines Collection", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Coleção do simulador de cidades.", "categorias": ["Simulação", "Construção"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg"},
    {"id": 50, "nome": "Age of Empires III Definitive", "preco_original": 34.90, "preco_oferta": 27.90, "descricao": "RTS histórico com todas expansões.", "categorias": ["Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/933110/header.jpg"},
    {"id": 51, "nome": "FIFA 14", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Futebol clássico FIFA 14.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/241950/header.jpg"},
    {"id": 52, "nome": "Euro Truck Simulator 2 Gold + BR", "preco_original": 39.90, "preco_oferta": 32.90, "descricao": "Simulador de caminhão com mapas BR!", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/227300/header.jpg"},
    {"id": 53, "nome": "eFootball PES 2021", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Futebol com Season Update 2021.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1394960/header.jpg"},
    {"id": 54, "nome": "FIFA 17", "preco_original": 44.90, "preco_oferta": 32.90, "descricao": "FIFA 17 com modo Journey.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/468120/header.jpg"},
    {"id": 55, "nome": "The Sims 4 Todas DLCs", "preco_original": 34.90, "preco_oferta": 34.90, "descricao": "The Sims 4 completo com todas as DLCs.", "categorias": ["Simulação", "Casuais", "Mais Vendidos"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1222670/header.jpg"},
    {"id": 56, "nome": "The Sims 4 Digital Deluxe", "preco_original": 34.90, "preco_oferta": 34.90, "descricao": "Edição Digital Deluxe do The Sims 4.", "categorias": ["Simulação", "Casuais"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1222670/header.jpg"},
    {"id": 57, "nome": "The Sims 3 Com Expansões", "preco_original": 39.90, "preco_oferta": 29.90, "descricao": "The Sims 3 completo com expansões.", "categorias": ["Simulação", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/47890/header.jpg"},
    {"id": 58, "nome": "FIFA 22", "preco_original": 39.90, "preco_oferta": 32.90, "descricao": "FIFA 22 com HyperMotion Technology.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1506830/header.jpg"},
    {"id": 59, "nome": "Cities Skylines 2 Ultimate", "preco_original": 69.90, "preco_oferta": 34.90, "descricao": "Simulador de cidade de última geração.", "categorias": ["Simulação", "Construção"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/949230/header.jpg"},
    {"id": 60, "nome": "FIFA 21", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "FIFA 21 - futebol eletrônico.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1313860/header.jpg"},
    {"id": 61, "nome": "Euro Truck Simulator 2 + Mapas BR", "preco_original": 39.90, "preco_oferta": 32.90, "descricao": "Simulador de caminhão com mapas BR.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/227300/header.jpg"},
    {"id": 62, "nome": "FIFA 23", "preco_original": 39.90, "preco_oferta": 29.90, "descricao": "FIFA 23 - o último FIFA antes do EA FC.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1811260/header.jpg"},
    {"id": 63, "nome": "Farming Simulator 25 + DLCs", "preco_original": 58.60, "preco_oferta": 34.90, "descricao": "O mais novo Farming Simulator!", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2300320/header.jpg"},
    {"id": 64, "nome": "Cities Skylines II + DLCs", "preco_original": 64.90, "preco_oferta": 34.90, "descricao": "Cities Skylines II completo.", "categorias": ["Simulação", "Construção"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/949230/header.jpg"},
    {"id": 65, "nome": "FIFA 15", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "FIFA 15 - futebol clássico.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/289600/header.jpg"},
    {"id": 66, "nome": "House Flipper Com DLCs", "preco_original": 49.90, "preco_oferta": 29.90, "descricao": "House Flipper completo com DLCs.", "categorias": ["Simulação", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/613100/header.jpg"},
    {"id": 67, "nome": "FIFA 13", "preco_original": 42.90, "preco_oferta": 29.90, "descricao": "FIFA 13 clássico.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/207580/header.jpg"},
    {"id": 68, "nome": "SnowRunner Premium Edition", "preco_original": 44.90, "preco_oferta": 32.90, "descricao": "Simulador off-road extremo.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1465360/header.jpg"},
    {"id": 69, "nome": "Mario Kart 8 Deluxe", "preco_original": 64.90, "preco_oferta": 29.90, "descricao": "Corrida divertida com personagens da Nintendo!", "categorias": ["Corrida", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://upload.wikimedia.org/wikipedia/en/8/8c/Mario_Kart_8_Deluxe.jpg"},
    {"id": 70, "nome": "FIFA 20", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "FIFA 20 com modo Volta Football.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1056600/header.jpg"},
    {"id": 71, "nome": "Plants Vs Zombies Replanted", "preco_original": 4.24, "preco_oferta": 4.24, "descricao": "Defenda seu jardim dos zumbis!", "categorias": ["Casuais", "Puzzle"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3950/header.jpg"},
    {"id": 72, "nome": "House Flipper 2 + DLCs", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "House Flipper 2 com todas as DLCs.", "categorias": ["Simulação", "Casuais"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1190970/header.jpg"},
    {"id": 73, "nome": "The Last of Us Part I", "preco_original": 48.90, "preco_oferta": 33.90, "descricao": "A jornada épica de Joel e Ellie.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1888930/header.jpg"},
    {"id": 74, "nome": "Dispatch", "preco_original": 39.90, "preco_oferta": 17.90, "descricao": "Simulador de central de emergências.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3527290/header.jpg"},
    {"id": 75, "nome": "Spider-Man Remastered", "preco_original": 42.40, "preco_oferta": 29.90, "descricao": "Marvel's Spider-Man Remasterizado.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1817070/header.jpg"},
    {"id": 76, "nome": "God Of War 2018 Dublado", "preco_original": 39.90, "preco_oferta": 29.90, "descricao": "Kratos e Atreus em PT-BR!", "categorias": ["Ação", "Aventura", "Destaques", "Mais Vendidos"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1593500/header.jpg"},
    {"id": 77, "nome": "Farming Simulator 25 Online", "preco_original": 58.60, "preco_oferta": 34.90, "descricao": "Farming Simulator 25 com modo Online!", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2300320/header.jpg"},
    {"id": 78, "nome": "FIFA 18", "preco_original": 49.90, "preco_oferta": 32.90, "descricao": "FIFA 18 com modo The Journey.", "categorias": ["Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/611500/header.jpg"},
    {"id": 79, "nome": "Resident Evil 4 Remake Gold", "preco_original": 59.90, "preco_oferta": 32.90, "descricao": "Remake do clássico RE4.", "categorias": ["Terror", "Ação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2050650/header.jpg"},
    {"id": 80, "nome": "FIFA 19", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "FIFA 19 com UEFA Champions League.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/918360/header.jpg"},
    {"id": 81, "nome": "Age of Mythology Retold", "preco_original": 44.90, "preco_oferta": 29.90, "descricao": "RTS mitológico remasterizado.", "categorias": ["Estratégia"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1934680/header.jpg"},
    {"id": 82, "nome": "SimCity 5 (2013)", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Construa e gerencie sua cidade.", "categorias": ["Simulação", "Construção"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://upload.wikimedia.org/wikipedia/en/9/9a/SimCity_2013_Limited_Edition_cover.jpg"},
    {"id": 83, "nome": "Cities Skylines Deluxe", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "Edição Deluxe do Cities Skylines.", "categorias": ["Simulação", "Construção"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg"},
    {"id": 84, "nome": "FIFA 16", "preco_original": 29.90, "preco_oferta": 29.90, "descricao": "FIFA 16 - futebol clássico.", "categorias": ["Esporte"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/353650/header.jpg"},
    {"id": 85, "nome": "God of War Ragnarok Dublado", "preco_original": 69.90, "preco_oferta": 32.90, "descricao": "Continuação épica de Kratos. PT-BR!", "categorias": ["Ação", "Aventura", "Destaques", "Mais Vendidos"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2322010/header.jpg"},
    {"id": 86, "nome": "Red Dead Redemption", "preco_original": 49.90, "preco_oferta": 29.90, "descricao": "O clássico do Velho Oeste.", "categorias": ["Ação", "Aventura"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2668510/header.jpg"},
    {"id": 87, "nome": "Spider-Man 2", "preco_original": 74.90, "preco_oferta": 36.90, "descricao": "Marvel's Spider-Man 2 para PC.", "categorias": ["Ação", "Aventura", "Destaques"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/2944550/header.jpg"},
    {"id": 88, "nome": "Project Zomboid", "preco_original": 22.90, "preco_oferta": 22.90, "descricao": "Simulador de sobrevivência zumbi.", "categorias": ["Simulação", "Indie"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/108600/header.jpg"},
    {"id": 89, "nome": "NASCAR 25", "preco_original": 59.90, "preco_oferta": 29.90, "descricao": "Corrida NASCAR com carros reais!", "categorias": ["Corrida", "Esporte"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/3158220/header.jpg"},
    {"id": 90, "nome": "Farming Simulator 22", "preco_original": 36.90, "preco_oferta": 29.90, "descricao": "Simulação agrícola completa.", "categorias": ["Simulação"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1248130/header.jpg"},
    {"id": 91, "nome": "Need for Speed Heat Deluxe", "preco_original": 32.90, "preco_oferta": 32.90, "descricao": "Corrida noturna de rua. Deluxe!", "categorias": ["Corrida", "Ação"], "oferta": False, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/1222680/header.jpg"},
    {"id": 92, "nome": "The Sims 3 Com Todas DLCs", "preco_original": 49.90, "preco_oferta": 29.90, "descricao": "The Sims 3 completo com todas as DLCs!", "categorias": ["Simulação", "Casuais"], "oferta": True, "plataforma": "PC", "tipo": "🎮 Jogo", "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/47890/header.jpg"},

    # ═══════════════════════════════════════════════════════
    # 🖥️ SISTEMAS OPERACIONAIS
    # ═══════════════════════════════════════════════════════
    {"id": 100, "nome": "Windows 11 Pro - Licença Vitalícia", "preco_original": 899.90, "preco_oferta": 89.90, "descricao": "Licença ORIGINAL Windows 11 Pro vitalícia. Ativação online garantida.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 101, "nome": "Windows 10 Pro - Licença Vitalícia", "preco_original": 699.90, "preco_oferta": 69.90, "descricao": "Licença ORIGINAL Windows 10 Pro vitalícia. Compatível com qualquer PC.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 102, "nome": "Windows 11 Home - Licença Original", "preco_original": 599.90, "preco_oferta": 59.90, "descricao": "Licença Windows 11 Home original. Perfeito para uso doméstico.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},
    {"id": 103, "nome": "Ubuntu 24.04 LTS + Suporte", "preco_original": 149.90, "preco_oferta": 49.90, "descricao": "Ubuntu 24.04 LTS com suporte premium. Instalação assistida + tutoriais.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "PC", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg"},
    {"id": 104, "nome": "Windows Server 2022 Standard", "preco_original": 2999.90, "preco_oferta": 499.90, "descricao": "Windows Server 2022. Para empresas e servidores corporativos.", "categorias": ["Sistema Operacional"], "oferta": True, "plataforma": "Server", "tipo": "🖥️ Sistema", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Windows_logo_-_2012.svg"},

    # ═══════════════════════════════════════════════════════
    # 📄 MICROSOFT OFFICE
    # ═══════════════════════════════════════════════════════
    {"id": 110, "nome": "Microsoft Office 2021 Pro Plus", "preco_original": 1899.90, "preco_oferta": 79.90, "descricao": "Office 2021 Pro Plus VITALÍCIO. Word, Excel, PowerPoint, Outlook, Access.", "categorias": ["Office", "Produtividade"], "oferta": True, "plataforma": "PC", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"},
    {"id": 111, "nome": "Microsoft Office 2019 Pro Plus", "preco_original": 1599.90, "preco_oferta": 69.90, "descricao": "Office 2019 Pro Plus completo. Licença vitalícia.", "categorias": ["Office", "Produtividade"], "oferta": True, "plataforma": "PC", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Microsoft_Office_logo_%282019%E2%80%93present%29.svg"},
    {"id": 112, "nome": "Microsoft 365 Family (6 usuários)", "preco_original": 449.90, "preco_oferta": 199.90, "descricao": "Microsoft 365 para 6 pessoas. 1TB OneDrive cada.", "categorias": ["Office", "Produtividade"], "oferta": True, "plataforma": "Multi", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Microsoft_365_%282022%29.svg"},
    {"id": 113, "nome": "Microsoft Project 2021 Pro", "preco_original": 4999.90, "preco_oferta": 299.90, "descricao": "MS Project 2021 para gerenciamento profissional.", "categorias": ["Office", "Produtividade"], "oferta": True, "plataforma": "PC", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Microsoft_Project_2019_Logo.svg"},
    {"id": 114, "nome": "Microsoft Visio 2021 Pro", "preco_original": 2999.90, "preco_oferta": 199.90, "descricao": "MS Visio 2021 para diagramas profissionais.", "categorias": ["Office", "Produtividade"], "oferta": True, "plataforma": "PC", "tipo": "📄 Office", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/1/14/Microsoft_Office_Visio_%282019%E2%80%93present%29.svg"},

    # ═══════════════════════════════════════════════════════
    # 🎨 ADOBE / DESIGN
    # ═══════════════════════════════════════════════════════
    {"id": 120, "nome": "Adobe Photoshop 2024 - Lifetime", "preco_original": 1899.90, "preco_oferta": 149.90, "descricao": "Adobe Photoshop 2024 completo. Sem mensalidade!", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "🎨 Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/Adobe_Photoshop_CC_icon.svg"},
    {"id": 121, "nome": "Adobe Illustrator 2024 - Lifetime", "preco_original": 1799.90, "preco_oferta": 139.90, "descricao": "Adobe Illustrator 2024. Design vetorial profissional.", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "🎨 Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/f/fb/Adobe_Illustrator_CC_icon.svg"},
    {"id": 122, "nome": "Adobe Premiere Pro 2024", "preco_original": 1999.90, "preco_oferta": 169.90, "descricao": "Adobe Premiere Pro 2024. Edição de vídeo Hollywood.", "categorias": ["Edição de Vídeo"], "oferta": True, "plataforma": "PC", "tipo": "🎬 Vídeo", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/4/40/Adobe_Premiere_Pro_CC_icon.svg"},
    {"id": 123, "nome": "Adobe After Effects 2024", "preco_original": 1999.90, "preco_oferta": 169.90, "descricao": "Adobe After Effects 2024. Animação e VFX.", "categorias": ["Edição de Vídeo", "Design"], "oferta": True, "plataforma": "PC", "tipo": "🎬 Vídeo", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/05/Adobe_After_Effects_CC_icon.svg"},
    {"id": 124, "nome": "Adobe Creative Cloud COMPLETO", "preco_original": 4999.90, "preco_oferta": 399.90, "descricao": "Pacote Adobe COMPLETO: 20+ apps profissionais!", "categorias": ["Design", "Edição de Vídeo"], "oferta": True, "plataforma": "PC", "tipo": "🎨 Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Adobe_Creative_Cloud_rainbow_icon.svg"},
    {"id": 125, "nome": "CorelDRAW Graphics Suite 2024", "preco_original": 2499.90, "preco_oferta": 199.90, "descricao": "CorelDRAW 2024 completo. Design vetorial.", "categorias": ["Design"], "oferta": True, "plataforma": "PC", "tipo": "🎨 Design", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/30/Coreldraw_2020_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🏗️ ENGENHARIA / 3D
    # ═══════════════════════════════════════════════════════
    {"id": 130, "nome": "AutoCAD 2024 - Profissional", "preco_original": 9999.90, "preco_oferta": 299.90, "descricao": "AutoCAD 2024 completo. Software CAD #1 do mundo.", "categorias": ["Engenharia"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg"},
    {"id": 131, "nome": "AutoCAD LT 2024", "preco_original": 4999.90, "preco_oferta": 199.90, "descricao": "AutoCAD LT 2024. Versão 2D profissional.", "categorias": ["Engenharia"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/4/45/Autocad-Logo.svg"},
    {"id": 132, "nome": "SketchUp Pro 2024 - Vitalício", "preco_original": 2999.90, "preco_oferta": 249.90, "descricao": "SketchUp Pro 2024. Modelagem 3D arquitetônica.", "categorias": ["Engenharia", "Design"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/SketchUp_logo.svg"},
    {"id": 133, "nome": "Revit 2024 Profissional", "preco_original": 11999.90, "preco_oferta": 399.90, "descricao": "Autodesk Revit 2024. BIM profissional.", "categorias": ["Engenharia"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Revit_2017_logo.png"},
    {"id": 134, "nome": "3ds Max 2024", "preco_original": 9999.90, "preco_oferta": 349.90, "descricao": "Autodesk 3ds Max 2024. Modelagem e renderização 3D.", "categorias": ["Engenharia", "Design"], "oferta": True, "plataforma": "PC", "tipo": "🏗️ Engenharia", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Autodesk_3ds_Max_2014_logo.png"},

    # ═══════════════════════════════════════════════════════
    # 🔒 ANTIVÍRUS
    # ═══════════════════════════════════════════════════════
    {"id": 140, "nome": "Norton 360 Deluxe (5 dispositivos)", "preco_original": 399.90, "preco_oferta": 89.90, "descricao": "Norton 360 Deluxe. Antivírus + VPN + Senhas. 5 dispositivos.", "categorias": ["Antivírus"], "oferta": True, "plataforma": "Multi", "tipo": "🔒 Segurança", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Norton_AntiVirus_logo.png"},
    {"id": 141, "nome": "Kaspersky Premium (5 dispositivos)", "preco_original": 349.90, "preco_oferta": 79.90, "descricao": "Kaspersky Premium. Proteção total + VPN ilimitada.", "categorias": ["Antivírus"], "oferta": True, "plataforma": "Multi", "tipo": "🔒 Segurança", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Kaspersky_logo.svg"},
    {"id": 142, "nome": "Bitdefender Total Security", "preco_original": 399.90, "preco_oferta": 89.90, "descricao": "Bitdefender Total Security. Melhor antivírus em testes.", "categorias": ["Antivírus"], "oferta": True, "plataforma": "Multi", "tipo": "🔒 Segurança", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/Bitdefender_2019_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🛠️ FERRAMENTAS
    # ═══════════════════════════════════════════════════════
    {"id": 150, "nome": "WinRAR Premium - Vitalício", "preco_original": 149.90, "preco_oferta": 29.90, "descricao": "WinRAR Premium vitalício. Compactador #1 do mundo!", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "🛠️ Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},
    {"id": 151, "nome": "CCleaner Professional Plus", "preco_original": 199.90, "preco_oferta": 39.90, "descricao": "CCleaner Pro Plus. Limpeza + otimização + recuperação.", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "🛠️ Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/5/55/CCleaner-Logo.svg"},
    {"id": 152, "nome": "IDM - Internet Download Manager", "preco_original": 99.90, "preco_oferta": 24.90, "descricao": "IDM vitalício. Acelera downloads em 5x!", "categorias": ["Ferramentas"], "oferta": True, "plataforma": "PC", "tipo": "🛠️ Ferramenta", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/8d/WinRAR_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🎬 STREAMING
    # ═══════════════════════════════════════════════════════
    {"id": 160, "nome": "Netflix Premium 4K - 30 dias", "preco_original": 55.90, "preco_oferta": 19.90, "descricao": "Netflix Premium 4K Ultra HD por 30 dias. 4 telas simultâneas!", "categorias": ["Streaming"], "oferta": True, "plataforma": "Multi", "tipo": "🎬 Streaming", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"},
    {"id": 161, "nome": "Disney+ Premium - 30 dias", "preco_original": 33.90, "preco_oferta": 14.90, "descricao": "Disney+ Premium 4K. Marvel, Star Wars, Pixar, National Geographic.", "categorias": ["Streaming"], "oferta": True, "plataforma": "Multi", "tipo": "🎬 Streaming", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🎵 MÚSICA
    # ═══════════════════════════════════════════════════════
    {"id": 165, "nome": "Spotify Premium - 30 dias", "preco_original": 21.90, "preco_oferta": 9.90, "descricao": "Spotify Premium individual 30 dias. Sem anúncios + offline.", "categorias": ["Música"], "oferta": True, "plataforma": "Multi", "tipo": "🎵 Música", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg"},

    # ═══════════════════════════════════════════════════════
    # 🎁 GIFT CARDS
    # ═══════════════════════════════════════════════════════
    {"id": 168, "nome": "Steam Gift Card R$ 50", "preco_original": 50.00, "preco_oferta": 42.90, "descricao": "Cartão Steam R$ 50,00. Entrega instantânea.", "categorias": ["Gift Card"], "oferta": True, "plataforma": "PC", "tipo": "🎁 Gift Card", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # ☁️ CLOUD
    # ═══════════════════════════════════════════════════════
    {"id": 172, "nome": "Google One 2TB - 1 ano", "preco_original": 449.90, "preco_oferta": 189.90, "descricao": "Google One 2TB por 1 ano. Drive, Gmail, Fotos.", "categorias": ["Cloud"], "oferta": True, "plataforma": "Multi", "tipo": "☁️ Cloud", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/c/c6/Google_One_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🎓 CURSOS
    # ═══════════════════════════════════════════════════════
    {"id": 175, "nome": "Curso Completo Excel Avançado", "preco_original": 397.00, "preco_oferta": 47.90, "descricao": "Curso completo Excel: Básico ao VBA + Dashboards. 80h.", "categorias": ["Curso", "Produtividade"], "oferta": True, "plataforma": "Online", "tipo": "🎓 Curso", "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/8/83/Microsoft_Excel_2013-2019_logo.svg"},

    # ═══════════════════════════════════════════════════════
    # 🧪 PRODUTO DE TESTE
    # ═══════════════════════════════════════════════════════
    {
        "id": 999,
        "nome": "🧪 TESTE DO ARI - R$ 1,50",
        "preco_original": 1.50,
        "preco_oferta": 1.50,
        "descricao": "✅ Produto de teste para validar o fluxo completo de compra!\n\n➡️ Adicione ao carrinho\n➡️ Finalize com PIX\n➡️ Envie o comprovante\n➡️ Receba o link de download\n\n🎯 Perfeito para testar todo o sistema!",
        "categorias": ["Destaques"],
        "oferta": True,
        "plataforma": "PC",
        "tipo": "🧪 Teste",
        "imagem_url": "https://cdn.akamai.steamstatic.com/steam/apps/440/header.jpg"
    },
]


# ════════════════════════════════════════
# FUNÇÕES DO CATÁLOGO
# ════════════════════════════════════════

def get_game_by_id(game_id):
    """Retorna um produto pelo ID."""
    for game in GAMES_CATALOG:
        if game["id"] == game_id:
            return game
    return None


def search_games(query):
    """Busca produtos pelo nome."""
    query_lower = query.lower()
    return [g for g in GAMES_CATALOG if query_lower in g["nome"].lower()]


def get_games_by_category(category):
    """Retorna produtos de uma categoria."""
    return [g for g in GAMES_CATALOG if category in g["categorias"]]


def get_offers():
    """Retorna produtos em oferta."""
    return [g for g in GAMES_CATALOG if g["oferta"]]


def get_only_games():
    """Apenas jogos."""
    return [g for g in GAMES_CATALOG if g.get("tipo") == "🎮 Jogo"]


def get_only_software():
    """Apenas softwares."""
    return [g for g in GAMES_CATALOG if g.get("tipo") != "🎮 Jogo"]


def get_by_type(tipo):
    """Por tipo específico."""
    return [g for g in GAMES_CATALOG if g.get("tipo") == tipo]


def format_price(game):
    """Formata o preço."""
    if game["oferta"] and game["preco_original"] != game["preco_oferta"]:
        return f"~R$ {game['preco_original']:.2f}~ → *R$ {game['preco_oferta']:.2f}* 🏷️"
    return f"*R$ {game['preco_oferta']:.2f}*"


def get_game_display(game):
    """Display formatado."""
    tag_oferta = " 🔥 OFERTA!" if game["oferta"] else ""
    preco = format_price(game)
    cats = ", ".join(game["categorias"])
    tipo = game.get("tipo", "🎮 Jogo")
    return (
        f"{tipo} *{game['nome']}*{tag_oferta}\n"
        f"💰 {preco}\n"
        f"🖥️ Plataforma: {game['plataforma']}\n"
        f"🏷️ Categorias: {cats}\n"
        f"📝 {game['descricao']}"
    )