"""
API REST para N8N - WareArcadeBot
Endpoints para automacoes de marketing
"""
from aiohttp import web
from database import get_connection
import json


async def api_carrinhos_abandonados(request):
    """Retorna carrinhos abandonados ha mais de 1 hora."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.telegram_id, 
            cust.nome_completo,
            cust.email,
            GROUP_CONCAT(c.game_name, ' | ') as jogos,
            SUM(c.price) as total,
            COUNT(c.id) as qtd_itens,
            MIN(c.added_at) as adicionado_em
        FROM cart c
        LEFT JOIN customers cust ON c.telegram_id = cust.telegram_id
        WHERE datetime(c.added_at) < datetime('now', '-1 hour')
        AND datetime(c.added_at) > datetime('now', '-3 days')
        GROUP BY c.telegram_id
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return web.json_response(rows)


async def api_clientes_ativos(request):
    """Clientes que interagiram nos ultimos 30 dias."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT telegram_id, nome_completo, email
        FROM customers
        WHERE datetime(updated_at) > datetime('now', '-30 days')
        AND nome_completo IS NOT NULL
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return web.json_response(rows)


async def api_clientes_inativos(request):
    """Clientes inativos ha 15+ dias."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT telegram_id, nome_completo
        FROM customers
        WHERE datetime(updated_at) < datetime('now', '-15 days')
        AND nome_completo IS NOT NULL
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return web.json_response(rows)


async def api_stats_diarias(request):
    """Estatisticas do dia para o admin."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as total, COALESCE(SUM(price), 0) as receita
        FROM orders
        WHERE date(created_at) = date('now') AND status = 'aprovado'
    """)
    vendas = dict(cursor.fetchone())
    
    cursor.execute("SELECT COUNT(*) as p FROM orders WHERE status = 'aguardando_aprovacao'")
    pendentes = dict(cursor.fetchone())["p"]
    
    cursor.execute("SELECT COUNT(*) as n FROM customers WHERE date(created_at) = date('now')")
    novos = dict(cursor.fetchone())["n"]
    
    cursor.execute("SELECT COUNT(DISTINCT telegram_id) as c FROM cart")
    carrinhos = dict(cursor.fetchone())["c"]
    
    conn.close()
    
    return web.json_response({
        "vendas_total": vendas["total"],
        "receita": round(vendas["receita"], 2),
        "pendentes": pendentes,
        "novos_clientes": novos,
        "carrinhos_ativos": carrinhos,
    })


def setup_api(app):
    app.router.add_get("/api/carrinhos-abandonados", api_carrinhos_abandonados)
    app.router.add_get("/api/clientes-ativos", api_clientes_ativos)
    app.router.add_get("/api/clientes-inativos", api_clientes_inativos)
    app.router.add_get("/api/stats-diarias", api_stats_diarias)


def run_api_server(port=8080):
    """Roda API em paralelo ao bot."""
    app = web.Application()
    setup_api(app)
    web.run_app(app, port=port, print=lambda *args: None)
