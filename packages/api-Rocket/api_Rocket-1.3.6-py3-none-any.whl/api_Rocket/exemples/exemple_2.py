import apirocket

app = apirocket.Client(token="be3e5a68684cc8bbe2cf78300")

info = app.info()

print(info.get("data"))