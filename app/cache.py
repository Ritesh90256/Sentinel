import hashlib
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

class ResponseCache:
    def __init__(self):
        self.cache = {}
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.similarity_threshold = 0.80

    def generate_key(self, prompt: str, provider: str):
        data = f"{provider}:{prompt}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, prompt: str, provider: str):
        key = self.generate_key(prompt, provider)

        exact_match = self.cache.get(key)

        if exact_match is not None:
            return exact_match["response"]

        query_embedding = self.embedding_model.encode(
            prompt,
            convert_to_tensor = True
        )

        for entry in self.cache.values():

            if entry["provider"] != provider:
                continue

            similarity = cos_sim(
                query_embedding,
                entry["embedding"]
            ).item()

            if similarity >= self.similarity_threshold:
                print(
                    f"Semantic cache hit! Similarity: {similarity:.3f}"
                )
                return entry["response"]

        return None


    def set(self, prompt: str, provider: str, response: str):
        key = self.generate_key(prompt,provider)

        embedding = self.embedding_model.encode(
            prompt,
            convert_to_tensor = True
        )

        self.cache[key] = {
            "prompt" : prompt,
            "provider" : provider,
            "embedding" : embedding,
            "response" : response
        }       
