import csv
from datetime import datetime, timedelta


def generate(path: str, start_price: float = 40000.0, hours: int = 100):
    start = datetime(2024, 1, 1, 0, 0, 0)
    price = start_price

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])

        for i in range(hours):
            ts = start + timedelta(hours=i)
            o = price
            h = o + 10
            l = o - 10
            c = o + 5
            v = 10 + (i % 5)
            writer.writerow([
                ts.isoformat(),
                f"{o:.0f}",
                f"{h:.0f}",
                f"{l:.0f}",
                f"{c:.0f}",
                f"{v}",
            ])
            price = c


if __name__ == "__main__":
    generate("btc_1h.csv")
