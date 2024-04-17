class PriceVolume:
    def __init__(self, price, volume):
        # Initialize PriceData object with price and amount
        self.price = price
        self.volume = volume

    def __repr__(self):
        # String representation of the PriceData object. (Mainly for debugging)
        return f"[Price: {self.price} Amount: {self.volume}]"
