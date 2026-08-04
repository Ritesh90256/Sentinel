import time

class TokenBucket:

    def __init__(self, capacity:int, refill_rate:float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def _refill(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_refill

        new_tokens = elapsed_time * self.refill_rate

        self.tokens = min(
            self.capacity,
            self.tokens + new_tokens
        )

        self.last_refill = current_time

    def allow_request(self):
        self._refill()

        if self.tokens >= 1:
            self.tokens -=1
            return True

        return False