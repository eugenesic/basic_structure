from decimal import Decimal
from interfaces import ApprovedSignal

# position_management/simple_position_manager.py
class SimplePositionManager:
    def __init__(self):
        self.positions = {"BTCUSDT": Decimal('0')}

    def get_position_size(self, symbol: str) -> Decimal:
        return self.positions.get(symbol, Decimal('0'))

    def apply_signal(self, approved: ApprovedSignal):
        if approved.direction == "CLOSE":
            self.positions[approved.symbol] = Decimal('0')
            print(f"[POSITION] Position closed for {approved.symbol}")
        else:
            self.positions[approved.symbol] = approved.size if approved.direction == "BUY" else -approved.size
            print(f"[POSITION] Position updated: {approved.direction} {approved.size} {approved.symbol}")