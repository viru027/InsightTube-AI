from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL
from config import GEMINI_MODEL

print("GEMINI_MODEL =", GEMINI_MODEL)

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
    RESEARCH_PROMPT,
)


class ChatEngine:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

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

    # -----------------------------------------------------

    def build_prompt(
        self,
        context,
        question,
        mode,
    ):

        template = self.prompt_map.get(
            mode,
            STRICT_RAG_PROMPT
        )

        return template.format(
            context=context,
            question=question
        )

    # -----------------------------------------------------

    def generate_answer(
        self,
        context,
        question,
        mode,
    ):

        prompt = self.build_prompt(
            context=context,
            question=question,
            mode=mode,
        )

        try:

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt,

            )

            if response.text:

                return response.text

            return "No response generated."

        except Exception as e:

            return f"⚠️ Gemini Error:\n\n{str(e)}"