from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def encode(self, texts):
        return self.model.encode(texts).tolist()