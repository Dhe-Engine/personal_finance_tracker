import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            finance_df = pd.DataFrame(columns=cls.COLUMNS)
            finance_df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_data(cls,date,amount,category,description):
        new_data = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }

        with open(cls.CSV_FILE, mode="a", newline="") as finance_csv:
            csv_write = csv.DictWriter(finance_csv, fieldnames=cls.COLUMNS)
            csv_write.writerow(new_data)
        print("Data added successfully!")

CSV.initialize_csv()
CSV.add_data("07-01-2026",67000.00,"Income","Jewelry")