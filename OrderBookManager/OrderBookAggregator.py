from MarketDepth import OrderBook
from PriceVolume import PriceVolume


class OrderBookAggregator:
    def __init__(self, coinbase_book, gemini_book, kraken_book):
        # Initialize the aggregator with order books from different exchanges
        self.coinbase_book = coinbase_book
        self.gemini_book = gemini_book
        self.kraken_book = kraken_book

    def aggregate(self):
        # Create a new OrderBook object to store the aggregated data
        aggregated_order_book = OrderBook()

        # Aggregate bids
        books_bids = self.coinbase_book.bids + self.gemini_book.bids
        if self.kraken_book:
            books_bids = self.coinbase_book.bids + self.gemini_book.bids + self.kraken_book.bids   # Include Kraken bids if available
        aggregated_bids = {}
        for entry in books_bids:
            if entry.price in aggregated_bids:
                aggregated_bids[entry.price] += entry.volume
            else:
                aggregated_bids[entry.price] = entry.volume

        # Sort aggregated bids by price in descending order
        aggregated_order_book.bids = [PriceVolume(price, aggregated_bids[price]) for price in sorted(aggregated_bids.keys(), reverse=True)]

        # Aggregate asks
        books_asks = self.coinbase_book.asks + self.gemini_book.asks
        if self.kraken_book:
            books_asks = self.coinbase_book.asks + self.gemini_book.asks + self.kraken_book.asks   # Include Kraken asks if available
        aggregated_asks = {}
        for entry in books_asks:
            if entry.price in aggregated_asks:
                aggregated_asks[entry.price] += entry.volume
            else:
                aggregated_asks[entry.price] = entry.volume

        # Sort aggregated asks by price in ascending order
        aggregated_order_book.asks = [PriceVolume(price, aggregated_asks[price]) for price in sorted(aggregated_asks.keys())]

        # Return the aggregated order book
        return aggregated_order_book
