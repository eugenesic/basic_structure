# indicators/ema.py
from decimal import Decimal

class SimpleEMA:
    def __init__(self, period: int):
        self.period = period
        self.alpha = Decimal('2') / (period + 1)
        self.ema: Decimal | None = None

    def update(self, price: Decimal):
        if self.ema is None:
            self.ema = price
        else:
            self.ema = self.alpha * price + (1 - self.alpha) * self.ema

    def get_value(self) -> Decimal:
        return self.ema or Decimal('0')