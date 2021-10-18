import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


class YahooFinanceScraper:
    def __init__(self, *, symbol) -> None:
        self.url = f"https://ca.finance.yahoo.com/quote/{symbol}?p={symbol}"

    def get_webpage_text(self, parsed_page, selector):
        web_page_divs = parsed_page.select(f"div#{selector}")
        try:
            spans = web_page_divs[0].find_all("span")
            inner_text_list = [span.get_text() for span in spans]
        except IndexError:
            print("Index Error, probably no text was found")
            inner_text_list = []

        return inner_text_list

    def get_headers(self):
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
            "cache-control": "max-age=0",
            "dnt": "1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        }

    def get_stock_data(self):
        try:
            req = requests.get(self.url, headers=self.get_headers(), timeout=30)
            parsed_webpage = BeautifulSoup(req.text, "html.parser")
            inner_texts = self.get_webpage_text(parsed_webpage, "quote-header-info")
            print(inner_texts)
            if inner_texts != []:
                price, change = inner_texts[3], inner_texts[4]
            else:
                price, change = [], []

        except ConnectionError:
            print("Connection Error, couldn't connect to yahoo finance website")

        print(f"Current Price is {price} and the Percentage Change is {change}")
        return price, change
