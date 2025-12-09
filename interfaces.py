# interfaces.py
from typing import Protocol, AsyncIterator
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Candle:
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

@dataclass
class Signal:
    symbol: str
    direction: str  # "BUY" / "SELL" / "CLOSE"
    size: Decimal   # сколько хотим (в контрактах/монетах)
    strategy_name: str

@dataclass
class ApprovedSignal:
    symbol: str
    direction: str
    size: Decimal
    strategy_name: str

class IMarketData(Protocol):
    async def subscribe(self, symbol: str) -> AsyncIterator[Candle]: ...

class IIndicatorEngine(Protocol):
    def update(self, candle: Candle): ...
    def get_ema(self, period: int) -> Decimal: ...

class IStrategy(Protocol):
    async def on_candle(self, candle: Candle, indicators: IIndicatorEngine, position_size: Decimal) -> Signal | None: ...

class IRiskManager(Protocol):
    def approve(self, signal: Signal, current_equity: Decimal, current_position: Decimal) -> ApprovedSignal | None: ...

class IPositionManager(Protocol):
    def update_from_fill(self, symbol: str, size: Decimal, price: Decimal, direction: str): ...
    def get_position_size(self, symbol: str) -> Decimal: ...
    def apply_signal(self, approved: ApprovedSignal): ...

class IExecutor(Protocol):
    async def execute(self, approved: ApprovedSignal): ...