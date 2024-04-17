import requests
from MarketDepth import OrderBook

class GeminiConnector:
  """
  Connector class specifically for interacting with the Gemini API.
  """

  def __init__(self):
    """
    Initializes the connector with an empty order book.
    """
    self.order_book = None

  def get_order_book(self, symbol):
    """
    Fetches the order book data for a specific symbol from the Gemini API.

    Args:
        symbol (str): The symbol of the cryptocurrency pair (e.g., BTC-USD).

    Returns:
        OrderBook: An OrderBook object containing the retrieved order book data, or None on error.
    """

    # Define the base URL and endpoint for Gemini API
    base_url = 'https://api.gemini.com'
    order_book_endpoint = f'/v1/book/{symbol}'
    url = f'{base_url}{order_book_endpoint}?limit_bids=25&limit_asks=25'

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the response is successful (status code 200)
    if response.status_code != 200:
      print(f'Error: {response.status_code}')
      return None

    # Parse the JSON response
    response_json = response.json()

    # Extract ask and bid data from the response
    asks_list = [[asks['price'], asks['amount']] for asks in response_json["asks"]]
    bids_list = [[bids['price'], bids['amount']] for bids in response_json["bids"]]

    # Create an OrderBook object and update it with the retrieved data
    order_book = OrderBook()
    order_book.add_bid_levels(bids_list)
    order_book.add_ask_levels(asks_list)

    self.order_book = order_book
    return order_book

  def print_order_book(self):
    """
    Prints the order book information for Gemini. (Mainly for debugging)
    """

    if self.order_book is None:
      print("Gemini order book not fetched yet.")
      return

    print("\nGEMINI:")
    print(f"Asks: {self.order_book.asks}")
    print(f"Bids: {self.order_book.bids}")
