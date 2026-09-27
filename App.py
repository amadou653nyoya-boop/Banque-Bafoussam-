from flask import Flask, request, redirect
import requests, uuid, os
app = Flask(__name__)
KEY=os.environ.get("NOTCHPAY_KEY")
@app.route("/")
def home():
 return "<h1>CAISSE BAFOUSSAM LIVE</h1><form method='POST' action='/payer'><input name='email' placeholder='email'><br><br><input name='montant' value='100'><br><br><button>PAYER MOMO</button></form>"
@app.route("/payer",methods=["POST"])
def payer():
 data={"email":request.form["email"],"amount":request.form["montant"],"currency":"XAF","reference":str(uuid.uuid4()),"callback":"https://banque-bafoussam.onrender.com/callback"}
 r=requests.post("https://api.notchpay.co/payments/initialize",json=data,headers={"Authorization":KEY})
 try: return redirect(r.json()["transaction"]["authorization_url"])
 except: return r.text
@app.route("/callback")
def callback():
 return "Paiement OK"
