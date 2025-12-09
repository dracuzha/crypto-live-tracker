import requests
import json

# endpoint parameters
function = "CURRENCY_EXCHANGE_RATE"
from_currency = "BTC"
to_currency = "USD"
apikey = "URZP2YJV026Z764X"

endpoint_url = f"https://www.alphavantage.co/query?function={function}&from_currency={from_currency}&to_currency={to_currency}&apikey={apikey}"

response = requests.get(endpoint_url)
data = response.json()

json_file = 'crypto-data-test.json'
with open(json_file, 'w') as file:
    json.dump(data,file)