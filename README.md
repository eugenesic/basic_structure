## Базовый пример архитектуры торгового бота (Python)

Минимальный учебный проект, показывающий архитектуру торгового бота:
источник данных → стратегия → риск‑менеджер → управление позицией → исполнение ордеров.

Используется для демонстрации в ролике, код специально упрощён.

### Структура проекта

```text
basic_structure/
  ├── main.py                        # Точка входа, собирает все модули и запускает цикл
  ├── config.yaml                    # Простые настройки демо (symbol, путь к CSV, risk_percent, equity)
  ├── event_bus.py                   # Простейшая событийная шина (pub/sub)
  ├── interfaces.py                  # Общие интерфейсы и DTO (Candle, Signal, ApprovedSignal, Protocol-ы)

  ├── market_data/
  │   ├── __init__.py
  │   ├── csv_provider.py            # Источник свечей из CSV-файла
  │   └── binance_ws.py              # Заглушка веб‑сокет провайдера (интерфейс совместим с CSV)

  ├── indicators/
  │   └── ema.py                     # Простейший расчёт EMA

  ├── strategies/
  │   └── ema_crossover.py          # Стратегия на пересечении быстрой и медленной EMA

  ├── risk/
  │   └── fixed_percent_risk.py     # Риск‑менеджер: фиксированный процент от капитала

  ├── position_management/
  │   └── simple_position_manager.py # Хранение текущей позиции по инструменту

  ├── execution/
  │   └── paper_executor.py          # Исполнитель ордеров «на бумаге» (paper trading)

  ├── app_logging/
  │   └── console_logger.py          # Простейший логгер событий в консоль

  └── data/
      ├── btc_1h.csv                 # Пример датасета с часовыми свечами
      └── generate_sample_data.py    # Скрипт генерации demo‑CSV
```

### Как это работает (RU)

1. `main.py`
   - Создаёт `EventBus`, провайдер маркет‑дат (`CSVMarketData`), стратегию, риск‑менеджер,
     менеджер позиций и исполнителя.
   - Подписывает на события:
     - `signal_generated` → логгер.
     - `signal_approved` → обновление позиции и исполнение ордера.
   - В цикле читает свечи из `market_data.subscribe()` и на каждую свечу
     вызывает стратегию, риск и публикует события в шину.

2. `market_data/csv_provider.py`
   - Читает CSV (`data/btc_1h.csv`) и отдаёт асинхронный поток свечей `Candle`.

3. `strategies/ema_crossover.py`
   - Считает быструю и медленную EMA.
   - При пересечении вверх генерирует `BUY`, при пересечении вниз — `CLOSE`.

4. `risk/fixed_percent_risk.py`
   - Ограничивает риск фиксированным процентом от капитала.
   - Возвращает `ApprovedSignal` с рассчитанным размером позиции или `None`.

5. `position_management/simple_position_manager.py`
   - Хранит текущий размер позиции по инструменту и применяет одобренные сигналы.

6. `execution/paper_executor.py`
   - «Исполняет» заявки и печатает результат в консоль (без реального брокера/биржи).

7. `app_logging/console_logger.py`
   - Пишет ключевые события (сигналы и т.п.) в консоль с таймстампами.

Все модули дополнительно печатают свой шаг работы в консоль, чтобы по логам
можно было объяснять архитектуру и последовательность действий.

---

## Basic trading bot architecture example (Python)

Minimal educational project demonstrating a trading bot architecture:
data source → strategy → risk manager → position management → order execution.

Code is intentionally simplified for video/demo purposes.

### Project structure

```text
basic_structure/
  ├── main.py                        # Entry point, wires all modules and runs the loop
  ├── config.yaml                    # Simple demo config (symbol, CSV path, risk_percent, equity)
  ├── event_bus.py                   # Simple event bus (pub/sub)
  ├── interfaces.py                  # Shared interfaces & DTOs (Candle, Signal, ApprovedSignal, Protocols)

  ├── market_data/
  │   ├── __init__.py
  │   ├── csv_provider.py            # Market data source from CSV file
  │   └── binance_ws.py              # WebSocket stub provider (same interface as CSV)

  ├── indicators/
  │   └── ema.py                     # Simple EMA calculation

  ├── strategies/
  │   └── ema_crossover.py          # EMA crossover strategy (fast vs slow EMA)

  ├── risk/
  │   └── fixed_percent_risk.py     # Fixed‑percent risk manager

  ├── position_management/
  │   └── simple_position_manager.py # In‑memory position tracking

  ├── execution/
  │   └── paper_executor.py          # Paper trading order executor

  ├── app_logging/
  │   └── console_logger.py          # Simple console event logger

  └── data/
      ├── btc_1h.csv                 # Sample dataset with 1h candles
      └── generate_sample_data.py    # Script to generate demo CSV
```

### How it works (EN)

1. `main.py`
   - Creates `EventBus`, market data provider (`CSVMarketData`), strategy,
     risk manager, position manager and executor.
   - Subscribes handlers to events:
     - `signal_generated` → logger.
     - `signal_approved` → position manager and executor.
   - In the main loop reads candles from `market_data.subscribe()` and for each
     candle calls the strategy, risk manager and publishes events to the bus.

2. `market_data/csv_provider.py`
   - Reads CSV (`data/btc_1h.csv`) and yields an async stream of `Candle` objects.

3. `strategies/ema_crossover.py`
   - Maintains fast and slow EMA.
   - On bullish crossover produces `BUY` signal, on bearish crossover — `CLOSE`.

4. `risk/fixed_percent_risk.py`
   - Limits risk by fixed percent of equity.
   - Returns `ApprovedSignal` with calculated size or `None`.

5. `position_management/simple_position_manager.py`
   - Stores current position size per symbol and applies approved signals.

6. `execution/paper_executor.py`
   - "Executes" orders and prints the result to console (no real broker/exchange).

7. `app_logging/console_logger.py`
   - Logs key events (signals etc.) to console with timestamps.

Each module prints its own steps to the console, so you can narrate the
architecture and execution flow directly from the logs.