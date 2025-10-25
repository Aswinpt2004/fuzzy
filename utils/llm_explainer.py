# utils/llm_explainer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def explain_with_llm(context, mf_type, params, prompt):
    """
    Generate branded, math-rendered explanations using Gemini.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        full_prompt = f"""
        You are "Aswin's Fuzzy Toolbox", an educational fuzzy logic assistant.

        Produce a clear, structured explanation of the given fuzzy membership function.
        The tone should be **academic, visual, and student-friendly**.
        Include:
        - Section titles with ### headings
        - Bullet points for clarity
        - Equations using LaTeX in $$ ... $$ blocks for math rendering
        - Avoid redundant introductions like "Of course!" or "I'm happy to explain"
        - Start the output with: "🧠 **Aswin’s Fuzzy Toolbox** is here to explain this function clearly."

        Context: {context}
        Type: {mf_type}
        Parameters: {params}

        Task: {prompt}
        """

        response = model.generate_content(full_prompt)
        explanation_md = response.text or "⚠️ No explanation returned."

        # Convert Markdown → HTML for browser display
        explanation_html = markdown(
            explanation_md,
            extensions=["fenced_code", "tables", "sane_lists"]
        )

        return explanation_html

    except Exception as e:
        return f"<p class='error'>⚠️ Gemini API error: {e}</p>"
