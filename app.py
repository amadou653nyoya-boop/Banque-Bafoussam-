from flask import Flask, request, jsonify
import os, requests, base64, uuid
app = Flask(__name__)
MTN_USER_ID = os.getenv("MTN_API_USER_ID")
MTN_API_KEY = os.getenv("MTN_API_KEY")
MTN_SUB_KEY = os.getenv("MTN_SUBSCRIPTION_KEY")
def get_mtn_token():
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    auth = base64.b64encode(f"{MTN_USER_ID}:{MTN_API_KEY}".encode()).decode()
    headers = {"Ocp-Apim-Subscription-Key": MTN_SUB_KEY, "Authorization": f"Basic {auth}"}
    r = requests.post(url, headers=headers)
    return r.json().get("access_token")
@app.route('/')
def home():
    return f"<h1>Banque Bafoussam CONNECTEE</h1><p>ID: {MTN_USER_ID}</p><a href='/test-mtn'>Tester MTN</a>"
@app.route('/test-mtn')
def test_mtn():
    try:
        token = get_mtn_token()
        return f"CONNEXION REUSSIE ! Token OK: {token[:30]}... Tu peux recevoir de l'argent MTN."
    except Exception as e:
        return f"Erreur: {e}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
