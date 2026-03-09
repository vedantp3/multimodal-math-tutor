"""Explainer / Tutor Agent — Produces step-by-step student-friendly explanations."""
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class ExplainerAgent:
    """Generates clear, student-friendly explanations for JEE students."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.name = "Explainer Agent"
    
    def explain(self, parsed_problem: dict, solution: str, 
                verification: dict, route_info: dict) -> str:
        """Generate a step-by-step student-friendly explanation.
        
        Args:
            parsed_problem: Structured problem from Parser Agent.
            solution: Solution from Solver Agent.
            verification: Verification result from Verifier Agent.
            route_info: Routing info from Router Agent.
        
        Returns:
            Formatted explanation string.
        """
        issues_note = ""
        if verification.get("issues"):
            issues_note = f"\nNote: The verifier found these issues to address: {verification['issues']}"
        
        prompt = f"""You are a friendly, encouraging math tutor helping a JEE student. 
Create a clear, step-by-step explanation of this solution.

## Problem
{parsed_problem.get('problem_text', 'Unknown problem')}

## Topic
{route_info.get('topic', 'general')} — {route_info.get('subtopic', '')}

## Solution
{solution}
{issues_note}

## Instructions for the Explanation
1. **Start with a brief overview** of what concept/formula is being used (1-2 sentences)
2. **Break down into numbered steps** — each step should explain ONE thing
3. **Use simple language** — explain as if the student is seeing this type of problem for the first time
4. **Highlight key formulas** — put important formulas in LaTeX ($...$)
5. **Point out common mistakes** — warn about typical errors for this type of problem
6. **End with a summary** — restate the final answer and the key insight
7. **Add a "Pro Tip"** — share one JEE-specific tip for this type of problem

Keep the tone friendly and encouraging. Use phrases like "Notice that...", "The key insight here is...", "A common mistake is..."

Use LaTeX for all mathematical expressions (e.g., $x^2 + 1$, $\\frac{{a}}{{b}}$)."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate explanation: {str(e)}\n\nPlease refer to the solution above."
