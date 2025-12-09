# strategies/ema_crossover.py
from interfaces import IStrategy, Signal, Candle
from indicators.ema import SimpleEMA
from decimal import Decimal

class EMACrossoverStrategy:
    def __init__(self, fast=12, slow=26):
        self.fast_ema = SimpleEMA(fast)
        self.slow_ema = SimpleEMA(slow)
        self.prev_fast = Decimal('0')
        self.prev_slow = Decimal('0')

    async def on_candle(self, candle: Candle, indicators=None, position_size: Decimal = Decimal('0')) -> Signal | None:
        print(f"[STRATEGY] on_candle ts={candle.timestamp}, close={candle.close}, position_size={position_size}")
        self.fast_ema.update(candle.close)
        self.slow_ema.update(candle.close)

        fast = self.fast_ema.get_value()
        slow = self.slow_ema.get_value()
        print(f"[STRATEGY] fast_ema={fast}, slow_ema={slow}, prev_fast={self.prev_fast}, prev_slow={self.prev_slow}")

        if fast > slow and self.prev_fast <= self.prev_slow and position_size <= 0:
            self.prev_fast, self.prev_slow = fast, slow
            signal = Signal("BTCUSDT", "BUY", Decimal('0.001'), "ema_crossover")
            print(f"[STRATEGY] Generated BUY signal: {signal}")
            return signal
        elif fast < slow and self.prev_fast >= self.prev_slow and position_size > 0:
            self.prev_fast, self.prev_slow = fast, slow
            signal = Signal("BTCUSDT", "CLOSE", Decimal('0'), "ema_crossover")
            print(f"[STRATEGY] Generated CLOSE signal: {signal}")
            return signal

        self.prev_fast, self.prev_slow = fast, slow
        print("[STRATEGY] No signal on this candle")
        return None