from flask import Flask, request, jsonify
import sqlite3, os
app = Flask(__name__)
DB = "banque.db"
def init_db():
 conn = sqlite3.connect(DB)
 c = conn.cursor()
 c.execute("CREATE TABLE IF NOT EXISTS comptes (numero TEXT PRIMARY KEY, solde INTEGER)")
 c.execute("INSERT OR IGNORE INTO comptes VALUES ('402000-00001', 960000)")
 c.execute("INSERT OR IGNORE INTO comptes VALUES ('CAISSE-BAFOUSSAM', 1990000)")
 conn.commit(); conn.close()
init_db()
@app.route("/")
def home():
 conn = sqlite3.connect(DB); c = conn.cursor()
 c.execute("SELECT * FROM comptes"); d = c.fetchall(); conn.close()
 h="<h1>Banque Bafoussam OK</h1>"
 for n,s in d: h+=f"<p>{n} : {s} FCFA</p>"
 return h
@app.route("/webhook/notchpay", methods=["POST"])
def webhook():
 data=request.json
 try:
  m=int(data.get("amount",0)); compte=data.get("custom_field") or "402000-00001"
  if m>0:
   conn=sqlite3.connect(DB); c=conn.cursor()
   c.execute("UPDATE comptes SET solde=solde+? WHERE numero=?", (m, compte))
   c.execute("UPDATE comptes SET solde=solde+? WHERE numero='CAISSE-BAFOUSSAM'", (m,))
   conn.commit(); conn.close()
   return jsonify({"ok":True})
 except Exception as e: return jsonify({"error":str(e)}),500
 return jsonify({"ok":True})
if __name__=="__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
