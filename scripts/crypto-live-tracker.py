import requests
import csv
import time

function = "CURRENCY_EXCHANGE_RATE"
from_currency = "BTC"   #<- or whatever currency you want to track
to_currency = "USD" #<- local conversion currency, change to your local currency. check the alpha vantage docs to see available currencies
apikey = "URZP2YJV026Z764X" #<- use your api-key and be aware about api calls, making more than 5 calls per second gets you banned. read the alpha vantage artcile for more 
fieldnames = ["from_currency_code", "from_currency_name", "to_currency_code", "to_currency_name", "exchange_rate", "last_refreshed", "time_zone", "bid_price", "ask_price"]

endpoint_url = f"https://www.alphavantage.co/query?function={function}&from_currency={from_currency}&to_currency={to_currency}&apikey={apikey}" #<- direct csv datatype api endpoint is available, but your learn purpose i did this way. Change this accordingly based on alpha vantage docs

while(True) :
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            print("Response got !")
            raw_data = response.json()
            clean_data = {
                "from_currency_code" : raw_data["Realtime Currency Exchange Rate"]["1. From_Currency Code"],
                "from_currency_name" : raw_data["Realtime Currency Exchange Rate"]["2. From_Currency Name"], 
                "to_currency_code" : raw_data["Realtime Currency Exchange Rate"]["3. To_Currency Code"], 
                "to_currency_name" : raw_data["Realtime Currency Exchange Rate"]["4. To_Currency Name"], 
                "exchange_rate" : raw_data["Realtime Currency Exchange Rate"]["5. Exchange Rate"], 
                "last_refreshed" : raw_data["Realtime Currency Exchange Rate"]["6. Last Refreshed"], 
                "time_zone" : raw_data["Realtime Currency Exchange Rate"]["7. Time Zone"], 
                "bid_price" : raw_data["Realtime Currency Exchange Rate"]["8. Bid Price"], 
                "ask_price" : raw_data["Realtime Currency Exchange Rate"]["9. Ask Price"]
            }

            csv_file = f"{from_currency}-{to_currency}-price-tracker.csv"
            with open(csv_file, mode='a', newline='') as data_file:
                writer = csv.DictWriter(data_file, fieldnames=fieldnames)
                if data_file.tell() == 0:
                    writer.writeheader()
                writer.writerow(clean_data)
            print(f"Data saved to {csv_file}")
            time.sleep(60)

        else:
            print(f"Response error: {response.status_code}")
            time.sleep(60)

    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(60)