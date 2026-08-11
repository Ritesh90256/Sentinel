class RequestQueue:

    def __init__(
            self,
            max_size: int = 10
    ):
        self.max_size = max_size
        self.current_requests = 0

    def enter(self):
        if self.current_requests >= self.max_size:
            return False

        self.current_requests += 1
        return True

    def leave(self):
        if self.current_requests > 0 :
            self.current_requests -= 1
