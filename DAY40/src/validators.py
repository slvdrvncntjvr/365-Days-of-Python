from typing import Optional

def validate_input(text: str) -> Optional[str]:
    
    if not text:
        return "Input text cannot be empty"
    
    if len(text) > 2953:  
        return "Input text exceeds maximum length of 2953 characters sorry"
        
    return None