"""
===============================================
WareArcadeBot - Gerador de QR Code PIX
===============================================
Geração dinâmica de QR Code para pagamentos PIX
===============================================
"""

import qrcode
import io
from config import PIX_CHAVE, PIX_NOME, PIX_CIDADE


def gerar_pix_payload(chave_pix, nome, cidade, valor, txid="WAREARCADE"):
    """
    Gera o payload EMV do PIX (BR Code)
    """
    def format_field(id_field, value):
        return f"{id_field:02d}{len(value):02d}{value}"

    # Limpa a chave (apenas números para celular)
    chave_limpa = chave_pix.replace("(", "").replace(")", "").replace(" ", "").replace("-", "").replace(".", "")
    
    # Para celular, adiciona +55
    if len(chave_limpa) == 11:
        chave_limpa = "+55" + chave_limpa

    # Campos PIX
    payload_format = format_field(0, "01")
    merchant_account = format_field(0, "BR.GOV.BCB.PIX") + format_field(1, chave_limpa)
    merchant_account_field = format_field(26, merchant_account)
    merchant_category = format_field(52, "0000")
    transaction_currency = format_field(53, "986")
    transaction_amount = format_field(54, f"{valor:.2f}")
    country_code = format_field(58, "BR")
    merchant_name = format_field(59, nome[:25])
    merchant_city = format_field(60, cidade[:15])
    additional_data = format_field(62, format_field(5, txid[:25]))

    # Monta payload sem CRC
    payload_sem_crc = (
        payload_format + merchant_account_field + merchant_category +
        transaction_currency + transaction_amount + country_code +
        merchant_name + merchant_city + additional_data + "6304"
    )

    # Calcula CRC16
    def calcular_crc16(payload):
        crc = 0xFFFF
        for byte in payload.encode("utf-8"):
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                crc &= 0xFFFF
        return format(crc, "04X")

    crc = calcular_crc16(payload_sem_crc)
    return payload_sem_crc + crc


def generate_qr_code_pix(valor, txid="WAREARCADE"):
    """
    Gera a imagem do QR Code PIX e retorna o buffer da imagem e o payload
    """
    codigo_pix = gerar_pix_payload(
        chave_pix=PIX_CHAVE,
        nome=PIX_NOME,
        cidade=PIX_CIDADE,
        valor=valor,
        txid=txid
    )
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(codigo_pix)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer, codigo_pix


async def enviar_qrcode_pix(context, chat_id, valor, txid="WAREARCADE"):
    """
    Envia o QR Code PIX para o chat do Telegram
    """
    try:
        buffer, codigo_pix = generate_qr_code_pix(valor, txid)
        
        caption = (
            f"💚 *QR CODE PIX*\n\n"
            f"💵 Valor: *R$ {valor:.2f}*\n\n"
            f"📱 *Como pagar:*\n"
            f"1️⃣ Abra seu app do banco\n"
            f"2️⃣ PIX → Ler QR Code\n"
            f"3️⃣ Aponte para o código acima\n"
            f"4️⃣ Confirme o pagamento\n\n"
            f"⚡ *Ou copie o código PIX:*"
        )
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=buffer,
            caption=caption,
            parse_mode="Markdown"
        )
        
        # Envia o código copiável
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"`{codigo_pix}`",
            parse_mode="Markdown"
        )
        
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar/enviar QR Code: {e}")
        return False