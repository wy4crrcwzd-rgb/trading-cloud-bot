import os, time, threading, requests
import yfinance as yf
from flask import Flask
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
app = Flask(__name__)

# ORO TURBO SCALPING
SYMBOL = "GC=F"
NAME = "GOLD"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"HTML"}, timeout=10)
    except: pass

def get_gold_signal():
    try:
        # 5 minuti = veloce!
        df = yf.download(SYMBOL, period="1d", interval="5m", progress=False)
        if len(df) < 30: return None
        
        df["EMA5"] = df["Close"].ewm(span=5).mean()
        df["EMA13"] = df["Close"].ewm(span=13).mean()
        df["RSI"] = 100 - (100 / (1 + df["Close"].diff().clip(lower=0).rolling(14).mean() / (-df["Close"].diff().clip(upper=0).rolling(14).mean())))

        last = df.iloc[-1]
        prev = df.iloc[-2]
        price = float(last["Close"])
        rsi = float(last["RSI"])

        # BUY veloce
        if last["EMA5"] > last["EMA13"] and prev["EMA5"] <= prev["EMA13"] and rsi < 70:
            sl = price * 0.998  # -0.2% stop
            tp = price * 1.004  # +0.4% take profit
            return f"🟢 <b>BUY GOLD VELOCE</b>\n💰 Prezzo: {price:.2f}\n📈 RSI: {rsi:.1f}\nEMA5 incrocia sopra\n\n🎯 TP: {tp:.2f} (+0.4%)\n🛑 SL: {sl:.2f} (-0.2%)\n⏱️ Scalp 5m"

        # SELL veloce
        if last["EMA5"] < last["EMA13"] and prev["EMA5"] >= prev["EMA13"] and rsi > 30:
            sl = price * 1.002
            tp = price * 0.996
            return f"🔴 <b>SELL GOLD VELOCE</b>\n💰 Prezzo: {price:.2f}\n📉 RSI: {rsi:.1f}\nEMA5 incrocia sotto\n\n🎯 TP: {tp:.2f} (-0.4%)\n🛑 SL: {sl:.2f} (+0.2%)\n⏱️ Scalp 5m"
    except Exception as e:
        print(e)
    return None

def loop():
    time.sleep(5)
    send("⚡️ <b>GOLD TURBO ONLINE!</b>\nMarco - Modalità Scalping Veloce\n\n🥇 Solo ORO - 5m\nControllo ogni 3 min\nTP +0.4% | SL -0.2%")
    while True:
        try:
            sig = get_gold_signal()
            if sig:
                send(sig + f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(180) # 3 minuti
        except:
            time.sleep(30)

@app.route("/")
def home(): return "GOLD TURBO LIVE"
threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
