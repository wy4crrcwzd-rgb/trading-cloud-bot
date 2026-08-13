import os, time, threading, requests
from flask import Flask

TOKEN=os.getenv("TELEGRAM_TOKEN")
CHAT=os.getenv("CHAT_ID")
app=Flask(__name__)

@app.route("/")
def home():
 return "Candle AI Live"

def send(m):
 try:
  requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",data={"chat_id":CHAT,"text":m,"parse_mode":"Markdown"},timeout=10)
 except: pass

def loop():
 send("✅ *Candle AI V5 Online!*\nCloud H24 attivo\nMarco - iPhone 17 Pro Max")
 while True:
  print("Scan...")
  time.sleep(300)

threading.Thread(target=loop,daemon=True).start()
app.run(host="0.0.0.0",port=int(os.getenv("PORT",10000)))
