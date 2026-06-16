"""
===============================================
WareArcadeBot - Envio de Emails
===============================================
Módulo para envio de emails de confirmação
de compra com link de download.
===============================================
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD,
    EMAIL_FROM_NAME, STORE_NAME, STORE_WEBSITE,
    STORE_EMAIL, DOWNLOAD_LINK_EXPIRY_HOURS
)


def send_purchase_email(to_email: str, customer_name: str, order_code: str,
                         game_name: str, price: float, download_url: str,
                         expiry_hours: int = None) -> bool:
    """
    Envia email de confirmação de compra com link de download.
    Retorna True se enviado com sucesso, False caso contrário.
    """
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("⚠️ Credenciais de email não configuradas. Email não enviado.")
        return False

    if expiry_hours is None:
        expiry_hours = DOWNLOAD_LINK_EXPIRY_HOURS

    subject = f"✅ Compra Confirmada! {game_name} - {STORE_NAME}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0a0a0a;
                color: #ffffff;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #1a1a2e;
                border-radius: 12px;
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #00b4d8, #0077b6);
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                color: white;
            }}
            .header p {{
                margin: 5px 0 0;
                color: #e0f7ff;
                font-size: 14px;
            }}
            .content {{
                padding: 30px;
            }}
            .success-badge {{
                background: linear-gradient(135deg, #00c853, #00e676);
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 25px;
            }}
            .order-details {{
                background-color: #16213e;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
            }}
            .order-details h3 {{
                color: #00b4d8;
                margin-top: 0;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #1a1a3e;
            }}
            .detail-label {{
                color: #8899aa;
            }}
            .detail-value {{
                color: #ffffff;
                font-weight: bold;
            }}
            .download-section {{
                background: linear-gradient(135deg, #1a1a4e, #16213e);
                border: 2px solid #00b4d8;
                border-radius: 12px;
                padding: 25px;
                text-align: center;
                margin: 25px 0;
            }}
            .download-btn {{
                display: inline-block;
                background: linear-gradient(135deg, #00b4d8, #0077b6);
                color: white;
                padding: 15px 40px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
                margin: 15px 0;
            }}
            .warning {{
                background-color: #3d2000;
                border-left: 4px solid #ff9800;
                padding: 12px 15px;
                border-radius: 4px;
                margin: 20px 0;
                font-size: 13px;
                color: #ffcc80;
            }}
            .footer {{
                background-color: #0f0f23;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 Ware Arcade</h1>
                <p>Nerd Games - Sua loja de jogos digitais</p>
            </div>
            <div class="content">
                <div class="success-badge">
                    ✅ COMPRA CONFIRMADA COM SUCESSO!
                </div>

                <p>Olá, <strong>{customer_name}</strong>! 👋</p>
                <p>Sua compra foi processada com sucesso. Confira os detalhes abaixo:</p>

                <div class="order-details">
                    <h3>📋 Detalhes do Pedido</h3>
                    <div class="detail-row">
                        <span class="detail-label">Código do Pedido:</span>
                        <span class="detail-value">{order_code}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Jogo:</span>
                        <span class="detail-value">{game_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Valor Pago:</span>
                        <span class="detail-value">R$ {price:.2f}</span>
                    </div>
                </div>

                <div class="download-section">
                    <h3>⬇️ Faça seu Download</h3>
                    <p>Clique no botão abaixo para baixar seu jogo:</p>
                    <a href="{download_url}" class="download-btn">
                        🎮 BAIXAR JOGO
                    </a>
                    <p style="font-size: 12px; color: #8899aa; margin-top: 10px;">
                        Link válido por <strong>{expiry_hours} horas</strong>
                    </p>
                </div>

                <div class="warning">
                    ⚠️ <strong>Importante:</strong> O link de download expira em
                    <strong>{expiry_hours} horas</strong>. Faça o download o quanto
                    antes! Em caso de problemas, entre em contato conosco.
                </div>

                <p>Se tiver qualquer dúvida, entre em contato:</p>
                <p>📧 {STORE_EMAIL}</p>
                <p>🌐 {STORE_WEBSITE}</p>
            </div>
            <div class="footer">
                <p>© 2025 {STORE_NAME}. Todos os direitos reservados.</p>
                <p>Este email foi enviado automaticamente. Não responda a este email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Versão texto simples
    text_body = f"""
    ✅ COMPRA CONFIRMADA - {STORE_NAME}

    Olá, {customer_name}!

    Sua compra foi confirmada com sucesso!

    📋 DETALHES DO PEDIDO:
    • Código: {order_code}
    • Jogo: {game_name}
    • Valor: R$ {price:.2f}

    ⬇️ LINK DE DOWNLOAD:
    {download_url}

    ⚠️ O link expira em {expiry_hours} horas!

    Dúvidas? Contato: {STORE_EMAIL}
    Site: {STORE_WEBSITE}
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_USER}>"
        msg["To"] = to_email

        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"✅ Email enviado com sucesso para {to_email}")
        return True

    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False


def send_multiple_purchase_email(to_email: str, customer_name: str,
                                  orders: list) -> bool:
    """Envia email com múltiplos pedidos (carrinho completo)."""
    if not orders:
        return False

    if len(orders) == 1:
        order = orders[0]
        return send_purchase_email(
            to_email, customer_name, order["order_code"],
            order["game_name"], order["price"], order["download_url"]
        )

    # Múltiplos pedidos
    subject = f"✅ {len(orders)} Compras Confirmadas! - {STORE_NAME}"
    total = sum(o["price"] for o in orders)

    games_html = ""
    games_text = ""
    for order in orders:
        games_html += f"""
        <div class="order-details" style="margin-bottom: 15px;">
            <div class="detail-row">
                <span class="detail-label">Código:</span>
                <span class="detail-value">{order['order_code']}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Jogo:</span>
                <span class="detail-value">{order['game_name']}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Valor:</span>
                <span class="detail-value">R$ {order['price']:.2f}</span>
            </div>
            <div style="text-align:center; margin-top:10px;">
                <a href="{order['download_url']}" style="color:#00b4d8;">
                    ⬇️ Download: {order['game_name']}
                </a>
            </div>
        </div>
        """
        games_text += f"""
    • {order['game_name']} - R$ {order['price']:.2f}
      Código: {order['order_code']}
      Download: {order['download_url']}
        """

    html_body = f"""
    <html><body style="font-family: Arial; background: #1a1a2e; color: white; padding: 20px;">
    <div style="max-width:600px; margin:auto; background:#16213e; border-radius:12px; padding:30px;">
        <h1 style="color:#00b4d8; text-align:center;">🎮 Ware Arcade - Nerd Games</h1>
        <div style="background:#00c853; color:white; padding:15px; border-radius:8px; text-align:center; font-size:18px;">
            ✅ {len(orders)} COMPRAS CONFIRMADAS!
        </div>
        <p>Olá, <strong>{customer_name}</strong>!</p>
        <p>Seus pedidos foram confirmados. Total: <strong>R$ {total:.2f}</strong></p>
        {games_html}
        <p style="background:#3d2000; border-left:4px solid #ff9800; padding:12px; border-radius:4px; color:#ffcc80;">
            ⚠️ Links válidos por {DOWNLOAD_LINK_EXPIRY_HOURS} horas!
        </p>
        <p style="text-align:center; color:#666; font-size:12px;">
            © 2025 {STORE_NAME} | {STORE_EMAIL}
        </p>
    </div>
    </body></html>
    """

    text_body = f"""
    ✅ {len(orders)} COMPRAS CONFIRMADAS - {STORE_NAME}

    Olá, {customer_name}!
    Total: R$ {total:.2f}

    SEUS JOGOS:
    {games_text}

    ⚠️ Links expiram em {DOWNLOAD_LINK_EXPIRY_HOURS} horas!
    Contato: {STORE_EMAIL}
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{EMAIL_FROM_NAME} <{EMAIL_USER}>"
        msg["To"] = to_email
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"✅ Email com {len(orders)} pedidos enviado para {to_email}")
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False