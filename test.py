import time
from stock_scraper import YahooFinanceScraper
import asyncio
import platform


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        total = time.time() - start
        print("Total time taken:", total, "seconds")

    return wrapper


symbol_list = ["BTC-CAD", "TSLA", "ETH-CAD", "MRNA", "AAPL"]


"""@timer
def get_data():
    for symbol in symbol_list:
        scraper = YahooFinanceScraper(symbol=symbol)
        scraper.get_stock_data()
"""


@timer
def get_data():
    scraper = YahooFinanceScraper(symbol_list=symbol_list)
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(scraper.fetch_prices())


get_data()
