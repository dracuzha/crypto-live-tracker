import requests
import csv
import time

function = "GLOBAL_QUOTE"
symbol = "IBM"
apikey = "URZP2YJV026Z764X"
fieldnames = ["symbol", "open", "high", "low", "price", "volume", "latest trading day", "previous_close", "change", "change_percent"]

endpoint_url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}"

while(True) :
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            print("Response obtained !")
            raw_data = response.json()

            clean_data = {
                "symbol" : raw_data["Global Quote"]["01. symbol"],
                "open" : raw_data["Global Quote"]["02. open"], 
                "high" : raw_data["Global Quote"]["03. high"], 
                "low" : raw_data["Global Quote"]["04. low"], 
                "price" : raw_data["Global Quote"]["05. price"], 
                "volume" : raw_data["Global Quote"]["06. volume"], 
                "latest trading day" : raw_data["Global Quote"]["07. latest trading day"], 
                "previous_close" : raw_data["Global Quote"]["08. previous close"], 
                "change" : raw_data["Global Quote"]["09. change"], 
                "change_percent" : raw_data["Global Quote"]["10. change percent"]
            }

            csv_file_name = "stock-data.csv"
            with open(csv_file_name, mode='a', newline='') as data_file:
                writer = csv.DictWriter(data_file,fieldnames=fieldnames)
                if data_file.tell() == 0:
                    writer.writeheader()
                writer.writerow(clean_data)

            print(f"Data Saved to {csv_file_name} !")
            time.sleep(60)

        else:
            print(f"Response error: {response.status_code}")
            time.sleep(60)

    except Exception as e:
        print(f"Error occurred: {e}")