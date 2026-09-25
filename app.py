 flask import Flask, request
import sqlite3
app = Flask(__name__)
DB = "banque.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS comptes (id TEXT PRIMARY KEY, solde INTEGER)")
    c.execute("INSERT OR IGNORE INTO comptes VALUES ('402000-00001', 960000)")
    c.execute("INSERT OR IGNORE INTO comptes VALUES ('CAISSE-BAFOUSSAM', 1990000)")
    conn.commit()
    conn.close()
init_db()

def get_html(msg=""):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM comptes")
    comptes = c.fetchall()
    conn.close()
    cards=""
    options=""
    for num,solde in comptes:
        s=f"{solde:,}".replace(","," ")
        cards+=f'<div style="background:white;border-radius:15px;padding:20px;margin-bottom:12px;box-shadow:0 4px 10px rgba(0,0,0,0.1);border-left:5px solid #ff6a00"><div style="color:#666;font-size:13px">{num}</div><div style="font-size:22px;font-weight:bold;color:#16a34a">{s} FCFA</div></div>'
        options+=f'<option value="{num}">{num}</option>'
    alert=f'<div style="background:#dcfce7;color:#166534;padding:15px;border-radius:10px;text-align:center;margin-bottom:15px;font-weight:bold">{msg}</div>' if msg else ''
    return f"<html><head><meta name='viewport
