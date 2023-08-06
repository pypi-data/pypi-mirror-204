import requests
import random
import json
class Client:
	def __init__(self, token):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": token,
			"Content-Type": "application/json",
		}
		
	#готов
	def api_version(self):
		url = "https://pay.ton-rocket.com/version"
		responce = requests.get(url)
		x = json.loads(responce.text)
		return x
		
	#готов
	def info(self):
		
		url = "https://pay.ton-rocket.com/app/info"
		responce = requests.get(url, headers=self.headers)
		x = json.loads(responce.text)
		return x
		
	#готов
	def transfer(self, data):
		responce = requests.post('https://pay.ton-rocket.com/app/transfer', headers = self.headers,
		json = {
			"tgUserId": data["userid"],
			"currency": data["currency"],
			"amount": data["amount"],
			"transferId": "12345",
			"description": data["comment"]
		}
		)
		
		x = json.loads(responce.text)
		
		return x
		
	#готов
	def create_multi_Cheques(self, data):
		responce = requests.post('https://pay.ton-rocket.com/multi-cheques', headers = self.headers,
			json = {
				"currency": data["currency"],
				"chequePerUser": data["PerUser"], #int
				"usersNumber": data["usersNumber"], #int
				"refProgram": data["refProgram"],
				"password": data["password"],
				"description": "This cheque is the best",
				"sendNotifications": True,
				"enableCaptcha": True,
				"telegramResourcesIds": [
					"-1001892364641"
					],
				"forPremium": False,
				"linkedWallet": False,
				"disabledLanguages": [
				"NL",
				"FR"
				]
			}
		)
		x = json.loads(responce.text)
		return x
	
	#готов
	def check_multi_Cheques(self, limit = 100, offset = 0):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques?limit={limit}&offset={offset}", headers= self.headers)
		x = json.loads(responce.text)
		return x