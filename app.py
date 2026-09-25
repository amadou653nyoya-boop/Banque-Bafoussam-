from flask import Flask
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

@app.route('/')
def maison():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM comptes")
    comptes = c.fetchall()
    conn.close()

    cards = ""
    for num, solde in comptes:
        s = f"{solde:,}".replace(",", " ")
        cards += f'<div class="card"><div class="numero">{num}</div><div class="solde">{s} FCFA</div></div>'

    return f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:Arial;background:#fff7ed;margin:0}}
.header{{background:linear-gradient(90deg,#ff6a00,#ee0979);color:white;padding:25px;text-align:center}}
.container{{padding:15px}}
.card{{background:white;border-radius:15px;padding:20px;margin-bottom:12px;box-shadow:0 4px 10px rgba(0,0,0,0.1);border-left:5px solid #ff6a00}}
.solde{{font-size:26px;font-weight:bold;color:#16a34a}}
.numero{{color:#666;font-size:13px}}
.btn{{display:block;background:#ff6a00;color:white;text-align:center;padding:15px;border-radius:10px;text-decoration:none;margin-top:10px;font-weight:bold}}
</style></head>
<body>
<div class="header"><h1>🏦 CAISSE BAFOUSSAM</h1><p>Banque Bafoussam OK - En Ligne</p></div>
<div class="container">{cards}<a class="btn" href="/">🔄 Actualiser</a></div>
</body></html>
"""

if __name__ == '__main__':
    app.run()
