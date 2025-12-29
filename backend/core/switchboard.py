import asyncio
from typing import Dict, Any

MAX_LINES = 200

class OutboundLine:
    def __init__(self, line_id: int):
        self.line_id = line_id
        self.busy = False
        self.last_call_info: Dict[str, Any] = {}

class Switchboard:
    def __init__(self):
        self.lines = [OutboundLine(i) for i in range(MAX_LINES)]
        self.call_queue = asyncio.Queue()
        self.lock = asyncio.Lock()
        self.active_calls = 0

    async def start(self):
        workers = [asyncio.create_task(self.line_worker(line)) for line in self.lines]
        await self.call_queue.join()  # Wait until all calls are processed
        for w in workers:
            w.cancel()

    async def line_worker(self, line: OutboundLine):
        while True:
            call_request = await self.call_queue.get()
            async with self.lock:
                if not line.busy:
                    line.busy = True
                    self.active_calls += 1
                    try:
                        await self.handle_call(line, call_request)
                    finally:
                        line.busy = False
                        self.active_calls -= 1
            self.call_queue.task_done()

    async def handle_call(self, line: OutboundLine, call_request: Dict[str, Any]):
        # TODO: Integrate with your telephony API/hardware here
        line.last_call_info = call_request
        print(f"[Line {line.line_id}] Outbound call to {call_request['number']} (duration: {call_request['duration']}s)")
        await asyncio.sleep(call_request['duration'])  # Simulate call duration
        print(f"[Line {line.line_id}] Call ended.")

    async def add_call(self, call_request: Dict[str, Any]):
        await self.call_queue.put(call_request)

    def get_status(self):
        return {
            'active_calls': self.active_calls,
            'queued_calls': self.call_queue.qsize(),
            'lines': [
                {'line_id': line.line_id, 'busy': line.busy, 'last_call_info': line.last_call_info}
                for line in self.lines
            ]
        }

# Example usage (run this as a script to test):
if __name__ == "__main__":
    import random
    import sys
    async def main():
        switchboard = Switchboard()
        # Simulate 205 outbound call requests
        for i in range(205):
            await switchboard.add_call({
                'number': f'+12345678{i:03}',
                'duration': random.randint(5, 15)  # seconds
            })
        await switchboard.start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting cleanly.")
        sys.exit(0)
