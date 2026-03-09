"""Audio input handler — Gemini ASR with math-specific phrase handling."""
import base64
import json
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL


class AudioHandler:
    """Transcribes math audio using Gemini with math-specific phrase handling."""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def transcribe(self, audio_bytes: bytes, mime_type: str = "audio/wav") -> dict:
        """Transcribe audio containing a math problem.
        
        Args:
            audio_bytes: Raw audio bytes.
            mime_type: MIME type (audio/wav, audio/mp3, audio/m4a, audio/mpeg).
        
        Returns:
            dict with keys: text, confidence (1-10), transcription_notes
        """
        prompt = """You are a math-specialized speech-to-text system. Transcribe this audio recording of a math problem.

Convert the spoken math into proper mathematical notation:
- "square root of x" → √x
- "x squared" or "x to the power 2" → x²
- "x cubed" → x³  
- "raised to the power n" → ^n
- "integral of" → ∫
- "summation" or "sigma" → Σ
- "pi" → π
- "theta" → θ
- "alpha" → α
- "beta" → β
- "greater than or equal to" → ≥
- "less than" → <
- "infinity" → ∞
- "fraction a over b" → a/b
- "log base 2 of x" → log₂(x)
- "absolute value of x" → |x|

Return a JSON object with exactly these fields:
{
    "text": "The transcribed math problem with proper notation",
    "confidence": 1-10 (transcription accuracy confidence),
    "transcription_notes": "any unclear parts or uncertainties"
}

Rules:
- Convert all spoken math phrases to proper mathematical notation
- If something is unclear, note it and provide your best guess
- Rate confidence honestly
- Return ONLY the JSON object"""

        try:
            audio_part = {
                "mime_type": mime_type,
                "data": base64.b64encode(audio_bytes).decode("utf-8")
            }
            
            response = self.model.generate_content([prompt, audio_part])
            result = self._clean_json_output(response.text)
            return result
            
        except Exception as e:
            return {
                "text": "",
                "confidence": 1,
                "transcription_notes": f"Transcription failed: {str(e)}"
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
                "transcription_notes": "Could not parse structured ASR output"
            }
