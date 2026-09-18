import re
from typing import List, Dict, Any, Optional

TELUGU_ENGLISH_MAP = {
    # Phonetic Telugu-English
    "poyindi": "lost",
    "poyina": "lost",
    "kolpoyanu": "lost",
    "cheyali": "procedure what to do",
    "em": "what",
    "ela": "how",
    "gurinchi": "about",
    "kavali": "required documents",
    "kavalo": "required",
    "amma": "mother",
    "nanna": "father",
    "teesukunnaru": "seized impounded",
    "seize": "seized impounded",
    "release": "release court order",
    "apdu": "apply",
    "dharakastu": "application",
    "kagithalu": "documents",
    "pathralu": "documents",
    "sakshya": "proof",
    "rupu": "form",
    
    # Native Telugu Script
    "ఆధార్": "aadhaar",
    "కార్డు": "card",
    "పోయింది": "lost",
    "చేయాలి": "procedure what to do",
    "ఏం": "what",
    "ఎలా": "how",
    "పెన్షన్": "pension",
    "పోలీస్": "police",
    "బండి": "bike vehicle",
    "లైసెన్స్": "driving licence",
    "డ్రైవింగ్": "driving",
    "పథకం": "scheme",
    "దరఖాస్తు": "application",
    "పత్రాలు": "documents"
}

QUERY_EXPANSIONS = {
    "aadhaar": ["lost aadhaar card", "download e-aadhaar", "aadhaar pvc card", "retrieve uid eid", "myaadhaar"],
    "pension": ["pension documents", "senior citizen pension", "widow pension", "disability certificate", "bdo dso office"],
    "police": ["police complaint", "fir procedure", "cognizable offence", "sho station house officer", "zero fir"],
    "vehicle": ["vehicle seizure", "impounded bike car", "section 207 mv act", "rto court release", "superdari application"],
    "pan": ["duplicate pan card", "lost pan card", "income tax nsdl", "form 49a", "utiitsl"],
    "driving_license": ["duplicate driving licence", "lost dl renewal", "parivahan sewa", "rto lld form"],
    "schemes": ["pm-kisan samman nidhi", "ayushman bharat pm-jay", "e-kyc verification", "welfare scheme eligibility"]
}

class QueryProcessor:
    """Processes user queries, detects Telugu/English, generates standalone follow-ups, and expands keywords."""

    @staticmethod
    def is_telugu_script(text: str) -> bool:
        """Detects if string contains Telugu unicode characters."""
        return bool(re.search(r'[\u0C00-\u0C7F]', text))

    @staticmethod
    def is_telugu_english_mixed(text: str) -> bool:
        """Detects Telugu-English phonetic keywords."""
        words = text.lower().split()
        return any(w in TELUGU_ENGLISH_MAP for w in words)

    @staticmethod
    def translate_telugu_to_english_concepts(query: str) -> str:
        """Translates Telugu & Telugu-English query into English search concepts for vector retrieval."""
        words = query.lower().split()
        translated_tokens = []
        for w in words:
            clean_w = re.sub(r'[^\w\u0C00-\u0C7F]', '', w)
            if clean_w in TELUGU_ENGLISH_MAP:
                translated_tokens.append(TELUGU_ENGLISH_MAP[clean_w])
            else:
                translated_tokens.append(w)
        return " ".join(translated_tokens)

    @staticmethod
    def extract_keywords(query: str) -> List[str]:
        """Extracts significant search terms and legal/procedural entities from query."""
        translated = QueryProcessor.translate_telugu_to_english_concepts(query)
        tokens = re.findall(r'\b[a-zA-Z0-9\-\.]+\b', translated.lower())
        stopwords = {
            "a", "an", "the", "is", "are", "was", "were", "what", "how", "where", 
            "when", "who", "which", "my", "your", "can", "i", "do", "to", "for", 
            "in", "on", "of", "and", "or", "should", "want", "need", "please", "help"
        }
        return [t for t in tokens if t not in stopwords and len(t) > 1]

    @staticmethod
    def generate_expansions(query: str, category: Optional[str] = None) -> List[str]:
        """Generates clean search query variations for retrieval without polluting intent."""
        translated_query = QueryProcessor.translate_telugu_to_english_concepts(query)
        variations = [query.strip(), translated_query.strip()]

        q_lower = query.lower()
        if any(kw in q_lower for kw in ["how", "what should", "procedure", "lost", "seized", "apply", "download"]):
            variations.append(f"{translated_query} required documents details proof")

        cleaned = []
        for v in variations:
            if v and v not in cleaned:
                cleaned.append(v)

        return cleaned[:3]
