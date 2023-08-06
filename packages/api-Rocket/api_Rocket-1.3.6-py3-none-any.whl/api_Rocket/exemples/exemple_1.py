import apirocket

app = apirocket.Client(token="be3e5a68684cc8bbe2cf78300")

version = app.api_version()

print(version)