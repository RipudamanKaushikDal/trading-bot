import pandas as pd
from datetime import datetime


class DataManipulator:
    def __init__(self, *, price, change, symbol, rolling_window) -> None:
        self.data = {
            "TimeStamp": [datetime.now().strftime("%d/%m/%Y | %H:%M:%S ")],
            "Symbol": [symbol],
            "Price": [price],
            "Change": [change],
        }
        self.price = price
        self.window = rolling_window

    def get_rolling_averages(self):

        try:
            df = pd.read_csv("stocks_data.csv", index_col=[0])
            df_length = len(df.index._range)

        except FileNotFoundError:
            df = pd.DataFrame(self.data)
            df.to_csv("stocks_data.csv")
            print("First Entry")
            return

        if df_length == self.window:
            new_df = pd.DataFrame(self.data)
            df = df.append(new_df, ignore_index=True)
            df["Rolling_Avg"] = df["Price"].rolling(self.window).mean()

        elif df_length > self.window:
            self.data["Rolling_Avg"] = [
                (self.price + df_length * df["Rolling_Avg"].iloc[-1]) / df_length + 1
            ]
            updated_df = pd.DataFrame(self.data)
            df = df.append(updated_df, ignore_index=True)

        else:
            new_df = pd.DataFrame(self.data)
            df = df.append(new_df, ignore_index=True)

        df.to_csv("stocks_data.csv")
        print(df)
