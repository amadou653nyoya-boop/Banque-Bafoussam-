from flask import Flask
import requests

app = Flask(__name__)

# --- TA PAGE D'ACCUEIL ---
@app.route('/')
def home():
    return "Banque Bafoussam est en ligne ! Va sur /setup-mtn pour finir MTN"

# --- ETAPE 2: RECUPERER LA CLE SECRETE API_KEY ---
@app.route('/setup-mtn')
def setup_mtn():
    sub_key = "ba9611de565f4dc4b710a5359e05f797"
    api_user_id = "190c8d40-5779-441d-9564-1fa699c75b59"  # celui que tu as déjà réussi avec Status 201

    # On demande la API_KEY à MTN
    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{api_user_id}/apikey"
    headers = {
        "Ocp-Apim-Subscription-Key": sub_key
    }
    r = requests.post(url, headers=headers)
    
    try:
        data = r.json()
        api_key = data.get('apiKey', 'Non trouvé')
    except:
        api_key = r.text

    return f"""
    <h1>ETAPE 2 REUSSIE</h1>
    <p><b>Status:</b> {r.status_code}</p>
    <p><b>API_USER_ID:</b> {api_user_id}</p>
    <p><b>API_KEY:</b> {api_key}</p>
    <hr>
    <p>Copie ces 2 valeurs dans Render > Environment:</p>
    <p>MTN_API_USER_ID = {api_user_id}</p>
    <p>MTN_API_KEY = {api_key}</p>
    <p>MTN_SUBSCRIPTION_KEY = {sub_key}</p>
    """

# --- ETAPE 3: TESTER QUE CA MARCHE (obtenir le Token) ---
@app.route('/test-token')
def test_token():
    import base64
    sub_key = "ba9611de565f4dc4b710a5359e05f797"
    api_user_id = "190c8d40-5779-441d-9564-1fa699c75b59"
    # Tu mettras ta nouvelle API_KEY ici après l'avoir copiée
    api_key = "COLLE_ICI_TA_API_KEY_QUE_TU_VIENS_D_OBTENIR"

    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    auth_str = f"{api_user_id}:{api_key}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Ocp-Apim-Subscription-Key": sub_key,
        "Authorization": f"Basic {auth_b64}"
    }
    r = requests.post(url, headers=headers)
    return f"Status Token: {r.status_code}<br>Response: {r.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
