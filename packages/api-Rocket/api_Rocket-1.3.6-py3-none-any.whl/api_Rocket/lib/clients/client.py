import requests
import random
import json
from .exception import exceptions
class Client:
	def __init__(self, token: str, proxies: dict = None):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": token,
			"Content-Type": "application/json",
		}

		if proxies == None:
			self.proxy = None
		else:
			self.proxy = {
				"http": f"http://{proxies}",
				"https": f"https://{proxies}"
				}
	#готов
	def api_version(self):
		url = "https://pay.ton-rocket.com/version"
		responce = requests.get(url, proxies=self.proxy)

		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def info(self):
		
		url = "https://pay.ton-rocket.com/app/info"
		responce = requests.get(url, proxies=self.proxy, headers=self.headers)
		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)
		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def transfer(self, data: dict):
		rand = random.randint(1000, 5000000000)
		responce = requests.post('https://pay.ton-rocket.com/app/transfer', proxies=self.proxy, headers = self.headers,
		json = {
			"tgUserId": data["userid"],
			"currency": data["currency"],
			"amount": data["amount"],
			"transferId": str(rand),
			"description": data["comment"]
		}
		)
		
		if responce.status_code != 201:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def create_multi_Cheques(self, data: dict):
		responce = requests.post('https://pay.ton-rocket.com/multi-cheques', proxies=self.proxy, headers = self.headers,
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
					data["telegramResurce"]
					],
				"forPremium": False,
				"linkedWallet": False,
				"disabledLanguages": [
				"NL",
				"FR"
				]
			}
		)
		if responce.status_code != 201:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x
	
	#готовy
	def check_multi_Cheques(self, limit: int = 100, offset: int = 0):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques?limit={limit}&offset={offset}", proxies=self.proxy, headers= self.headers)
		x = json.loads(responce.text)
		return x
		
	def info_multi_Cheques(self, id: int):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques/{id}", proxies=self.proxy, headers=self.headers)
		x = json.loads(responce.text)
		return x
		
	def edit_multi_Cheques(self, id: int, data: dict):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques/{id}", proxies=self.proxy, headers=self.headers,
				json = {
					"password": data["password"],
					"telegramResourcesIds": [
						data["telegramResurce"]
					]
				}
		)
		
		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x
		
	def delete_multi_Cheques(self, id: int):
		responce = requests.delete(f"https://pay.ton-rocket.com/multi-cheques/{id}", proxies=self.proxy, headers=self.headers)
		
		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x

	def check_currency(self):
		responce = requests.get("https://pay.ton-rocket.com/currencies/available", proxies=self.proxy, headers=self.headers)
		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x


	def create_invoice(self, data: dict):

		responce = requests.post("https://pay.ton-rocket.com/tg-invoices", proxies=self.proxy, headers=self.headers,
								json = {
									"amount": float(data["amount"]),
									"numPayments": int(data["numPayments"]),
									"currency": data["currency"],
									"description": data["description"],
									"hiddenMessage": data["message"],
									"callbackUrl": data["url"],
									"payload": "load",
									"expiredIn": data["expired"]
								}
			)

		if responce.status_code != 201:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x

	def check_invoices(self, limit: int =100, offset: int =0):
		responce = requests.get(f"https://pay.ton-rocket.com/tg-invoices?limit={limit}&offset={offset}", proxies=self.proxy, headers=self.headers)

		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x

	def get_invoice(self, id: int =0):
		responce = requests.get(f"https://pay.ton-rocket.com/tg-invoices/{id}", proxies=self.proxy, headers=self.headers)

		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x

	def delete_invoice(self, id: int =0):
		responce = requests.delete(f"https://pay.ton-rocket.com/tg-invoices/{id}", proxies=self.proxy, headers=self.headers)

		if responce.status_code != 200:
			exceptions.check_exceptions(code=responce.status_code)

		else:
			x = json.loads(responce.text)
		return x