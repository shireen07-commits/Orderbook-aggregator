import requests
from MarketDepth import OrderBook

class CoinBaseConnector:
  
  def __init__(self):
    self.order_book = None
  def get_order_book(self, symbol):
   
    base_url = 'https://api.pro.coinbase.com'
    order_book_endpoint = f'/products/{symbol}/book'
    url = f'{base_url}{order_book_endpoint}?level=2'

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the response is successful (status code 200)
    if response.status_code != 200:
      print(f'Error: {response.status_code}')
      return None

    # Parse the JSON response
    response_json = response.json()

    # Extract ask and bid data from the response
    asks_list = [[asks[0], asks[1]] for asks in response_json["asks"]]
    bids_list = [[bids[0], bids[1]] for bids in response_json["bids"]]

    # Create an OrderBook object and update it with the retrieved data
    order_book = OrderBook()
    order_book.add_bid_levels(bids_list)
    order_book.add_ask_levels(asks_list)

    self.order_book = order_book
    return order_book

  def print_order_book(self):
   
    if self.order_book is None:
      print("Coinbase order book not fetched yet.")
      return

    print("\nCOINBASE:")
    print(f"Asks: {self.order_book.asks}")
    print(f"Bids: {self.order_book.bids}")
