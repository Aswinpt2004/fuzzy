# utils/llm_explainer.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def explain_with_llm(context, mf_type, params, prompt):
    '''
    Generate branded, math-rendered explanations using Gemini.
    '''
    try:
        model = genai.GenerativeModel("gemini-pro-latest")

        full_prompt = f'''
You are "Aswin's Fuzzy Toolbox", an educational fuzzy logic assistant.

Create a well-structured Markdown explanation with proper formatting.

IMPORTANT FORMATTING RULES:
- Use ### for main section headings
- Use #### for subsections  
- Start new paragraphs with blank lines between them
- Use proper bullet points with * or -
- Number steps clearly as 1., 2., 3.
- Use $$ ... $$ on separate lines for block math
- Use $ ... $ for inline math
- Keep paragraphs short and digestible
- Add blank lines before and after lists and math blocks

Structure with these sections:

### Definition of the Function
### Parameters and Their Roles
### Graphical Intuition
### Mathematical Formulation
### Step-by-Step Calculation
### Real-World Example

Requirements:
- Start with: "**Aswin's Fuzzy Toolbox** is here to explain this function clearly."
- Explain every step in detail for beginners
- Use actual numbers from the calculation
- Make the response academic yet friendly

Context: {context}
Type: {mf_type}
Parameters: {params}
Task: {prompt}
'''

        response = model.generate_content(full_prompt)
        explanation_md = response.text or "No explanation returned."

        # Convert Markdown to HTML but preserve LaTeX for MathJax
        # First, protect LaTeX expressions from markdown processing
        import re
        
        # Store LaTeX expressions temporarily
        latex_blocks = []
        latex_inline = []
        
        # Replace block math $$ ... $$ with placeholders
        def save_block_math(match):
            latex_blocks.append(match.group(0))
            return f"LATEX_BLOCK_{len(latex_blocks)-1}"
        
        # Replace inline math $ ... $ with placeholders
        def save_inline_math(match):
            latex_inline.append(match.group(0))
            return f"LATEX_INLINE_{len(latex_inline)-1}"
        
        # Protect LaTeX from markdown
        explanation_md = re.sub(r'\$\$(.+?)\$\$', save_block_math, explanation_md, flags=re.DOTALL)
        explanation_md = re.sub(r'\$(.+?)\$', save_inline_math, explanation_md)
        
        # Convert Markdown to HTML
        explanation_html = markdown(
            explanation_md,
            extensions=["fenced_code", "tables", "sane_lists", "nl2br"]
        )
        
        # Restore LaTeX expressions
        for i, latex in enumerate(latex_blocks):
            explanation_html = explanation_html.replace(f"LATEX_BLOCK_{i}", latex)
        for i, latex in enumerate(latex_inline):
            explanation_html = explanation_html.replace(f"LATEX_INLINE_{i}", latex)

        return explanation_html

    except Exception as e:
        return f"<p class='error'>Gemini API error: {e}</p>"
