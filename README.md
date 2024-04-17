OrderBookAggregator:
main.py
Functionality
**1. Command-Line Arguments (parse_arguments):**

- Parses command-line arguments provided when running the script.
- Sets default values for target amount (10.0) and using Kraken exchange (False).
- Reads arguments:
  - If a target amount is provided, validates it and updates the default value.
  - If a flag for using Kraken exchange is present (various formats like "true", "1", "t"), sets the corresponding flag.
- Returns the parsed target amount and Kraken exchange usage flag.

**2. Fetching Order Books (get_order_books):**

- Takes the trading symbol (`symbol`) and a flag indicating Kraken exchange usage (`use_kraken_exchange`).
- Defines the actual symbol used for Coinbase and Gemini (always "BTC-USD").
- Creates connectors for Coinbase and Gemini exchanges.
- Fetches order books from Coinbase and Gemini using their connectors.
- Optionally, if the `use_kraken_exchange` flag is set:
  - Defines the symbol used for Kraken ("XXBTZUSD").
  - Creates a connector for Kraken exchange.
  - Fetches the order book from Kraken.
- Returns a tuple containing the fetched order books from Coinbase, Gemini, and optionally Kraken.

**3. Main Function (main):**

- The main entry point of the script.
- Retrieves command-line arguments using `sys.argv`.
- Calls `parse_arguments` to parse arguments and get target amount and Kraken exchange usage flag.
- Defines the symbol ("BTC-USD") used for all exchanges (assumed consistent).
- Calls `get_order_books` to fetch order books from Coinbase, Gemini, and optionally Kraken with the parsed arguments.
- Creates an `OrderBookAggregator` object, passing the fetched order books from each exchange.
- Calls the `aggregate` method of the aggregator to combine the order books from different exchanges.
- Calculates the average buy and sell prices for the target amount using the `calculate_average_price` method of the aggregated order book.
- Prints the calculated average buy price and average sell price for the specified target amount (formatted to two decimal places).

**Summary:**

This script fetches order book data from Coinbase, Gemini, and optionally Kraken for a specified trading symbol ("BTC-USD" by default). It then combines these order books and calculates the average buy and sell prices for a user-defined target quantity. Finally, it displays the calculated average buy and sell prices.

Order Book Aggregator

This Python script retrieves order book data from multiple cryptocurrency exchanges and calculates the average buy and sell prices for a target quantity.

- **Optional arguments:**
  - `target_amount`: The desired quantity of cryptocurrency (default: 10.0).
  - `use_kraken_exchange`: Set to `true`, `1`, `t`, `y`, or `yes` to include Kraken exchange (default: False).

### Example

```bash
python main.py 10.0 true
```

This will fetch order books from Coinbase, Gemini, and Kraken for the BTC-USD symbol, Aggregate and calculate the average buy and sell prices for 10.0 BTC, and print the results.

### Dependencies

- Python 3.x
- `requests` library (for making API calls to exchanges)

OrderBookAggregator.py

1. **Initialize:**
   - Receives order books from Coinbase, Gemini (optional Kraken).
2. **Combine Bids:**
   - Combine bids from all exchanges.
   - Iterate through each combined bid entry.
     - If price exists in aggregated bids, add current volume to existing volume.
     - Otherwise, add a new entry for the price with the current volume.
   - Sort aggregated bids by price (descending order - highest first).
   - Convert aggregated bids back to `PriceVolume` objects.
3. **Combine Asks:**
   - Similar to bids, combine asks from all exchanges.
   - Iterate through each combined ask entry.
     - If price exists in aggregated asks, add current volume to existing volume.
     - Otherwise, add a new entry for the price with the current volume.
   - Sort aggregated asks by price (ascending order - lowest first).
   - Convert aggregated asks back to `PriceVolume` objects.
4. **Return Result:**
   - Create a new empty order book.
   - Set the book's bids and asks to the sorted aggregated lists.
   - Return the combined order book.

`OrderBook`:

**OrderBook Class:**

- Stores buy and sell orders (asks and bids) as separate lists of `PriceVolume` objects.

**Adding Orders:**

- `add_bid_levels` and `add_ask_levels` functions take price-volume pairs and convert them to rounded `PriceVolume` objects before adding them to the corresponding lists (bids or asks).

**Calculating Average Price:**

1. **Helper function:** `calculate_weighted_average` finds the weighted average price for a list of `PriceVolume` objects (fills).

   - Calculates total price (sum of price \* volume for each entry).
   - Calculates total volume (sum of volume for each entry).
   - Divides total price by total volume (weighted average).

2. **Buy and Sell Calculations:**

   - Iterate through asks (buy) and bids (sell) in opposite price orders (ascending for asks, descending for bids).
   - Track purchased/sold volume (`buy_amount`/`sell_amount`).
   - Fill a list (`buy_fills`/`sell_fills`) with `PriceVolume` objects representing the orders used to reach the target quantity.
   - Stop iterating when the target quantity is fulfilled.

3. **Average Price Calculation:**

   - Use the helper function to calculate the average price for both buy and sell fills.

4. **Return Results:**
   - Return the average buy price and average sell price.

`PriceVolume`
It's a simple data structure (normalized form) used throughout the code to represent a single order level within an order book. Here's a breakdown of its functionality:

**Functionality:**

- **Initialization (`__init__`):**

  - Takes two arguments: `price` (float) and `volume` (float).
  - Initializes two attributes:
    - `self.price`: Stores the price of the order.
    - `self.volume`: Stores the volume (quantity) associated with the order.

- **String Representation (`__repr__`):**
  - Defines how the object is represented as a string (useful for debugging).
  - Returns a string formatted as `[Price: {price} Amount: {volume}]`, displaying both price and volume values.

**Overall, the `PriceVolume` class acts as a building block to represent individual price and volume combinations within order books.**

The CoinBaseConnector,Gemini & Kraken class provides a way to interact
with the Coinbase Pro, gemini,kraken API to fetch order book data for a specific symbol.
It handles making the API request, parsing the JSON response, extracting relevant ask and bid data,
and creating an OrderBook object to store the retrieved information.
It also offers a method to print the contents of the fetched order book.
