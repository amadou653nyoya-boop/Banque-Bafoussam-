from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import os, uuid, requests

app = FastAPI()

# --- TES SOLDES ---
COMPTES = [
    {"numero": "531000-00001", "nom": "CAISSE PHYSIQUE", "solde": "51,980,000 F"},
    {"numero": "402000-00001", "nom": "CLIENT MARCHE B 1", "solde": "950,000 F"},
    {"numero": "402000-00002", "nom": "CLIENT MARCHE B 2", "solde": "30,000 F"},
    {"numero": "101000-00001", "nom": "CAPITAL - MONNAIE SCRIPTURALE", "solde": "50,000,000 F"},
]

# --- CONFIG MTN ---
SUB_KEY = os.getenv("MOMO_SUBSCRIPTION_KEY")
API_USER = os.getenv("MOMO_API_USER")
API_KEY = os.getenv("MOMO_API_KEY")
BASE_URL = "https://sandbox.momodeveloper.mtn.com"

def get_momo_token():
    url = f"{BASE_URL}/collection/token/"
    headers = {"Ocp-Apim-Subscription-Key": SUB_KEY}
    auth = (API_USER, API_KEY)
    r = requests.post(url, headers=headers, auth=auth)
    r.raise_for_status()
    return r.json()["access_token"]

@app.get("/", response_class=HTMLResponse)
def banque():
    rows = "".join([f"<tr><td>{c['numero']}</td><td>{c['nom']}</td><td>{c['solde']}</td></tr>" for c in COMPTES])
    return f"""
    <h2>Banque Bafoussam - 50.000.000F</h2>
    <table border=1 cellpadding=5><tr><th>Numero</th><th>Nom</th><th>Solde</th></tr>{rows}</table>
    <br><a href='/test-momo' style='background:#FFCC00;padding:10px;text-decoration:none;font-weight:bold'>💳 Testeur MTN - PAIEMENT REEL</a>
    <p>CAISSE: 51,980,000F | Statut: CONNECTEE</p>
    """

@app.get("/test-momo", response_class=HTMLResponse)
def test_form():
    return """
    <h2>Test MTN MoMo REEL</h2>
    <form method='post'>
        Numero MTN (format 2376XXXXXXXX):<br><input name='phone' value='237670000000' required><br><br>
        Montant FCFA:<br><input name='amount' type='number' value='100' required><br><br>
        <button type='submit'>Debiter maintenant</button>
    </form>
    <br><a href='/'>Retour Banque</a>
    """

@app.post("/test-momo", response_class=HTMLResponse)
def test_pay(phone: str = Form(...), amount: str = Form(...)):
    try:
        token = get_momo_token()
        ref = str(uuid.uuid4())
        url = f"{BASE_URL}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": ref,
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": SUB_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "amount": amount,
            "currency": "EUR" if "sandbox" in BASE_URL else "XAF",
            "externalId": "BFSSM"+ref[:8],
            "payer": {"partyIdType": "MSISDN", "partyId": phone.replace("+","")},
            "payerMessage": "Test Banque Bafoussam",
            "payeeNote": "Test"
        }
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 202:
            return f"<h3 style='color:green'>✅ REQUETE ENVOYEE!</h3><p>Ref: {ref}</p><p>Regarde ton telephone {phone}, tu dois approuver le paiement de {amount}.</p><a href='/'>Retour</a>"
        else:
            return f"<h3 style='color:red'>Erreur MTN: {r.status_code}</h3><p>{r.text}</p><a href='/test-momo'>Reessayer</a>"
    except Exception as e:
        return f"<h3>Erreur: {e}</h3><a href='/test-momo'>Reessayer</a>"
