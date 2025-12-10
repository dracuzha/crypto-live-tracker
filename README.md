# 📈 Crypto Live Price Tracker

A python script to live price track crypto currencies with local currency exhange rate and store it in a sqlite DB file. Uses [Alpha Vantage](https://www.alphavantage.co/documentation/) API for getting crypto exchange rate.

## 🧪 Tests Overview

- Tests the api endpoint and json structure.
- Folder test/ has test python script that calls AV API endpoint and gets a json file. This actually used to test the API endpoint works and how the json data is structured and its parameters.

## 📃 Script

- This Python script gets the crypto live price exchange rate and store it in a sqlite DB file
- Uses requests python library to interact with API and gets the json data. And the json data is cleaned somewhat and stored in a sqlite DB file.
- Implemented Pandas for much cleaner approach to insert dictionary data into SQL DB, logging for cleaner way to document the process.

## 📝 Note :

This can be implemented in much efficient way like using direct csv api endpoint and pandas can be used to simply the data cleaning which would be very much efficient than what is implemented here. This is simply done for my learning purpose and doing the old school way.
