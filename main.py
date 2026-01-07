import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date,get_category,get_amount,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    DATE_FORMAT = "%d-%m-%Y"

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

def graph_transaction(finance_df):
    finance_df.set_index("date", inplace=True)

    income_df = finance_df[finance_df["category"] == "Income"].resample("D").sum().reindex(
        finance_df.index, fill_value=0
    )

    expense_df = finance_df[finance_df["category"] == "Expense"].resample("D").sum().reindex(
        finance_df.index, fill_value=0
    )

    plt.figure(figsize = (10,5))
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "orange")
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color = "black")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over time")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    while True:
        print("\n1. Add New Transaction")
        print("2. View Transactions")
        print("3. Exit Program")

        user_choice = int(input("Selet Option (1-3): "))
        if user_choice == 1:
            start()
        elif user_choice == 2:
            start_date = get_date("Enter start date (dd-mm-yyyy): ")
            end_date = get_date("Enter end date (dd-mm-yyyy): ")
            date_df = CSV.get_transactions(start_date, end_date)
            if input("Show transaction in graph (yes/no): ").lower() == "yes":
                graph_transaction(date_df)
        elif user_choice == 3:
            print("End of Program")
            break
        else:
            print("Index out of range")
            main()

if __name__ == "__main__":
    main()





