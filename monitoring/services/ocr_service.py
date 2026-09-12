import re
import pytesseract
from PIL import Image
from typing import List, Tuple

class OCRService:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            
    def extract_text(self, image_path: str) -> str:
        """Extracts all visible text from the screenshot."""
        try:
            image = Image.open(image_path)
            # Use basic config. Could be optimized for game screens later.
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def normalize_text(self, text: str) -> str:
        """Normalizes text by lowercasing and removing extra whitespace/newlines."""
        if not text:
            return ""
        # Lowercase
        normalized = text.lower()
        # Replace newlines with spaces
        normalized = normalized.replace('\n', ' ')
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        # Remove punctuation that might be misread by OCR (optional, but requested in prompt)
        normalized = re.sub(r'[^\w\s]', '', normalized)
        return normalized.strip()

    def compare_expected_text(self, actual_text: str, expected_text: str) -> bool:
        """Compares normalized OCR text with normalized expected text."""
        if not expected_text:
            return True # If nothing is expected, it passes
            
        normalized_actual = self.normalize_text(actual_text)
        normalized_expected = self.normalize_text(expected_text)
        
        return normalized_expected in normalized_actual

    def detect_error_text(self, actual_text: str, error_patterns: List[str]) -> Tuple[bool, str]:
        """Checks if any known error pattern exists in the extracted text."""
        normalized_actual = self.normalize_text(actual_text)
        
        for pattern in error_patterns:
            normalized_pattern = self.normalize_text(pattern)
            if normalized_pattern and normalized_pattern in normalized_actual:
                return True, pattern
                
        return False, ""
