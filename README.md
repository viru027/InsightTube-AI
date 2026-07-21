# 🎥 InsightTube AI

<p align="center">
  <img src="assets/banner.png" alt="InsightTube AI Banner" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?style=for-the-badge&logo=google)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple?style=for-the-badge)

</p>

---

## 🚀 Overview

**InsightTube AI** is an AI-powered Video Intelligence Platform that transforms YouTube videos into an interactive learning experience.

Instead of watching lengthy videos repeatedly, users can ask questions, generate summaries, create quizzes, prepare for interviews, discover project ideas, and receive personalized learning roadmaps—all powered by **Retrieval-Augmented Generation (RAG)**.

The application combines **Whisper**, **Sentence Transformers**, **ChromaDB**, and **Google Gemini** to deliver accurate, context-aware answers directly from video transcripts.

---

## ✨ Features

### 📹 Video Processing
- Extract audio from YouTube videos
- Automatic speech-to-text transcription using Whisper
- Transcript visualization

### 🤖 AI Chat
- Context-aware Q&A
- Semantic search using vector embeddings
- Retrieval-Augmented Generation (RAG)
- Hallucination reduction through transcript grounding

### 📚 AI Learning Modes

- 📄 Video Summary
- 💡 Explain Simply
- 🚀 Project Ideas
- 💼 Resume Project Builder
- ❓ Interview Questions
- 📝 Quiz Generator
- 🗺️ Learning Roadmap
- 💻 Coding Challenges
- 🔬 Research Topics

### 🧠 Intelligent Retrieval

- Semantic search using ChromaDB
- Vector embeddings with Sentence Transformers
- Relevant transcript chunk retrieval
- Context-aware Gemini responses

---

# 🏗 System Architecture

```
                 YouTube Video
                        │
                Audio Extraction
                        │
                 Whisper Transcription
                        │
                 Transcript Chunking
                        │
             Sentence Transformer Embeddings
                        │
                  ChromaDB Vector Store
                        │
               Semantic Similarity Search
                        │
                 Google Gemini (LLM)
                        │
              AI-Powered Intelligent Response
```

---

# 📂 Project Structure

```
InsightTube-AI
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── core
│   ├── chat_engine.py
│   ├── embeddings.py
│   ├── extractor.py
│   ├── prompts.py
│   ├── rag_engine.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── database
│
├── assets
│
└── modules
```

---

# ⚙️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Framework | Streamlit |
| LLM | Google Gemini |
| Speech Recognition | OpenAI Whisper |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| NLP | LangChain |
| AI Technique | Retrieval-Augmented Generation (RAG) |

---

# 📦 Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/InsightTube-AI.git
```

```bash
cd InsightTube-AI
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

### Run Application

```bash
streamlit run app.py
```

---

# 📸 Screenshots

### Home Page

> Add screenshot here

---

### AI Chat

> Add screenshot here

---

### Video Summary

> Add screenshot here

---

### Quiz Generator

> Add screenshot here

---

### Project Ideas

> Add screenshot here

---

# 🎯 Example Use Cases

- Learn from long YouTube tutorials quickly
- Prepare for technical interviews
- Generate revision notes
- Create quizzes from educational videos
- Build projects based on tutorials
- Understand difficult concepts simply
- Generate learning roadmaps

---

# 🌟 Future Improvements

- Multi-video knowledge base
- PDF and DOCX support
- Chat history
- Export AI responses as PDF
- Flashcards
- Mind maps
- Voice interaction
- Multi-language support
- Team collaboration

---

# 📈 Resume Highlights

- Developed an AI-powered Retrieval-Augmented Generation (RAG) platform for YouTube video intelligence.
- Implemented semantic search using Sentence Transformers and ChromaDB.
- Integrated Google Gemini for context-aware conversational AI.
- Automated speech-to-text transcription using Whisper.
- Designed an interactive Streamlit application supporting AI summaries, quizzes, interview preparation, project generation, and learning roadmaps.

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve InsightTube AI:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Viraj Patil**

📧 Email: 27virajpatil@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/viraj-patil-43195a223

💻 GitHub: https://github.com/viraj2700

---

## ⭐ If you found this project helpful, consider giving it a Star!
