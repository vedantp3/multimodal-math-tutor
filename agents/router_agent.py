"""Intent Router Agent — Classifies problem type and routes workflow."""
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class RouterAgent:
    """Classifies math problems and determines the optimal solving strategy."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.name = "Router Agent"
    
    def route(self, parsed_problem: dict) -> dict:
        """Classify the problem and determine the solving approach.
        
        Args:
            parsed_problem: Structured problem from Parser Agent.
        
        Returns:
            dict with keys: topic, subtopic, approach, tools_needed, difficulty
        """
        prompt = f"""You are a math problem router. Analyze this structured problem and determine the optimal solving strategy.

Problem:
{json.dumps(parsed_problem, indent=2)}

Return a JSON object with exactly these fields:
{{
    "topic": "one of: algebra, probability, calculus, linear_algebra, general",
    "subtopic": "specific subtopic like 'quadratic equations', 'conditional probability', 'limits', 'matrix determinant'",
    "approach": "brief description of the recommended solving approach",
    "tools_needed": ["list of tools: 'rag_retrieval', 'python_calculator', 'step_by_step'"],
    "difficulty": "one of: easy, medium, hard"
}}

Rules:
- Choose the most specific topic category
- Recommend appropriate tools (always include 'rag_retrieval')
- Include 'python_calculator' for numerical computation problems
- Include 'step_by_step' always for clear explanation
- Return ONLY the JSON object"""

        try:
            response = self.model.generate_content(prompt)
            result = self._clean_json_output(response.text)
            return result
        except Exception as e:
            return {
                "topic": parsed_problem.get("topic", "general"),
                "subtopic": "unknown",
                "approach": "Direct solving with RAG context",
                "tools_needed": ["rag_retrieval", "step_by_step"],
                "difficulty": "medium"
            }
    
    def _clean_json_output(self, text: str) -> dict:
        """Extract and parse JSON from LLM response."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            return {
                "topic": "general",
                "subtopic": "unknown",
                "approach": "Direct solving",
                "tools_needed": ["rag_retrieval", "step_by_step"],
                "difficulty": "medium"
            }
