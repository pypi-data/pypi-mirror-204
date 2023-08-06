import apirocket

app = apirocket.Client(token="be3e5a68684cc8bbe2cf78300")

data = {
	"userid": 123456,
	"currency": "TONCOIN",
	"amount": 0.5,
	"comment": "you best bruh!"
}

transfer = app.transfer(data=data)

print(transfer)