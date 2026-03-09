"""Image input handler — Gemini Vision OCR with confidence scoring."""
import base64
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class ImageHandler:
    """Extracts text from math problem images using Gemini Vision."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def extract_text(self, image_bytes: bytes, mime_type: str = "image/png") -> dict:
        """Extract math text from an image using Gemini Vision.
        
        Args:
            image_bytes: Raw image bytes.
            mime_type: MIME type of the image (image/png, image/jpeg).
        
        Returns:
            dict with keys: text, confidence (1-10), extraction_notes
        """
        prompt = """You are an OCR system specialized in extracting math problems from images.

Extract ALL text from this image, especially mathematical expressions, equations, and problem statements.

Return a JSON object with exactly these fields:
{
    "text": "The complete extracted text with proper mathematical notation",
    "confidence": 1-10 (how confident you are in the extraction accuracy),
    "extraction_notes": "any issues or uncertainties in the extraction"
}

Rules:
- Preserve mathematical symbols and notation as closely as possible
- Use standard notation: x², √x, ∫, Σ, π, etc.
- If handwriting is unclear, note it in extraction_notes and provide your best guess
- Rate confidence honestly: 10 = perfect clarity, 1 = barely readable
- Return ONLY the JSON object"""

        try:
            image_part = {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            }
            
            response = self.model.generate_content([prompt, image_part])
            result = self._clean_json_output(response.text)
            return result
            
        except Exception as e:
            return {
                "text": "",
                "confidence": 1,
                "extraction_notes": f"OCR failed: {str(e)}"
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
                "text": text,
                "confidence": 5,
                "extraction_notes": "Could not parse structured OCR output"
            }
