import os, time, threading, requests
import yfinance as yf
from flask import Flask
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
app = Flask(__name__)
SYMBOLS = {"BTC-USD":"BTC", "ETH-USD":"ETH", "GC=F":"GOLD", "EURUSD=X":"EUR/USD"}

def send(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"HTML"}, timeout=10)
    except: pass

def get_signal(symbol):
    try:
        df = yf.download(symbol, period="2d", interval="1h", progress=False)
        if len(df) < 22: return None
        df["EMA9"] = df["Close"].ewm(span=9).mean()
        df["EMA21"] = df["Close"].ewm(span=21).mean()
        last, prev = df.iloc[-1], df.iloc[-2]
        price = float(last["Close"])
        if last["EMA9"] > last["EMA21"] and prev["EMA9"] <= prev["EMA21"]: return f"🟢 BUY {SYMBOLS[symbol]}\nPrezzo: {price:.2f}\nEMA9 sopra EMA21"
        if last["EMA9"] < last["EMA21"] and prev["EMA9"] >= prev["EMA21"]: return f"🔴 SELL {SYMBOLS[symbol]}\nPrezzo: {price:.2f}\nEMA9 sotto EMA21"
    except: pass
    return None

def loop():
    time.sleep(8)
    send("✅ <b>Candle AI V5 FULL Online!</b>\nCloud H24 attivo\nMarco - iPhone 17 Pro Max\n\n🎯 Scanner: BTC, ETH, GOLD, EUR/USD")
    while True:
        try:
            for s in SYMBOLS:
                sig = get_signal(s)
                if sig: send(sig + f"\n⏰ {datetime.now().strftime('%H:%M')}")
            time.sleep(900)
        except: time.sleep(60)

@app.route("/")
def home(): return "Candle AI V5 LIVE"
threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
