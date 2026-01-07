import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_category,get_amount,get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    DATE_FORMAT = "%d-/%m-/%Y"

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        finance_df = pd.read_csv(cls.CSV_FILE)
        finance_df["date"] = pd.to_datetime(finance_df["date"], format=CSV.DATE_FORMAT)
        start_date = datetime.strptime(start_date, CSV.DATE_FORMAT)
        end_date = datetime.strptime(end_date, CSV.DATE_FORMAT)

        mask = (finance_df["date"] >= start_date) & (finance_df["date"] <= end_date)
        filtered_df = finance_df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in the specified date range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}")
            print(finance_df.to_string(index=False,
                                       formatters={"date":lambda x: x.strftime(CSV.DATE_FORMAT)}
                                       )
                  )
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\n Summary: ")
            print(f"Total Income: #{total_income:.2f}")
            print(f"Total Expense: #{total_expense:.2f}")
            print(f"Net Savings: #{(total_income - total_expense):.2f}")

        return filtered_df

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



