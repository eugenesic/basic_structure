# market_data/csv_provider.py
import csv
from datetime import datetime
from decimal import Decimal
from interfaces import IMarketData, Candle
import asyncio

class CSVMarketData:
    def __init__(self, filepath: str):
        self.filepath = filepath

    async def subscribe(self, symbol: str = "BTCUSDT"):
        print(f"[MARKET_DATA] Start streaming from CSV: {self.filepath} for symbol={symbol}")
        with open(self.filepath, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                candle = Candle(
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    open=Decimal(row['open']),
                    high=Decimal(row['high']),
                    low=Decimal(row['low']),
                    close=Decimal(row['close']),
                    volume=Decimal(row['volume'])
                )
                print(f"[MARKET_DATA] Yield candle ts={candle.timestamp}, close={candle.close}")
                yield candle
                await asyncio.sleep(0.1)  # имитация реального времени