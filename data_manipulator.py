import pandas as pd
from datetime import datetime


class DataManipulator:
    def __init__(
        self, *, price: str, change: str, symbol: str, rolling_window: int
    ) -> None:
        price = price.replace(",", "")
        self.price = float(price)
        self.window = rolling_window
        self.data = {
            "TimeStamp": [datetime.now().strftime("%d/%m/%Y | %H:%M:%S ")],
            "Symbol": [symbol],
            "Price": [self.price],
            "Change": [change],
        }

    def get_rolling_averages(self):

        try:
            df = pd.read_csv("stocks_data.csv", index_col=[0])
            df_length = len(df.index)

        except FileNotFoundError:
            df = pd.DataFrame(self.data)
            df.to_csv("stocks_data.csv")
            print("First Entry")
            return

        if df_length >= self.window:
            new_df = pd.DataFrame(self.data)
            df = df.append(new_df, ignore_index=True)
            df["Rolling_Avg"] = df["Price"].rolling(self.window).mean()

        else:
            new_df = pd.DataFrame(self.data)
            df = df.append(new_df, ignore_index=True)

        df.to_csv("stocks_data.csv")
        print(df)
