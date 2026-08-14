import os, time, threading, requests, yfinance as yf
from flask import Flask
from datetime import datetime
TOKEN=os.getenv("TELEGRAM_TOKEN"); CHAT_ID=os.getenv("CHAT_ID")
app=Flask(__name__)

def send(m):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":CHAT_ID,"text":m,"parse_mode":"HTML"},timeout=10)
    except Exception as e: print(e)

def check():
    try:
        df=yf.download("GC=F", period="1d", interval="5m", progress=False, auto_adjust=True)
        if len(df)<20: return f"⚠️ ORO: Dati insufficienti len={len(df)}"
        df["EMA5"]=df["Close"].ewm(span=5).mean()
        df["EMA13"]=df["Close"].ewm(span=13).mean()
        c=float(df["Close"].iloc[-1]); e5=float(df["EMA5"].iloc[-1]); e13=float(df["EMA13"].iloc[-1])
        diff = (e5-e13)/c*100
        
        if e5>e13:
            return f"🟢 GOLD {c:.2f}\nTrend rialzista +{diff:.3f}%\nEMA5 {e5:.2f} > EMA13 {e13:.2f}\nSegnale BUY attivo - puoi entrare long con SL 0.2%"
        else:
            return f"🔴 GOLD {c:.2f}\nTrend ribassista {diff:.3f}%\nEMA5 {e5:.2f} < EMA13 {e13:.2f}\nSegnale SELL attivo - puoi entrare short con SL 0.2%"
    except Exception as e:
        return f"❌ Errore: {e}"

def loop():
    time.sleep(5)
    send("✅ <b>FIX ORO ATTIVO - Marco</b>\nOra ti manda segnali veri ogni 5 min\nNon più 0 previsioni!")
    while True:
        try:
            msg=check()
            send(msg+f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(300)
        except: time.sleep(30)

@app.route("/")
def home(): return "FIX LIVE"
threading.Thread(target=loop, daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
