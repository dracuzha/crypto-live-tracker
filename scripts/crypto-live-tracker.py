import pandas as pd
from datetime import datetime
import requests
import sqlite3
import time
import logging

# LOGGING CONFIGURATION
logging.basicConfig(
    filename="crypto-tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# CONSOLE CONFIGURATION
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# CONFIGURATION
# paramters are passed via dictionary to avoid endpoint errors
payload = {
    "function" : "CURRENCY_EXCHANGE_RATE",
    "from_currency" : "BTC",   #<- or whatever currency you want to track
    "to_currency" : "USD", #<- local conversion currency, change to your local currency. check the alpha vantage docs to see available currencies
    "apikey" : "URZP2YJV026Z764X" #<- use your api-key and be aware about api calls, making more than 5 calls per second gets you banned. read the alpha vantage artcile for more 
}
endpoint_url = "https://www.alphavantage.co/query" #<- direct csv datatype api endpoint is available, but your learn purpose i did this way. Change this accordingly based on alpha vantage docs
db_name = "crypto-prices.db"

logging.info("Starting Crypto Live Tracker...")
while(True) :
    try:
        logging.info("Sending request to Alpha Vantage...")
        response = requests.get(endpoint_url, params=payload)
        if response.status_code == 200:
            raw_data = response.json()

            if "Realtime Currency Exchange Rate" not in raw_data:
                logging.error(f"API Returned unexpected data: {raw_data}")
                time.sleep(60)
                continue
            logging.info("Response got successfully from Alpha Vantage !")
            
            clean_data = {
                "from_currency_code" : raw_data["Realtime Currency Exchange Rate"]["1. From_Currency Code"],
                "from_currency_name" : raw_data["Realtime Currency Exchange Rate"]["2. From_Currency Name"], 
                "to_currency_code" : raw_data["Realtime Currency Exchange Rate"]["3. To_Currency Code"], 
                "to_currency_name" : raw_data["Realtime Currency Exchange Rate"]["4. To_Currency Name"], 
                "exchange_rate" : float(raw_data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]), 
                "last_refreshed" : raw_data["Realtime Currency Exchange Rate"]["6. Last Refreshed"], 
                "time_zone" : raw_data["Realtime Currency Exchange Rate"]["7. Time Zone"], 
                "bid_price" : float(raw_data["Realtime Currency Exchange Rate"]["8. Bid Price"]), 
                "ask_price" : float(raw_data["Realtime Currency Exchange Rate"]["9. Ask Price"])
            }

            df = pd.DataFrame([clean_data])
            conn = sqlite3.connect(db_name)
            df.to_sql("bitcoin_prices", conn, if_exists="append", index=False)
            conn.close()

            logging.info(f"Data saved to crypto-prices.db @{datetime.now()}")
            time.sleep(15)

        else:
            logging.error(f"HTTP error: {response.status_code}")
            time.sleep(60)

    except KeyboardInterrupt:
            logging.info("User stopped the script manually.")
            break

    except Exception as e:
        logging.error("Critical crash occurred", exc_info=True)
        time.sleep(60)
