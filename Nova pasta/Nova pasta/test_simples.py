import requests
import time

TOKEN = "8880569558:AAEtC-oePtV2aB46mw5pouNIhZbUPjosTYc"

print("🔄 Testando conexão com Telegram...")

for tentativa in range(1, 6):
    try:
        inicio = time.time()
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        response = requests.get(url, timeout=60)
        fim = time.time()
        
        print(f"✅ Tentativa {tentativa}: OK! ({fim - inicio:.2f}s)")
        print(f"   Resposta: {response.json()}")
        break
    except requests.exceptions.Timeout:
        print(f"❌ Tentativa {tentativa}: Timeout!")
    except Exception as e:
        print(f"❌ Tentativa {tentativa}: {e}")
    
    if tentativa < 5:
        print(f"⏳ Aguardando 5s antes da próxima tentativa...")
        time.sleep(5)