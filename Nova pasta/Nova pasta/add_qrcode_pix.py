"""
ADICIONA QR CODE PIX DINAMICO NO BOT
"""
import shutil

print("=" * 60)
print("  ADICIONANDO QR CODE PIX AUTOMATICO")
print("=" * 60)

# Backup
shutil.copy("bot.py", "bot.py.backup_qrcode")
print("[OK] Backup criado")

with open("bot.py", "r", encoding="utf-8") as f:
    c = f.read()

# Adiciona funcao de gerar PIX no topo do arquivo
pix_function = '''

# ════════════════════════════════════════
# GERADOR DE PIX COM QR CODE
# ════════════════════════════════════════

def gerar_pix_payload(chave_pix, nome, cidade, valor, txid="WAREARCADE"):
    """Gera codigo PIX EMV (BR Code)."""
    def format_field(id_field, value):
        return f"{id_field:02d}{len(value):02d}{value}"

    # Limpa chave (so numeros para celular)
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


async def enviar_qrcode_pix(context, chat_id, valor, txid="WAREARCADE"):
    """Gera e envia QR Code PIX para o cliente."""
    try:
        import qrcode
        import io
        
        # Gera codigo PIX
        codigo_pix = gerar_pix_payload(
            chave_pix=PIX_CHAVE,
            nome=PIX_NOME,
            cidade=PIX_CIDADE,
            valor=valor,
            txid=txid
        )
        
        # Gera QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(codigo_pix)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Salva em buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Envia foto do QR Code
        caption = (
            f"💚 *QR CODE PIX*\\n\\n"
            f"💵 Valor: *R$ {valor:.2f}*\\n\\n"
            f"📱 *Como pagar:*\\n"
            f"1️⃣ Abra seu app do banco\\n"
            f"2️⃣ PIX → Ler QR Code\\n"
            f"3️⃣ Aponte para o codigo acima\\n"
            f"4️⃣ Confirme o pagamento\\n\\n"
            f"⚡ *Ou copie o codigo PIX:*"
        )
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=buffer,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Envia codigo PIX copiavel
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"`{codigo_pix}`",
            parse_mode=ParseMode.MARKDOWN
        )
        
        return True
    except Exception as e:
        logger.error(f"Erro ao gerar QR Code: {e}")
        return False

'''

# Adiciona a funcao antes da funcao main_async
if "def gerar_pix_payload" not in c:
    idx = c.find("async def main_async")
    if idx < 0:
        idx = c.find("def main()")
    
    if idx > 0:
        c = c[:idx] + pix_function + "\n\n" + c[idx:]
        print("[OK] Funcao QR Code PIX adicionada!")

# Modifica process_payment para enviar QR Code quando for PIX
old_pix_text = 'text += (\n            f"💚 *DADOS DO PIX*\\n\\n"'

if old_pix_text in c:
    # Adiciona chamada para enviar QR Code antes do return
    old_confirmar = """    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=confirm_purchase_keyboard()
    )"""
    
    new_confirmar = """    await update.callback_query.edit_message_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=confirm_purchase_keyboard()
    )
    
    # Envia QR Code se for PIX
    if method == "pix":
        try:
            await enviar_qrcode_pix(
                context=context,
                chat_id=update.callback_query.message.chat_id,
                valor=total,
                txid=f"PEDIDO{user_id}"
            )
        except Exception as e:
            logger.warning(f"Nao foi possivel gerar QR Code: {e}")"""
    
    # Substitui apenas a primeira ocorrencia em process_payment
    if "Envia QR Code se for PIX" not in c:
        c = c.replace(old_confirmar, new_confirmar, 1)
        print("[OK] QR Code sera enviado automaticamente no PIX!")

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(c)

# Valida sintaxe
try:
    with open("bot.py", "r", encoding="utf-8") as f:
        compile(f.read(), "bot.py", "exec")
    print("[OK] Sintaxe valida!")
    print("\n" + "=" * 60)
    print("  QR CODE PIX ADICIONADO COM SUCESSO!")
    print("=" * 60)
    print("\n  Agora quando o cliente escolher PIX:")
    print("  - Aparece os dados do PIX (como antes)")
    print("  - Aparece o QR CODE da imagem")
    print("  - Aparece o codigo PIX copia e cola")
    print("\n  Cliente pode:")
    print("  - Escanear QR Code (mais rapido)")
    print("  - Copiar codigo PIX")
    print("  - Usar a chave normal")
    print("\n  Rode: py bot.py")
    print("=" * 60)
except SyntaxError as e:
    print(f"[ERRO] {e}")
    shutil.copy("bot.py.backup_qrcode", "bot.py")
    print("[OK] Backup restaurado.")