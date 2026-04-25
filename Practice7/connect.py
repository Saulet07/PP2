import psycopg2
import csv
import os
from config import DB_CONFIG

def connect_and_insert():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Connected successfully!")

        # Очистка
        cur.execute("DELETE FROM contacts")
        conn.commit()

        # Путь к файлу
        file_path = os.path.join(os.path.dirname(__file__), "contacts.csv")
        
        if not os.path.exists(file_path):
            print(f"ERROR: File not found at {file_path}")
            return

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Пропуск заголовка
            
            count = 0
            for row in reader:
                print(f"Inserting: {row}")
                cur.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )
                count += 1
            
            print(f"Total rows inserted: {count}")

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

connect_and_insert()