import requests
import json

# endpoint parameters
payload = {
    "function" : "CURRENCY_EXCHANGE_RATE",
    "from_currency" : "BTC",
    "to_currency" : "USD",
    "apikey" : "URZP2YJV026Z764X"
}

endpoint_url = "https://www.alphavantage.co/query"
response = requests.get(endpoint_url, params=payload)
data = response.json()

json_file = 'crypto-data-test.json' #<- change the test data file name here
with open(json_file, 'w') as file:
    json.dump(data,file)