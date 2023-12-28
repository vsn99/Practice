import mysql.connector
import json

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            with open("config.json") as config_file:
                config_data = json.load(config_file)["database"]

            self.conn = mysql.connector.connect(
                host=config_data["host"],
                user=config_data["user"],
                password=config_data["password"],
                database=config_data["database"]
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")




    def disconnect(self):
        try:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
        except Exception as e:
            print(f"Error disconnecting from the database: {e}")

    def execute_query(self, query, data=None):
        try:
            if not self.conn.is_connected():
                self.connect()

            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)

            self.conn.commit()
            return self.cursor.fetchall()

        except Exception as e:
            print(f"Error executing query: {e}")
            return None
