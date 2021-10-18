import sched
import time
from stock_scraper import YahooFinanceScraper
from data_manipulator import DataManipulator


symbol = "BTC-CAD"


def retreive_data():
    scraper = YahooFinanceScraper(symbol=symbol)
    price, change = scraper.get_stock_data()
    datamanipulator = DataManipulator(
        price=price, symbol=symbol, change=change, rolling_window=5
    )
    datamanipulator.get_rolling_averages()


"""

def file_reader():
    local_time = datetime.now().strftime("%d/%m/%Y | %H:%M:%S ")
    print(local_time)
    try:
        df = pandas.read_csv("stocks_data.csv", index_col=[0])

    except FileNotFoundError:
        print("No File ")
        df = pandas.DataFrame(
            {
                "TimeStamp": local_time,
                "Symbol": symbol,
                "Price": 35,
                "Change": "5%",
            },
            index=[0],
        )
        df.to_csv("stocks_data.csv")
        return

    series = pandas.DataFrame(
        {
            "TimeStamp": local_time,
            "Symbol": symbol,
            "Price": 40,
            "Change": "5%",
        },
        index=[0],
    )

    print(series)

    df = df.append(
        series,
        ignore_index=True,
    )
    print(df)
    df.to_csv("stocks_data.csv")
"""


scheduler = sched.scheduler(time.time, time.sleep)
i = 0

while i <= 10:
    scheduler.enter(5, 1, retreive_data)
    scheduler.run()
    i += 1
