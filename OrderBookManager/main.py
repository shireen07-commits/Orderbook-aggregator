import sys

from ExchangeManager.CoinBaseExchange import CoinBaseConnector
from ExchangeManager.GeminiExchange import GeminiConnector
from ExchangeManager.KrakenExchange import KrakenConnector

from OrderBookAggregator import OrderBookAggregator


def parse_arguments(arguments):
  """
  Parses command-line arguments for the script.
  Args:
      arguments (list[str]): List of command-line arguments.
  Returns:
      tuple[float, bool]: A tuple containing the target amount and a flag indicating Kraken exchange usage.
  """
  # Set default values
  target_amount = 10.0
  use_kraken_exchange = False

  # Check if target_amount is provided
  if len(arguments) > 1:
    try:
      target_amount = float(arguments[1])
    except ValueError:
      print("Error: Invalid input for target_amount. Using the default value of 10.")

  # Check if use_kraken_exchange is provided
  if len(arguments) > 2:
    try:
      use_kraken_exchange = arguments[2].lower() in ['true', '1', 't', 'y', 'yes']
    except ValueError:
      print("Error: Invalid input for use_kraken_exchange. Not considering it.")

  return target_amount, use_kraken_exchange


def get_order_books(symbol, use_kraken_exchange):
  """
  Fetches order books from Coinbase and Gemini, optionally including Kraken.

  Args:
      symbol (str): The trading symbol for Coinbase and Gemini exchanges.
      use_kraken_exchange (bool): A flag indicating whether to include Kraken exchange.

  Returns:
      tuple[OrderBook, OrderBook, OrderBook]: A tuple containing order books from Coinbase, Gemini, and optionally Kraken.
  """
  symbol = 'BTC-USD'
  coinbase_connector = CoinBaseConnector()
  coinbase_book = coinbase_connector.get_order_book(symbol)

  gemini_symbol = 'btcusd'
  gemini_connector = GeminiConnector()
  gemini_book = gemini_connector.get_order_book(gemini_symbol)

  kraken_book = None
  if use_kraken_exchange:
    kraken_symbol = 'XXBTZUSD'
    kraken_connector = KrakenConnector()
    kraken_book = kraken_connector.get_order_book(kraken_symbol)

  return coinbase_book, gemini_book, kraken_book


def main():
  """
  Main entry point of the script.
  """
  # Parse command-line arguments
  arguments = sys.argv
  target_amount, use_kraken_exchange = parse_arguments(arguments)

  # Fetch order books
  symbol = 'BTC-USD'
  coinbase_book, gemini_book, kraken_book = get_order_books(symbol, use_kraken_exchange)

  # Initialize OrderBookAggregator
  aggregator = OrderBookAggregator(coinbase_book, gemini_book, kraken_book)

  # Aggregate order books
  aggregated_book = aggregator.aggregate()

  # Calculate average buy and sell prices
  average_buy_price, average_sell_price = aggregated_book.calculate_average_price(target_amount)

  # Print the results
  print(f'Average Buy Price for {target_amount} BTC: {average_buy_price:.2f}')
  print(f'Average Sell Price for {target_amount} BTC: {average_sell_price:.2f}')


if __name__ == '__main__':
  main()
