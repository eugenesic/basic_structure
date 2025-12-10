# main.py
import asyncio
from decimal import Decimal
from event_bus import EventBus
from interfaces import *
from market_data.csv_provider import CSVMarketData
from indicators.ema import SimpleEMA
from strategies.ema_crossover import EMACrossoverStrategy
from risk.fixed_percent_risk import FixedPercentRisk
from position_management.simple_position_manager import SimplePositionManager
from execution.paper_executor import PaperExecutor
from app_logging.console_logger import log_event

async def main():
    print("[MAIN] start main()")
    bus = EventBus()
    print("[MAIN] EventBus created")
    market_data: IMarketData = CSVMarketData("data/btc_1h.csv")  # ← поменять на BinanceWS — НИЧЕГО не сломается
    print("[MAIN] MarketData provider created (CSVMarketData)")
    strategy = EMACrossoverStrategy()
    print("[MAIN] Strategy created (EMACrossoverStrategy)")
    risk = FixedPercentRisk(risk_percent=1.0, equity=Decimal('10000'))
    print("[MAIN] RiskManager created (FixedPercentRisk)")
    position_manager = SimplePositionManager()
    print("[MAIN] PositionManager created (SimplePositionManager)")
    executor = PaperExecutor()
    print("[MAIN] Executor created (PaperExecutor)")

    # === Подписки на события ===
    print("[MAIN] Subscribing handlers to EventBus")
    bus.subscribe("signal_generated", lambda s: log_event("SIGNAL", s))
    bus.subscribe("signal_approved", lambda a: position_manager.apply_signal(a))
    bus.subscribe("signal_approved", lambda a: asyncio.create_task(executor.execute(a)))

    # === Основной цикл ===
    print("[MAIN] Entering main loop")
    equity = Decimal('10000')
    async for candle in market_data.subscribe("BTCUSDT"): # Отсюда берутся свечи, market_data — это CSVMarketData("data/btc_1h.csv").
        print(f"[MAIN] New candle: ts={candle.timestamp}, close={candle.close}") # Логгирует свечу
        position_size = position_manager.get_position_size("BTCUSDT") # Берёт текущий размер позиции из SimplePositionManager.
        print(f"[MAIN] Current position size: {position_size}")

        # Стратегия могла сгенерировать сигнал внутри on_candle
        print("[MAIN] Calling strategy.on_candle")
        signal = await strategy.on_candle(candle, None, position_size) # Вызывает стратегию напрямую

        if signal: # Если есть signal
            print(f"[MAIN] Strategy produced signal: {signal}")
            await bus.publish("signal_generated", signal) # Публикует событие signal_generated в EventBus (это нужно только, чтобы логгер увидел сигнал)
            print("[MAIN] Passing signal to risk manager")
            approved = risk.approve(signal, equity, position_manager.get_position_size("BTCUSDT")) # Передаёт сигнал в риск‑менеджер
            if approved:
                print(f"[MAIN] Risk manager approved signal: {approved}")
                await bus.publish("signal_approved", approved)
            else:
                print("[MAIN] Risk manager rejected signal")

if __name__ == "__main__":
    asyncio.run(main())