request
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
 h = "<html><body style='font-family:Arial'>"
 h += "<h1 style='background:orange;color:white;padding:20px'>CAISSE BAFOUSSAM</h1>"
 for n,s in data:
  h += f"<p><b>{n}</b> : {s} FCFA</p>"
 h += "<form action='/transfert' method='POST'>"
 h += "De: <select name='de'><option>402000-00001</option><option>CAISSE-BAFOUSSAM</option></select><br>"
 h += "Vers: <select name='vers'><option>402000-00001</option><option>CAISSE-BAFOUSSAM</option></select><br>"
 h += "Montant: <input type='number' name='montant' required><br>"
 h += "<button style='background:orange;padding:10px'>TRANSFERER</button></form></body></html>"
 return h  
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
 return f"OK {montant} de {de} vers {vers} <br><a href='/'>Retour</a
