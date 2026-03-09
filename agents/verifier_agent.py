"""Verifier / Critic Agent — Checks solution correctness and confidence."""
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, VERIFIER_CONFIDENCE_THRESHOLD


class VerifierAgent:
    """Verifies math solutions for correctness, edge cases, and domain validity."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.name = "Verifier Agent"
    
    def verify(self, parsed_problem: dict, solution: str, 
               python_verification: dict = None) -> dict:
        """Verify the solution for correctness.
        
        Args:
            parsed_problem: Structured problem from Parser Agent.
            solution: Solution text from Solver Agent.
            python_verification: Optional Python execution result.
        
        Returns:
            dict with keys: is_correct, confidence, issues, edge_cases_checked,
            suggestions, needs_hitl
        """
        python_section = ""
        if python_verification:
            if python_verification.get("success"):
                python_section = f"\nPython verification output: {python_verification['output']}"
            else:
                python_section = f"\nPython verification FAILED with error: {python_verification.get('error', 'unknown')}"
        
        prompt = f"""You are a critical math verifier. Check this solution for correctness.

## Original Problem
{json.dumps(parsed_problem, indent=2)}

## Proposed Solution
{solution}
{python_section}

## Verification Checklist
Check ALL of the following:
1. Are the mathematical steps correct?
2. Is the final answer correct?
3. Are the units/dimensions consistent?
4. Are domain constraints satisfied (e.g., x > 0, denominators ≠ 0)?
5. Are edge cases handled?
6. Does the answer make sense in context?

Return a JSON object with exactly these fields:
{{
    "is_correct": true/false,
    "confidence": 0-100 (how confident you are in the verification),
    "issues": ["list of any issues found, empty if none"],
    "edge_cases_checked": ["list of edge cases you verified"],
    "suggestions": "any suggestions for improvement, or empty string"
}}

Be thorough but fair. Return ONLY the JSON object."""

        try:
            response = self.model.generate_content(prompt)
            result = self._clean_json_output(response.text)
            
            # Add HITL flag based on confidence
            confidence = result.get("confidence", 50)
            result["needs_hitl"] = confidence < VERIFIER_CONFIDENCE_THRESHOLD
            
            return result
            
        except Exception as e:
            return {
                "is_correct": False,
                "confidence": 0,
                "issues": [f"Verification error: {str(e)}"],
                "edge_cases_checked": [],
                "suggestions": "Verification failed. Please review manually.",
                "needs_hitl": True
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
                "is_correct": False,
                "confidence": 30,
                "issues": ["Could not parse verification output"],
                "edge_cases_checked": [],
                "suggestions": "Manual review recommended."
            }
