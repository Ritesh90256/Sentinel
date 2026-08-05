import hashlib

class ResponseCache:
    def __init__(self):
        self.cache = {}

    def generate_key(self, prompt: str, provider: str):
        data = f"{provider}:{prompt}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, prompt: str, provider: str):
        key = self.generate_key(prompt, provider)
        return self.cache.get(key)

    def set(self, prompt: str, provider: str, response: str):
        key = self.generate_key(prompt,provider)
        self.cache[key] = response