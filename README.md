/basic_structure/
  ├── main.py
  ├── config.yaml
  ├── event_bus.py
  ├── interfaces.py
  ├── /market_data/
  │   ├── __init__.py
  │   └── csv_provider.py          # можно добавить binance_ws.py — просто реализует тот же интерфейс
  ├── /indicators/
  │   └── ema.py
  ├── /strategies/
  │   └── ema_crossover.py
  ├── /risk/
  │   └── fixed_percent_risk.py
  ├── /position_management/
  │   └── simple_position_manager.py
  ├── /execution/
  │   └── paper_executor.py
  └── /logging/
      └── console_logger.py