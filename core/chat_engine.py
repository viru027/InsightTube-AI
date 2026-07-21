import google.generativeai as genai

from config import GEMINI_API_KEY,GEMINI_MODEL
from core.prompts import (
    STRICT_RAG_PROMPT,
    SUMMARY_PROMPT,
    SIMPLE_PROMPT,
    PROJECT_PROMPT,
    INTERVIEW_PROMPT,
    QUIZ_PROMPT,
    ROADMAP_PROMPT,
    CODING_PROMPT,
    RESUME_PROMPT,
    RESEARCH_PROMPT
)

genai.configure(api_key=GEMINI_API_KEY)


class ChatEngine:

    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)

        self.prompt_map = {
            "Ask Questions": STRICT_RAG_PROMPT,
            "Video Summary": SUMMARY_PROMPT,
            "Explain Simply": SIMPLE_PROMPT,
            "Project Ideas": PROJECT_PROMPT,
            "Interview Questions": INTERVIEW_PROMPT,
            "Quiz Generator": QUIZ_PROMPT,
            "Learning Roadmap": ROADMAP_PROMPT,
            "Coding Challenges": CODING_PROMPT,
            "Resume Project Builder": RESUME_PROMPT,
            "Research Topics": RESEARCH_PROMPT,
        }

    def generate_answer(self, context, question, mode):

        prompt_template = self.prompt_map.get(
            mode,
            STRICT_RAG_PROMPT
        )

        prompt = prompt_template.format(
            context=context,
            question=question
        )

        response = self.model.generate_content(prompt)

        return response.text