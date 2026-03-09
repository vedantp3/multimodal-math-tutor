"""Parser Agent — Converts raw input text into a structured math problem."""
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class ParserAgent:
    """Cleans OCR/ASR output and converts to structured format."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.name = "Parser Agent"
    
    def parse(self, raw_text: str) -> dict:
        """Parse raw text into a structured math problem.
        
        Args:
            raw_text: Raw text from OCR, ASR, or user input.
        
        Returns:
            dict with keys: problem_text, topic, variables, constraints,
            needs_clarification, clarification_reason
        """
        prompt = f"""You are a math problem parser. Analyze the following raw text and extract a structured math problem.

Raw input text:
\"\"\"{raw_text}\"\"\"

Return a JSON object with exactly these fields:
{{
    "problem_text": "The cleaned, well-formatted math problem statement",
    "topic": "one of: algebra, probability, calculus, linear_algebra, general",
    "variables": ["list", "of", "variables", "used"],
    "constraints": ["list of constraints like x > 0"],
    "needs_clarification": true/false,
    "clarification_reason": "reason why clarification is needed, or empty string"
}}

Rules:
- Clean up any OCR/ASR artifacts (weird characters, broken formatting)
- Identify the math topic accurately
- Extract all variables mentioned in the problem
- Identify any constraints (domain restrictions, given conditions)
- Set needs_clarification to true ONLY if the problem is genuinely ambiguous or incomplete
- Return ONLY the JSON object, no other text"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            result = json.loads(response.text)
            return result
        except Exception as e:
            return {
                "problem_text": raw_text,
                "topic": "general",
                "variables": [],
                "constraints": [],
                "needs_clarification": True,
                "clarification_reason": f"Parser error: {str(e)}"
            }
    
    def _clean_json_output(self, text: str) -> dict:
        """Extract and parse JSON from LLM response."""
        # Try to find JSON in the response
        text = text.strip()
        
        # Remove markdown code block markers
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
            # Try to find JSON within the text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            
            # Fallback
            return {
                "problem_text": text,
                "topic": "general",
                "variables": [],
                "constraints": [],
                "needs_clarification": True,
                "clarification_reason": "Failed to parse structured output from AI."
            }
