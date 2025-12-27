"""
AI Agent with Personality

Agno-based chat agent with Mistral integration.
"""

from agno.agent import Agent
from typing import Dict
import logging

from app.config import settings

logger = logging.getLogger(__name__)


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
    },
}

PERSONALITY_PROFILES: Dict[str, Dict[str, str]] = {
    "default": {"personality": "friendly", "expertise": "general assistant", "goal": "Help users with their questions and tasks"},
    "professional": {"personality": "professional", "expertise": "business and productivity", "goal": "Deliver precise, actionable guidance"},
    "casual": {"personality": "casual", "expertise": "general chat", "goal": "Keep conversations light and concise"},
    "enthusiastic": {"personality": "enthusiastic", "expertise": "motivation and support", "goal": "Encourage and energize users"},
    "technical": {"personality": "professional", "expertise": "programming and technology", "goal": "Provide accurate technical help"},
    "empathetic": {"personality": "empathetic", "expertise": "emotional support", "goal": "Offer supportive, compassionate responses"},
    "calming": {"personality": "calming", "expertise": "stress relief", "goal": "Help users stay calm and grounded"},
}

_agent_cache: Dict[str, "ChatAgent"] = {}


class ChatAgent:
    """AI Chat Agent with personality and role-based behavior."""

    def __init__(
        self,
        personality: str = "friendly",
        expertise: str = "general assistant",
        goal: str = "Help users with their questions and tasks",
        model_id: str = "",
    ):
        self.personality = personality
        self.expertise = expertise
        self.goal = goal
        self.model_id = model_id or settings.MISTRAL_CHAT_MODEL

        self.agent = self._create_agent()
        logger.info("Chat agent created with %s personality using Mistral via Agno", personality)

    def _create_agent(self) -> Agent:
        """Create Agno agent with configured Mistral model."""
        from agno.models.mistral import MistralChat

        mistral_api_key = settings.MISTRAL_API_KEY
        if not mistral_api_key:
            raise ValueError("MISTRAL_API_KEY is not set; cannot initialize ChatAgent")

        traits = PERSONALITY_TRAITS.get(self.personality, PERSONALITY_TRAITS["friendly"])

        system_prompt = (
            f"You are a {traits['tone']} AI assistant specializing in {self.expertise}. "
            f"Your communication style is {traits['style']}. "
            f"You always strive to be helpful, accurate, and engaging. "
            f"{self.goal}."
        )

        return Agent(
            name=f"{self.personality.capitalize()} Assistant",
            model=MistralChat(
                id=self.model_id,
                api_key=mistral_api_key,
            ),
            instructions=system_prompt,
            markdown=True,
            add_history_to_context=True,
        )

    def get_system_prompt(self, memory_context: str = "") -> str:
        traits = PERSONALITY_TRAITS.get(self.personality, PERSONALITY_TRAITS["friendly"])

        prompt = (
            f"You are a {traits['tone']} AI assistant. "
            f"Your communication style is {traits['style']}. "
            f"You specialize in {self.expertise}. "
            f"{self.goal}."
        )

        if memory_context:
            prompt += f"\n\n{memory_context}"

        return prompt

    def run(self, message: str) -> str:
        try:
            response = self.agent.run(message)
            return response.content if hasattr(response, "content") else str(response)
        except Exception as exc:  # keep the assistant running with a friendly fallback
            logger.error("Agent execution failed: %s", exc)
            return "I apologize, but I encountered an error. Could you please rephrase your question?"


def get_agent(personality: str = "default") -> ChatAgent:
    """Get or create a chat agent with the specified personality."""
    if personality not in PERSONALITY_PROFILES:
        personality = "default"

    if personality not in _agent_cache:
        config = PERSONALITY_PROFILES[personality]
        _agent_cache[personality] = ChatAgent(**config)

    return _agent_cache[personality]


def get_emotion_agent(emotion: str) -> ChatAgent:
    """Map detected emotion to an appropriate agent personality."""
    emotion_to_personality = {
        "happy": "enthusiastic",
        "excited": "enthusiastic",
        "sad": "empathetic",
        "anxious": "calming",
        "angry": "calming",
        "frustrated": "calming",
        "confused": "professional",
        "grateful": "friendly",
        "neutral": "default",
    }

    personality = emotion_to_personality.get(emotion, "default")
    return get_agent(personality)
