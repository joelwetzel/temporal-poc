def calculate_shipping_cost(amount: float) -> float:
    """Calculate the estimated shipping cost for an order."""
    return round(amount * 0.075, 2)
