import streamlit as st
from sentence_transformers import SentenceTransformer


# ==========================================
# CACHE EMBEDDING MODEL
# ==========================================

@st.cache_resource(show_spinner=False)
def load_embedding_model():
    """
    Loads the embedding model only once during
    the lifetime of the Streamlit app.
    """

    print("Loading embedding model...")

    return SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )


# ==========================================
# EMBEDDING MODEL
# ==========================================

class EmbeddingModel:

    def __init__(self):

        self.model = load_embedding_model()

    def encode(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()