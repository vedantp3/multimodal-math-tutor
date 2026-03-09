"""Solver Agent — Solves math problems using RAG context and Python tools."""
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from utils.python_executor import execute_python


class SolverAgent:
    """Solves math problems using retrieved context, memory, and computational tools."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.name = "Solver Agent"
    
    def solve(self, parsed_problem: dict, route_info: dict, 
              rag_context: str, memory_context: str = "") -> dict:
        """Solve the math problem.
        
        Args:
            parsed_problem: Structured problem from Parser Agent.
            route_info: Routing info from Router Agent.
            rag_context: Retrieved knowledge base context.
            memory_context: Context from similar previously-solved problems.
        
        Returns:
            dict with keys: solution, steps, python_verification
        """
        memory_section = ""
        if memory_context:
            memory_section = f"""
## Previously Solved Similar Problems
The following similar problems were solved before. Use these as reference if helpful:
{memory_context}
"""
        
        use_python = "python_calculator" in route_info.get("tools_needed", [])
        
        python_instruction = ""
        if use_python:
            python_instruction = """
## Python Verification
After solving, provide a Python code block that verifies the numerical answer.
The code should compute the answer and print it. Use only basic math operations and the math module.
Wrap the code in a ```python code block.
"""
        
        prompt = f"""You are an expert math tutor solving a JEE-level problem. Solve this problem step by step.

## Problem
{json.dumps(parsed_problem, indent=2)}

## Solving Strategy
Topic: {route_info.get('topic', 'general')}
Subtopic: {route_info.get('subtopic', 'unknown')}
Approach: {route_info.get('approach', 'Direct solving')}

## Relevant Formulas & Context (from knowledge base)
{rag_context}
{memory_section}
{python_instruction}

## Instructions
1. State what is given and what needs to be found
2. Identify the relevant formulas/concepts from the context above
3. Solve step by step with clear mathematical reasoning
4. State the final answer clearly
5. Show all intermediate calculations

Use LaTeX notation for mathematical expressions where appropriate (e.g., $x^2$, $\\frac{{a}}{{b}}$, $\\sqrt{{x}}$).

Provide your response as a clear, structured solution."""

        try:
            response = self.model.generate_content(prompt)
            solution_text = response.text
            
            # Try to extract and run Python verification code
            python_result = None
            if use_python:
                python_result = self._extract_and_run_python(solution_text)
            
            return {
                "solution": solution_text,
                "python_verification": python_result
            }
            
        except Exception as e:
            return {
                "solution": f"Error solving problem: {str(e)}",
                "python_verification": None
            }
    
    def _extract_and_run_python(self, text: str) -> dict | None:
        """Extract Python code from solution text and execute it."""
        # Find Python code blocks
        code_blocks = []
        lines = text.split("\n")
        in_python_block = False
        current_block = []
        
        for line in lines:
            if line.strip().startswith("```python"):
                in_python_block = True
                current_block = []
            elif line.strip() == "```" and in_python_block:
                in_python_block = False
                if current_block:
                    code_blocks.append("\n".join(current_block))
            elif in_python_block:
                current_block.append(line)
        
        if not code_blocks:
            return None
        
        # Execute the last Python code block (usually the verification)
        code = code_blocks[-1]
        result = execute_python(code)
        return result
