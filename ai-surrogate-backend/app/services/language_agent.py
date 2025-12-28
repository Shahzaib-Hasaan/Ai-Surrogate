"""
Language Detection Agent using Agno

Detects user's language: English, Urdu (includes Roman Urdu and Hindi), or Other
"""

from agno.agent import Agent


def create_language_detector() -> Agent:
    """
    Creates an Agno agent for language detection.
    
    Returns:
        Agent configured to detect language from user message
    """
    return Agent(
        name="Language Detector",
        model="mistral:mistral-small-latest",  # Agno format: provider:model_id
        instructions="""
        You are a language detection expert.
        
        Detect the language of the user's message and return ONLY one of these:
        - English
        - Urdu (this includes proper Urdu script, Roman Urdu, and Hindi)
        - Other
        
        Rules:
        - If user writes in Urdu script (اردو), return "Urdu"
        - If user writes in Roman Urdu (e.g., "Kaise ho", "Shukriya"), return "Urdu"
        - If user writes in Hindi (Devanagari or Roman), return "Urdu"
        - If user writes in English, return "English"
        - For any other language, return "Other"
        - If user mixes languages, return the primary/dominant language
        
        Return ONLY the language name, nothing else. No explanation.
        """
    )


def detect_language(message: str) -> str:
    """
    Detect the language of a user message.
    
    Args:
        message: User's input message
        
    Returns:
        One of: "English", "Urdu", "Other"
    """
    agent = create_language_detector()
    result = agent.run(message)
    
    # Extract content from RunOutput object
    detected = result.content if hasattr(result, 'content') else str(result)
    detected = detected.strip()
    
    # Ensure valid response
    if detected not in ["English", "Urdu", "Other"]:
        # Default to English if detection fails
        return "English"
    
    return detected
