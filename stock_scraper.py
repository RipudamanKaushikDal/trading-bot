import aiohttp
import asyncio
from bs4 import BeautifulSoup


class YahooFinanceScraper:
    def __init__(self, *, symbol_list) -> None:
        self.symbols = symbol_list

    async def get_info_fields(self, *, container, attr_dict) -> str:
        field = container.find(attrs=attr_dict)
        info = field.get_text()
        return info

    async def get_webpage_text(self, parsed_page, selector) -> tuple:
        web_page_divs = parsed_page.select(f"div#{selector}")
        try:
            price, change = await asyncio.gather(
                self.get_info_fields(
                    container=web_page_divs[0],
                    attr_dict={"data-field": "regularMarketPrice"},
                ),
                self.get_info_fields(
                    container=web_page_divs[0],
                    attr_dict={"data-field": "regularMarketChangePercent"},
                ),
            )
        except AttributeError:
            print("Error, probably no info was found")
            price, change = "N/A", "N/A"

        return price, change

    def get_headers(self) -> dict:
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

    async def get_stock_data(self, *, symbol, session) -> tuple:
        try:
            url = f"https://ca.finance.yahoo.com/quote/{symbol}?p={symbol}"
            req = await session.get(url=url, headers=self.get_headers(), timeout=30)
            parsed_webpage = BeautifulSoup(await req.text(), "html.parser")
            price, change = await self.get_webpage_text(
                parsed_webpage, "quote-header-info"
            )

        except ConnectionError:
            print("Connection Error, couldn't connect to yahoo finance website")

        print(
            f"Current Price of {symbol} is {price} and the Percentage Change is {change}"
        )
        return price, change

    async def fetch_prices(self) -> list:
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *[
                    self.get_stock_data(symbol=symbol, session=session)
                    for symbol in self.symbols
                ]
            )
        await session.close()
        return results
