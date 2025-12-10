import sqlite3

conn = sqlite3.connect("crypto-prices.db")
cursor = conn.cursor()

cursor.execute('''SELECT * FROM bitcoin_prices''')
print(cursor.fetchall())
conn.close()