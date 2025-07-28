import random

def predict_eod_price(current_price: float) -> float:
    # Simulated increase or decrease
    fluctuation = random.uniform(-0.03, 0.05)  # -3% to +5%
    return round(current_price * (1 + fluctuation), 2)
