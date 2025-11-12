import re
from typing import List, Dict, Tuple
from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import hashlib
import uuid


class RedactionService:
    def __init__(self):
        # Generate key from JWT secret (in production, use separate key)
        key = hashlib.sha256(settings.jwt_secret.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key))
        
        # PII patterns
        self.patterns = {
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        }

    def redact(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """
        Redact PII from text and return redacted text + vault tokens.
        Returns: (redacted_text, tokens_list)
        """
        if not settings.redaction_enabled:
            return text, []
        
        tokens = []
        redacted_text = text
        
        for kind, pattern in self.patterns.items():
            matches = pattern.finditer(text)
            for match in reversed(list(matches)):  # Reverse to preserve positions
                original = match.group()
                token = f"[REDACTED_{kind.upper()}_{uuid.uuid4().hex[:8]}]"
                
                # Encrypt original value
                encrypted = self.cipher.encrypt(original.encode()).decode()
                
                tokens.append({
                    "token": token,
                    "kind": kind,
                    "value_ciphertext": encrypted,
                })
                
                # Replace in text
                redacted_text = (
                    redacted_text[:match.start()] + token + redacted_text[match.end():]
                )
        
        return redacted_text, tokens

    def reveal(self, ciphertext: str) -> str:
        """Decrypt a redacted value"""
        try:
            decrypted = self.cipher.decrypt(ciphertext.encode())
            return decrypted.decode()
        except Exception:
            return "[DECRYPTION_FAILED]"


redaction_service = RedactionService()

