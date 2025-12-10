import requests
import sqlite3
import time
import datetime

# paramters are passed via dictionary to avoid endpoint errors
payload = {
    "function" : "CURRENCY_EXCHANGE_RATE",
    "from_currency" : "BTC",   #<- or whatever currency you want to track
    "to_currency" : "USD", #<- local conversion currency, change to your local currency. check the alpha vantage docs to see available currencies
    "apikey" : "URZP2YJV026Z764X" #<- use your api-key and be aware about api calls, making more than 5 calls per second gets you banned. read the alpha vantage artcile for more 
}
endpoint_url = "https://www.alphavantage.co/query" #<- direct csv datatype api endpoint is available, but your learn purpose i did this way. Change this accordingly based on alpha vantage docs

fieldnames = ["from_currency_code", "from_currency_name", "to_currency_code", "to_currency_name", "exchange_rate", "last_refreshed", "time_zone", "bid_price", "ask_price"]

conn = sqlite3.connect("crypto-prices.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bitcoin_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_currency_code TEXT, 
        from_currency_name TEXT, 
        to_currency_code TEXT, 
        to_currency_name TEXT, 
        exchange_rate FLOAT, 
        last_refreshed TEXT, 
        time_zone TEXT, 
        bid_price FLOAT, 
        ask_price FLOAT
    )
''')
conn.commit()

while(True) :
    try:
        response = requests.get(endpoint_url, params=payload)
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

            cursor.execute('''
                INSERT INTO bitcoin_prices(from_currency_code , 
                                            from_currency_name , 
                                            to_currency_code , 
                                            to_currency_name , 
                                            exchange_rate , 
                                            last_refreshed , 
                                            time_zone , 
                                            bid_price , 
                                            ask_price )
                values(?,?,?,?,?,?,?,?,?)
            ''',(clean_data["from_currency_code"],clean_data["from_currency_name"],clean_data["to_currency_code"],clean_data["to_currency_name"],clean_data["exchange_rate"],clean_data["last_refreshed"],clean_data["time_zone"],clean_data["bid_price"],clean_data["ask_price"]))
            conn.commit()


            print(f"Data saved to crypto-prices.db")
            time.sleep(60)

        else:
            print(f"Response error: {response.status_code}")
            time.sleep(60)

    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(60)

conn.close()