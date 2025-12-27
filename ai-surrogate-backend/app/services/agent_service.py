"""
AI Agent with Personality

CrewAI-based chat agent with Mistral AI integration.
"""

from crewai import Agent, Task, Crew
from langchain_mistralai import ChatMistralAI
from typing import Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)


# Initialize Mistral LLM for CrewAI
def get_mistral_llm():
    """Get Mistral LLM instance for CrewAI agents."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not found in environment")
    
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=api_key,
        temperature=0.7,
        max_tokens=1000
    )


class ChatAgent:
    """
    AI Chat Agent with personality and role-based behavior.
    
    Uses CrewAI framework with Mistral AI.
    """
    
    def __init__(
        self,
        personality: str = "friendly",
        expertise: str = "general assistant",
        goal: str = "Help users with their questions and tasks"
    ):
        """
        Initialize chat agent with personality.
        
        Args:
            personality: Personality type (friendly, professional, casual, enthusiastic)
            expertise: Area of expertise
            goal: Agent's primary goal
        """
        self.personality = personality
        self.expertise = expertise
        self.goal = goal
        
        # Get Mistral LLM
        self.llm = get_mistral_llm()
        
        # Define personality traits
        self.personality_traits = {
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
            }
        }
        
        # Create CrewAI agent with Mistral
        self.agent = self._create_agent()
        logger.info(f"✅ Chat agent created with {personality} personality using Mistral AI")
    
    def _create_agent(self) -> Agent:
        """Create CrewAI agent with personality."""
        traits = self.personality_traits.get(
            self.personality,
            self.personality_traits["friendly"]
        )
        
        backstory = (
            f"You are a {traits['tone']} AI assistant specializing in {self.expertise}. "
            f"Your communication style is {traits['style']}. "
            f"You always strive to be helpful, accurate, and engaging."
        )
        
        return Agent(
            role=f"{self.personality.capitalize()} AI Assistant",
            goal=self.goal,
            backstory=backstory,
            llm=self.llm,  # Use Mistral AI
            verbose=False,
            allow_delegation=False
        )
    
    def get_system_prompt(self, memory_context: str = "") -> str:
        """
        Generate system prompt with personality and memory.
        
        Args:
            memory_context: Context from past conversations
            
        Returns:
            System prompt string
        """
        traits = self.personality_traits.get(
            self.personality,
            self.personality_traits["friendly"]
        )
        
        prompt = (
            f"You are a {traits['tone']} AI assistant. "
            f"Your communication style is {traits['style']}. "
            f"You specialize in {self.expertise}. "
            f"{self.goal}."
        )
        
        if memory_context:
            prompt += f"\n\n{memory_context}"
        
        return prompt
    
    def create_task(self, user_message: str, context: str = "") -> Task:
        """
        Create a CrewAI task for the agent.
        
        Args:
            user_message: User's message
            context: Additional context
            
        Returns:
            CrewAI Task
        """
        description = f"Respond to the user's message: {user_message}"
        if context:
            description += f"\n\nContext: {context}"
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="A helpful, engaging response to the user's message"
        )
    
    def execute_task(self, user_message: str, context: str = "") -> str:
        """
        Execute a task using the agent.
        
        Args:
            user_message: User's message
            context: Additional context
            
        Returns:
            Agent's response
        """
        try:
            task = self.create_task(user_message, context)
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=False
            )
            
            result = crew.kickoff()
            return str(result)
        
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            return f"I apologize, but I encountered an error. Could you please rephrase your question?"


# Predefined agent personalities
AGENT_PERSONALITIES = {
    "default": ChatAgent(personality="friendly"),
    "professional": ChatAgent(personality="professional", expertise="business and productivity"),
    "casual": ChatAgent(personality="casual", expertise="general chat"),
    "enthusiastic": ChatAgent(personality="enthusiastic", expertise="motivation and support"),
    "technical": ChatAgent(personality="professional", expertise="programming and technology"),
}


def get_agent(personality: str = "default") -> ChatAgent:
    """Get a chat agent with specified personality."""
    return AGENT_PERSONALITIES.get(personality, AGENT_PERSONALITIES["default"])
