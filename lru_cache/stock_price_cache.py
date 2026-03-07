# This program implements a StockPriceCache that:
# Has a fixed capacity (say 3 stocks).
# Has a get_price(symbol) method:
# If the symbol is in the cache, return the price instantly (cache hit).
# If not, simulate a slow API call to the exchange, store the result, and return it (cache miss).
# When the cache is full, evict the least recently viewed stock.




from collections import OrderedDict
import time


# Simulates a slow stock price API (pretend this takes network time)
STOCK_PRICE_API = {
    "AAPL": 150.75,
    "GOOG": 2820.12,
    "MSFT": 235.77,
    "AMZN": 3384.12,
    "TSLA": 822.12,
}

def slow_stock_price_api(symbol):
    """
     a slow network call to get the stock price for a given symbol
    """
    time.sleep(1)
    return STOCK_PRICE_API.get(symbol, 0)

class StockPriceCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get_symbol(self, symbol):
        """
        fetch the price for a given symbol from cache
        if not found, return -1
        if found, move to end of cache
        return the price
        """
        if symbol is not None and symbol in self.cache:
            self.cache.move_to_end(symbol)
            return self.cache[symbol]
        return -1
    
    def put_symbol(self, symbol, price):
        """
        put tthe symbol & price in the cache
        in case cache is full, remove the LRU item
        """
        if symbol is not None:
            self.cache[symbol] = price
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def get_price(self, symbol):
        if symbol is not None and symbol in self.cache:
            self.cache.move_to_end(symbol)
            return f"{symbol} - cache hit, current cache: {self.cache}"
        else:
            price = slow_stock_price_api(symbol)
            self.put_symbol(symbol, price)
            return f"{symbol} - cache miss, current cache: {self.cache}"

stockpricecache = StockPriceCache(capacity=3)
print(stockpricecache.get_price("AAPL"))
print(stockpricecache.get_price("GOOG"))
print(stockpricecache.get_price("AAPL"))
print(stockpricecache.get_price("MSFT"))
print(stockpricecache.get_price("AMZN"))
print(stockpricecache.get_price("TSLA"))

# expected Output :
# AAPL - cache miss, current cache: OrderedDict([('AAPL', 150.75)])
# GOOG - cache miss, current cache: OrderedDict([('AAPL', 150.75), ('GOOG', 2820.12)])
# AAPL - cache hit, current cache: OrderedDict([('GOOG', 2820.12), ('AAPL', 150.75)])
# MSFT - cache miss, current cache: OrderedDict([('GOOG', 2820.12), ('AAPL', 150.75), ('MSFT', 235.77)])
# AMZN - cache miss, current cache: OrderedDict([('AAPL', 150.75), ('MSFT', 235.77), ('AMZN', 3384.12)])
# TSLA - cache miss, current cache: OrderedDict([('MSFT', 235.77), ('AMZN', 3384.12), ('TSLA', 822.12)])