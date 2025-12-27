"""
AI Agent with Emotional Intelligence

Agno-based chat agent with emotion detection and empathetic responses.
"""

from agno.agent import Agent
from typing import Dict
import logging
import os

from app.config import settings

logger = logging.getLogger(__name__)


# Personality traits with emotional intelligence
PERSONALITY_TRAITS = {
    "friendly": {
        "tone": "warm and approachable",
        "style": "conversational with occasional emojis",
        "greeting": "Hey there! 😊",
    },
    "professional": {
        "tone": "formal and precise",
        "style": "structured and detailed",
        "greeting": "Hello, how may I assist you today?",
    },
    "casual": {
        "tone": "relaxed and informal",
        "style": "brief and to-the-point",
        "greeting": "Hey! What's up?",
    },
    "enthusiastic": {
        "tone": "energetic and positive",
        "style": "encouraging with lots of emojis",
        "greeting": "Hi! I'm so excited to help you! 🎉",
    },
    "empathetic": {
        "tone": "gentle and understanding",
        "style": "supportive and compassionate",
        "greeting": "Hello, I'm here for you. 💙",
    },
    "calming": {
        "tone": "soothing and reassuring",
        "style": "patient and de-escalating",
        "greeting": "Hi, let's take this one step at a time. 🌿",
    }
}


class ChatAgent:
    """
    AI Chat Agent with emotional intelligence.
    
    Detects user emotions and responds empathetically using system prompts.
    """
    
    def __init__(
        self,
        personality: str = "friendly",
        expertise: str = "general assistant",
        goal: str = "Help users with their questions and tasks"
    ):
        """
        Initialize emotionally intelligent chat agent.
        
        Args:
            personality: Personality type
            expertise: Area of expertise
            goal: Agent's primary goal
        """
        self.personality = personality
        self.expertise = expertise
        self.goal = goal
        self.personality_traits = PERSONALITY_TRAITS
        
        # Create Agno agent
        self.agent = self._create_agent()
        logger.info(f"✅ Emotionally intelligent agent created with {personality} personality")
    
    def _create_agent(self) -> Agent:
        """Create Agno agent with emotion-aware system prompt."""
        from agno.models.mistral import MistralChat
        from agno.db.sqlite import SqliteDb
        
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_api_key:
            raise ValueError("MISTRAL_API_KEY is not set")
        
        traits = self.personality_traits.get(
            self.personality,
            self.personality_traits["friendly"]
        )
        
        # Emotion-aware system prompt
        system_prompt = f"""
You are a {traits['tone']} AI assistant specializing in {self.expertise}.
Your communication style is {traits['style']}.
{self.goal}.

EMOTIONAL INTELLIGENCE:
You have the natural ability to detect and respond to user emotions.

Emotion Detection & Response Guide:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Happy/Excited 🎉✨
   - Tone: Enthusiastic, celebratory, energetic
   - Response: Match their excitement, celebrate with them
   - Example: "That's AMAZING! 🎉 I'm so happy for you! Tell me all about it!"

2. Sad/Down 💙🤗
   - Tone: Gentle, supportive, understanding
   - Response: Show empathy, offer comfort, be present
   - Example: "I'm sorry you're feeling down. I'm here for you. 💙 Would you like to talk about it?"

3. Angry/Frustrated 🌿
   - Tone: Calm, validating, de-escalating
   - Response: Acknowledge their feelings, stay patient, help problem-solve
   - Example: "I can hear your frustration, and that's completely valid. Let's work through this together. 🌿"

4. Anxious/Worried 🫂
   - Tone: Reassuring, patient, calming
   - Response: Provide reassurance, break things down, be steady
   - Example: "I understand this feels overwhelming. Let's take it one step at a time. You've got this. 🫂"

5. Confused 📚💡
   - Tone: Clear, structured, helpful
   - Response: Simplify, explain step-by-step, be patient
   - Example: "No worries! Let me break this down clearly for you. 📚"

6. Grateful ✨💖
   - Tone: Warm, reciprocating positivity
   - Response: Accept graciously, encourage continued growth
   - Example: "You're so welcome! It's my pleasure to help. ✨"

7. Excited/Enthusiastic 🚀⚡
   - Tone: High energy, matching enthusiasm
   - Response: Amplify their excitement, be encouraging
   - Example: "YES! That's the spirit! 🚀 Let's make this happen!"

8. Neutral 😊
   - Tone: Friendly, conversational, helpful
   - Response: Be warm and engaging
   - Example: "Happy to help! What can I do for you today? 😊"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Response Strategy:
1. Read the user's message carefully
2. Sense their emotional state from their words, tone, and context
3. Choose the appropriate emotional response style
4. Mirror appropriate empathy and adjust your tone
5. Provide emotional support when needed
6. Use emojis that fit the emotional context
7. Be authentic and genuine in your responses

CRITICAL INSTRUCTION - EMOTION TAG:
At the END of EVERY response, you MUST add a new line with:
EMOTION: [detected_emotion]

Where [detected_emotion] must be ONE of these EXACT words:
- happy
- excited
- sad
- angry
- frustrated
- anxious
- confused
- grateful
- neutral

Example:
"I can hear your frustration. Let's work through this. 🌿

EMOTION: frustrated"

Remember: Your goal is to make users feel heard, understood, and supported.
"""
        
        # Create agent with persistent memory
        return Agent(
            name=f"{self.personality.capitalize()} Assistant",
            model=MistralChat(
                id="mistral-small-latest",
                api_key=mistral_api_key,
            ),
            instructions=system_prompt,
            markdown=True,
            add_history_to_context=True,  # Built-in conversation memory
            db=SqliteDb(db_file="./agno_memory.db"),  # Persistent storage
        )
    
    def run(self, message: str) -> str:
        """
        Run agent with emotional intelligence.
        
        Args:
            message: User's message
            
        Returns:
            Empathetic AI response
        """
        try:
            response = self.agent.run(message)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return "I apologize, but I encountered an error. Could you please rephrase your question?"


# Predefined agent personalities
AGENT_PERSONALITIES = {
    "default": ChatAgent(personality="friendly"),
    "professional": ChatAgent(personality="professional", expertise="business and productivity"),
    "casual": ChatAgent(personality="casual", expertise="general chat"),
    "enthusiastic": ChatAgent(personality="enthusiastic", expertise="motivation and support"),
    "technical": ChatAgent(personality="professional", expertise="programming and technology"),
    "empathetic": ChatAgent(personality="empathetic", expertise="emotional support"),
    "calming": ChatAgent(personality="calming", expertise="stress relief"),
}


def get_agent(personality: str = "default") -> ChatAgent:
    """Get a chat agent with specified personality."""
    return AGENT_PERSONALITIES.get(personality, AGENT_PERSONALITIES["default"])
