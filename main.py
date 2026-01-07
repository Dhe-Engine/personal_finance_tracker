import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_category,get_amount,get_description

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

def start():
    CSV.initialize_csv()
    date = get_date("Enter transaction date (dd-mm-yyyy) format: ",
                    allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    #take user input to the csv file
    CSV.add_data(date,amount,category,description)

start()



