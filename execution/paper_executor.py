# execution/paper_executor.py
import asyncio

class PaperExecutor:
    async def execute(self, approved):
        print(f"[EXECUTOR] EXECUTED: {approved.direction} {approved.size} {approved.symbol} (paper trading)")
        await asyncio.sleep(0.1)