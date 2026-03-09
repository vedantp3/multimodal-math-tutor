"""Text input handler — Basic cleanup for direct text input."""


class TextHandler:
    """Handles direct text input with basic cleanup."""
    
    def process(self, raw_text: str) -> dict:
        """Process raw text input.
        
        Args:
            raw_text: User-typed text.
        
        Returns:
            dict with keys: text, confidence (always 10), notes
        """
        cleaned = raw_text.strip()
        
        if not cleaned:
            return {
                "text": "",
                "confidence": 1,
                "notes": "Empty input received."
            }
        
        return {
            "text": cleaned,
            "confidence": 10,
            "notes": "Direct text input — no extraction needed."
        }
