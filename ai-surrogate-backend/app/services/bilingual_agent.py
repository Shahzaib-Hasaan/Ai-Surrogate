"""
Bilingual Agent using Agno

Generates responses in English or Urdu based on user's language.
Politely declines requests for other languages.
"""

from agno.agent import Agent


def create_bilingual_agent() -> Agent:
    """
    Creates an Agno agent that responds in English or Urdu only.
    
    Returns:
        Agent configured for bilingual responses
    """
    return Agent(
        name="Bilingual AI Assistant",
        model="mistral:mistral-large-latest",  # Agno format: provider:model_id
        instructions="""
        You are a helpful, friendly AI assistant that speaks ONLY English and Urdu.
        
        CRITICAL LANGUAGE RULES:
        1. If user writes in English → Respond in English
        2. If user writes in Urdu (proper Urdu, Roman Urdu, or Hindi) → Respond in proper Urdu script (اردو)
        3. If user requests any other language → Politely decline in both languages:
           "I only speak English and Urdu. میں صرف انگریزی اور اردو بولتا ہوں۔"
        
        RESPONSE QUALITY:
        - Be helpful, friendly, and conversational
        - Use markdown formatting when appropriate (bold, italic, code blocks, lists)
        - Maintain context from conversation history
        - Give clear, concise answers
        - Be engaging and personable
        
        IMPORTANT:
        - When responding in Urdu, use ONLY proper Urdu script (اردو)
        - Do NOT use Roman Urdu in your responses
        - Do NOT mix English and Urdu in the same response
        - Match the user's language choice
        """
    )


def generate_response(user_message: str, detected_language: str, conversation_context: str = "") -> str:
    """
    Generate a bilingual response based on detected language.
    
    Args:
        user_message: User's input message
        detected_language: Detected language ("English", "Urdu", or "Other")
        conversation_context: Optional conversation history for context
        
    Returns:
        AI response in appropriate language
    """
    agent = create_bilingual_agent()
    
    # Build context for the agent
    context_parts = []
    
    # Add language detection info
    if detected_language == "Other":
        context_parts.append("[User requested unsupported language - politely decline]")
    else:
        context_parts.append(f"[User language: {detected_language}]")
    
    # Add conversation history if available
    if conversation_context:
        context_parts.append(f"[Conversation context: {conversation_context}]")
    
    # Add user message
    context_parts.append(user_message)
    
    full_context = "\n".join(context_parts)
    
    # Generate response
    result = agent.run(full_context)
    
    # Extract content from RunOutput object
    response = result.content if hasattr(result, 'content') else str(result)
    
    return response
