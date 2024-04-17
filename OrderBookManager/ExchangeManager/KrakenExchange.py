import requests
from MarketDepth import OrderBook

class KrakenConnector:
  """
  Connector class specifically for interacting with the Kraken API.
  """

  def __init__(self):
    """
    Initializes the connector with an empty order book.
    """
    self.order_book = None

  def get_order_book(self, symbol):
    """
    Fetches the order book data for a specific symbol from the Kraken API.

    Args:
        symbol (str): The symbol of the cryptocurrency pair (e.g., BTC-USD).

    Returns:
        OrderBook: An OrderBook object containing the retrieved order book data, or None on error.
    """

    # Define the base URL and endpoint for Kraken API
    base_url = 'https://api.kraken.com'
    url = f'{base_url}/0/public/Depth?pair={symbol}&count=25'

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the response is successful (status code 200)
    if response.status_code != 200:
      print(f'Error: {response.status_code}')
      return None

    # Parse the JSON response
    try:
      response_json = response.json()
      order_book_data = response_json["result"][symbol]
    except KeyError:
      print("Error: Invalid Kraken API response format.")
      return None

    # Extract ask and bid data from the response
    asks_list = [[asks[0], asks[1]] for asks in order_book_data["asks"]]
    bids_list = [[bids[0], bids[1]] for bids in order_book_data["bids"]]

    # Create an OrderBook object and update it with the retrieved data
    order_book = OrderBook()
    order_book.add_bid_levels(bids_list)
    order_book.add_ask_levels(asks_list)

    self.order_book = order_book
    return order_book

  def print_order_book(self):
    """
    Prints the order book information for Kraken. (Mainly for debugging)
    """

    if self.order_book is None:
      print("Kraken order book not fetched yet.")
      return

    print("\nKRAKEN:")
    print(f"Asks: {self.order_book.asks}")
    print(f"Bids: {self.order_book.bids}")
