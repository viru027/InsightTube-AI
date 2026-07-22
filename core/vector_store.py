import re
import streamlit as st
import chromadb

from core.embeddings import EmbeddingModel


@st.cache_resource(show_spinner=False)
def get_chroma_client():
    return chromadb.PersistentClient(
        path="database/chroma"
    )


class VectorStore:

    def __init__(self):

        self.client = get_chroma_client()
        self.embedding_model = EmbeddingModel()

    # ----------------------------------------

    def _safe_collection_name(self, name):

        # Replace invalid characters
        safe = re.sub(r"[^a-zA-Z0-9._-]", "_", name)

        # Chroma requires first character to be alphanumeric
        if not safe[0].isalnum():
            safe = "video" + safe

        return safe

    # ----------------------------------------

    def get_collection(self, collection_name):

        collection_name = self._safe_collection_name(collection_name)

        return self.client.get_or_create_collection(
            name=collection_name
        )

    # ----------------------------------------

    def add_documents(self, collection_name, documents):

        collection_name = self._safe_collection_name(collection_name)

        collection = self.get_collection(collection_name)

        try:
            if collection.count() > 0:
                return
        except Exception:
            pass

        embeddings = self.embedding_model.encode(documents)

        ids = [
            f"{collection_name}_{i}"
            for i in range(len(documents))
        ]

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
        )

    # ----------------------------------------

    def search(
        self,
        collection_name,
        query,
        n_results=4,
    ):

        collection_name = self._safe_collection_name(collection_name)

        collection = self.get_collection(collection_name)

        if collection.count() == 0:
            return {"documents": [[]]}

        query_embedding = self.embedding_model.encode([query])

        return collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, collection.count()),
        )

    # ----------------------------------------

    def delete_collection(self, collection_name):

        collection_name = self._safe_collection_name(collection_name)

        try:
            self.client.delete_collection(
                collection_name
            )
        except Exception:
            pass

    # ----------------------------------------

    def collection_exists(self, collection_name):

        collection_name = self._safe_collection_name(collection_name)

        try:
            self.client.get_collection(
                collection_name
            )
            return True
        except Exception:
            return False

    # ----------------------------------------

    def list_collections(self):

        return [
            c.name
            for c in self.client.list_collections()
        ]