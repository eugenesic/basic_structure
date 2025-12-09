# risk/fixed_percent_risk.py
from interfaces import IRiskManager, Signal, ApprovedSignal
from decimal import Decimal

class FixedPercentRisk:
    def __init__(self, risk_percent: float = 1.0, equity: Decimal = Decimal('10000')):
        self.risk_percent = Decimal(str(risk_percent)) / 100
        self.equity = equity

    def approve(self, signal: Signal, current_equity: Decimal, current_position: Decimal) -> ApprovedSignal | None:
        print(f"[RISK] Got signal={signal}, equity={current_equity}, current_position={current_position}")
        if current_position != 0:  # уже в позиции — не открываем новую
            if signal.direction == "BUY":
                print("[RISK] Reject BUY: already in position")
                return None

        risk_amount = current_equity * self.risk_percent
        size = risk_amount / Decimal('5000')  # грубая оценка: 1% риска ≈ 5000$ движения
        if signal.direction in ("BUY", "SELL"):
            approved = ApprovedSignal(signal.symbol, signal.direction, size, signal.strategy_name)
            print(f"[RISK] Approved signal with size={size}: {approved}")
            return approved
        print("[RISK] Signal not approved (unsupported direction)")
        return None