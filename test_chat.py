from core.rag_engine import RAGEngine
from core.chat_engine import ChatEngine

rag = RAGEngine()

question = "What is Python?"

results = rag.search(
    video_id="demo_video",
    question=question
)

context = "\n\n".join(results["documents"][0])

chat = ChatEngine()

answer = chat.ask(context, question)

print(answer)