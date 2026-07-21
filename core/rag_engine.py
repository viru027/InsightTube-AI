from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.vector_store import VectorStore


class RAGEngine:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        self.vector_store = VectorStore()

    def index_video(self, video_id, transcript):

        docs = self.splitter.create_documents([transcript])

        texts = [doc.page_content for doc in docs]

        self.vector_store.add_documents(
            collection_name=video_id,
            documents=texts
        )

    def search(self, video_id, question):

        return self.vector_store.search(
            collection_name=video_id,
            query=question
        )