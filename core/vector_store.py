import chromadb

from core.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="database/chroma"
        )

        self.embedding_model = EmbeddingModel()

    def get_collection(self, collection_name):

        return self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(self, collection_name, documents):

        collection = self.get_collection(collection_name)

        embeddings = self.embedding_model.encode(documents)

        ids = [f"doc_{i}" for i in range(len(documents))]

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )

    def search(self, collection_name, query, n_results=3):

        collection = self.get_collection(collection_name)

        query_embedding = self.embedding_model.encode([query])

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results