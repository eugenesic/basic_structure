import asyncio
from datetime import datetime
from decimal import Decimal

from interfaces import Candle


class BinanceWSMarketData:
    async def subscribe(self, symbol: str = "BTCUSDT"):
        while True:
            now = datetime.utcnow()
            candle = Candle(
                timestamp=now,
                open=Decimal("0"),
                high=Decimal("0"),
                low=Decimal("0"),
                close=Decimal("0"),
                volume=Decimal("0"),
            )
            yield candle
            await asyncio.sleep(1)
