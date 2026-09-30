fastapi import FastAPI
import os
import base64
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Banque Bafoussam API OK"}

@app.get("/collection/token/")
@app.post("/collection/token/")
def get_token():
    user_id = os.getenv("MTN_API_USER_ID")
    api_key = os.getenv("MTN_API_KEY")
    sub_key = os.getenv("MTN_SUBSCRIPTION_KEY")

    if not user_id or not api_key or not sub_key:
        return {"detail": "Variables Render manquantes"}

    auth_str = f"{user_id}:{api_key}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Ocp-Apim-Subscription-Key": sub_key
    }

    r = requests.post(url, headers=headers)
    try:
        return {"status": r.status_code, "result": r.json()}
    except:
        return {"status": r.status_code
