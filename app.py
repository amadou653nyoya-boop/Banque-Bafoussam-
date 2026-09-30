from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()
comptes = {
    "531000-00001": {"nom": "CAISSE PHYSIQUE", "solde": 51980000},
    "402000-00001": {"nom": "CLIENT MARCHE B 1", "solde": 950000},
    "402000-00002": {"nom": "CLIENT MARCHE B 2", "solde": 30000},
    "101000-00001": {"nom": "CAPITAL - MONNAIE SCRIPTURALE", "solde": 50000000},
}
@app.get("/", response_class=HTMLResponse)
def home():
    html = "<h1>Banque Bafoussam - 50.000.000F</h1><table border=1><tr><th>Numero</th><th>Nom</th><th>Solde</th></tr>"
    for num, info in comptes.items():
        html += f"<tr><td>{num}</td><td>{info['nom']}</td><td>{info['solde']:,} F</td></tr>"
    html += "</table><br><a href='/test-mtn'>Testeur MTN - CONNEXION REUSSIE</a>"
    return html
