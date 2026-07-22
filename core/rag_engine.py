from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.vector_store import VectorStore


class RAGEngine:

    def __init__(self):

        self.vector_store = VectorStore()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                ""
            ]
        )

    # ---------------------------------------------------

    def index_video(self, video_id: str, transcript: str):

        # Skip if already indexed
        if self.vector_store.collection_exists(video_id):

            collection = self.vector_store.get_collection(video_id)

            if collection.count() > 0:
                return

        transcript = transcript.strip()

        if not transcript:
            raise ValueError("Transcript is empty.")

        docs = self.splitter.create_documents(
            [transcript]
        )

        documents = [

            doc.page_content.strip()

            for doc in docs

            if doc.page_content.strip()

        ]

        if not documents:
            raise ValueError(
                "Unable to generate transcript chunks."
            )

        self.vector_store.add_documents(
            collection_name=video_id,
            documents=documents
        )

    # ---------------------------------------------------

    def search(
        self,
        video_id,
        question,
        top_k=4
    ):

        return self.vector_store.search(
            collection_name=video_id,
            query=question,
            n_results=top_k
        )

    # ---------------------------------------------------

    def is_indexed(
        self,
        video_id
    ):

        return self.vector_store.collection_exists(
            video_id
        )

    # ---------------------------------------------------

    def delete_video(
        self,
        video_id
    ):

        self.vector_store.delete_collection(
            video_id
        )

    # ---------------------------------------------------

    def indexed_videos(self):

        return self.vector_store.list_collections()