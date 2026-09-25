from flask import Flask, request
import sqlite3
app = Flask(__name__)
DB = "banque.db"
def init():
 con = sqlite3.connect(DB)
 con.execute("CREATE TABLE IF NOT EXISTS comptes (id TEXT PRIMARY KEY, solde INTEGER)")
 con.execute("INSERT OR IGNORE INTO comptes VALUES ('402000-00001', 960000)")
 con.execute("INSERT OR IGNORE INTO comptes VALUES ('CAISSE-BAFOUSSAM', 1990000)")
 con.commit()
 con.close()
init()
@app.route('/')
def home():
 con = sqlite3.connect(DB)
 data = con.execute("SELECT * FROM comptes").fetchall()
 con.close()
 page = "<html><meta name='viewport' content='width=device-width'><body style='font-family:Arial;background:#fff7ed'><h1 style='background:orange;color:white;padding:20px;text-align:center'>CAISSE BAFOUSSAM</h1><div style='max-width:500px;margin:auto;padding:15px'>"
 for num, solde in data:
  page += f"<div style='background:white;padding:15px;margin:10px;border-left:4px solid orange'><b>{num}</b><br><b style='color:green'>{solde} FCFA</b></div>"
 page += "<form action='/transfert' method='POST' style='background:white;padding:15px;border-radius:10px'><h3>Transfert</h3>"
 page += "De: <select name='de'><option>402000-00001</option><option>CAISSE-BAFOUSSAM</option></select><br>"
 page += "Vers: <select name='vers'><option>402000-00001</option><option>CAISSE-BAFOUSSAM</option></select><br>" page += "Montant: <input type='number' name='montant' required><br><button style='background:orange;color:white;width:100%;padding:12px;margin-top:10px'>TRANSFERER</button></form></div></body></html>"
 return page
@app.route('/transfert', methods=['POST'])
def transfert():
 de = request.form['de']
 vers = request.form['vers']
 montant = int(request.form['montant'])
 con = sqlite3.connect(DB)
 solde = con.execute("SELECT solde FROM comptes WHERE id=?", (de,)).fetchone()[0]
 if de == vers:
  con.close()
  return "Meme compte <a href='/'>Retour</a>"
 if solde < montant:
  con.close()
  return f"Solde insuffisant {solde} <a href='/'>Retour</a>"
 con.execute("UPDATE comptes SET solde=solde-? WHERE id=?", (montant, de))
 con.execute("UPDATE comptes SET solde=solde+? WHERE id=?", (montant, vers))
 con.commit()
 con.close()
 return f"OK {montant} envoye {de} vers {vers} <br><a href='/'>Retour</a>"
if __name__ == '__main__':
 app.run()
