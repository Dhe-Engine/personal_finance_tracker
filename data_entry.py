import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            finance_df = pd.DataFrame(columns=["date","amount","category","description"])
            finance_df.to_csv(cls.CSV_FILE, index=False)

CSV.initialize_csv()