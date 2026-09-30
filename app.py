from fastapi import FastAPI
import os, base64, requests, uuid

app = FastAPI(title="Banque Bafoussam")

def get_momo_token():
    user_id = os.getenv("MTN_API_USER_ID")
    api_key = os.getenv("MTN_API_KEY")
    sub_key = os.getenv("MTN_SUBSCRIPTION_KEY")
    auth = base64.b64encode(f"{user_id}:{api_key}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Ocp-Apim-Subscription-Key": sub_key
    }
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    r = requests.post(url, headers=headers)
    return r.json()["access_token"]

@app.get("/")
def home():
    return {"message": "Banque Bafoussam OK"}

@app.get("/collection/token/")
def token():
    return {"access_token": get_momo_token()}

@app.post("/collect/")
def collect(phone: str, amount: str = "1000"):
    token = get_momo_token()
    ref = str(uuid.uuid4())
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Reference-Id": ref,
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": os.getenv("MTN_SUBSCRIPTION_KEY"),
        "Content-Type": "application/json"
    }
    body = {
        "amount": amount,
        "currency": "EUR",
        "externalId": "12345",
        "payer": {"partyIdType": "MSISDN", "partyId": phone},
        "payerMessage": "Paiement Banque Bafoussam",
        "payeeNote": "Merci"
    }
    r = requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay", headers=headers, json=body)
    return {"status": r.status_code, "reference": ref, "reponse": r.text}
