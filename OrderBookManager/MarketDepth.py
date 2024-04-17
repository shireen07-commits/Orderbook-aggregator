from PriceVolume import PriceVolume


class OrderBook:
    def __init__(self):
        # Initialize empty lists for asks and bids
        self.asks = []
        self.bids = []

    def __repr__(self):
        # String representation of the order book
        return f"Asks: {self.asks}\nBids: {self.bids}"

    def add_bid_levels(self, bids):
        # add bids with new data
        # Convert input data to PriceData objects and round values
        self.bids = [PriceVolume(round(float(price), 2), round(float(volume), 7)) for price, volume in bids]

    def add_ask_levels(self, asks):
        # Update asks with new data
        # Convert input data to PriceData objects and round values
        self.asks = [PriceVolume(round(float(price), 2), round(float(volume), 7)) for price, volume in asks]

    def calculate_average_price(self, target_quantity=10.0):
        # Static method to calculate average buy and sell prices for a target quantity given an order book

        def calculate_weighted_average(fills):
            # Helper function to calculate the weighted average of a list of fills
            total_price = sum(entry.price * entry.volume for entry in fills)
            total_quantity = sum(entry.volume for entry in fills)
            return total_price / total_quantity if total_quantity != 0 else 0.0

        # Buys calculations
        buy_amount = 0.0
        buy_fills = []
        for ask_level in self.asks:
            if buy_amount + ask_level.volume > target_quantity:
                fill = PriceVolume(ask_level.price, target_quantity-buy_amount)
                buy_fills.append(fill)
                buy_amount += target_quantity-buy_amount
                break
            else:
                buy_fills.append(ask_level)
                buy_amount += ask_level.volume

        # Sells calculations
        sell_amount = 0.0
        sell_fills = []
        for bid_level in self.bids:
            if sell_amount + bid_level.volume > target_quantity:
                fill = PriceVolume(bid_level.price, target_quantity-sell_amount)
                sell_fills.append(fill)
                sell_amount += target_quantity-sell_amount
                break
            else:
                sell_fills.append(bid_level)
                sell_amount += bid_level.volume

        # Calculate average buy and sell prices
        average_buy_price = calculate_weighted_average(buy_fills)
        average_sell_price = calculate_weighted_average(sell_fills)

        return average_buy_price, average_sell_price
