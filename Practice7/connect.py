import psycopg2
import csv
from config import DB_CONFIG

def connect():
    return psycopg2.connect(**DB_CONFIG)

conn = connect()
cur = conn.cursor()

cur.execute("DELETE FROM contacts")
conn.commit()

with open("/Users/akhmetsaulet/Desktop/PP2/Practice7/contacts.csv", "r") as file:
    reader = csv.reader(file)

    next(reader, None)

    for row in reader:
        cur.execute(
            "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
            (row[0], row[1])
        )

conn.commit()
print("Data inserted!")

cur.execute("SELECT * FROM contacts")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()