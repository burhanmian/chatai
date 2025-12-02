from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Main orchestrator with GPT-4o for routing to specialized agents"""
    
    # Routing keywords for different agents
    EMAIL_KEYWORDS = ['email', 'mail', 'inbox', 'send']
    CALENDAR_KEYWORDS = ['calendar', 'schedule', 'appointment', 'meeting']
    REMINDER_KEYWORDS = ['remind', 'reminder', 'yaad', 'alert']
    PAYMENT_KEYWORDS = ['pay', 'payment', 'jazzcash', 'easypaisa', 'paisay']
    LOCAL_SERVICE_KEYWORDS = ['k-electric', 'bill', 'careem', 'foodpanda', 'daraz']
    
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key,
            temperature=0.7
        )
        
        self.system_prompt = """
You are DostAI, Pakistan's first proactive WhatsApp AI assistant with full audio support.

PERSONALITY:
- Warm, friendly, and culturally aware Pakistani assistant
- Speak naturally in Urdu, English, or Roman Urdu based on user preference
- Always greet with "Assalam-o-Alaikum" when appropriate
- Be helpful, proactive, and understanding of Pakistani context

CAPABILITIES:
- Email management (Gmail integration)
- Calendar scheduling (Google Calendar)
- Proactive reminders and notifications
- Payments via JazzCash and Easypaisa
- Utility bill payments (K-Electric, Sui Gas, WAPDA)
- Local service bookings (Careem, Foodpanda, Daraz)

LANGUAGE:
- Detect and respond in the same language as the user
- Support Urdu (اردو), English, and Roman Urdu
- Be culturally sensitive and use Pakistani expressions

ROUTING:
Analyze the user's request and route to appropriate specialized agent:
- email_agent: For email summaries, sending emails, checking inbox
- calendar_agent: For scheduling, appointments, calendar events
- reminder_agent: For setting reminders, notifications
- payment_agent: For JazzCash, Easypaisa payments, money transfers
- local_services: For K-Electric bills, Careem, Foodpanda, Daraz orders

For general conversations, respond directly without routing.
"""
    
    async def process_message(self, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user message and route to appropriate agent
        
        Args:
            user_message: User's message text
            user_context: Optional user context (language preference, history)
            
        Returns:
            Response with agent routing information
        """
        try:
            # Create prompt with system message and user message
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", "{message}")
            ])
            
            chain = prompt | self.llm
            
            # Get response from LLM
            response = await chain.ainvoke({"message": user_message})
            
            # Determine which agent to route to
            agent_routing = self._analyze_routing(user_message, response.content)
            
            return {
                "response": response.content,
                "route_to_agent": agent_routing["agent"],
                "agent_params": agent_routing["params"],
                "requires_action": agent_routing["requires_action"]
            }
        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")
            return {
                "response": "Maaf kijiye, mujhe kuch masla ho gaya. Kya aap dobara koshish kar sakte hain?",
                "route_to_agent": None,
                "agent_params": {},
                "requires_action": False
            }
    
    def _analyze_routing(self, user_message: str, ai_response: str) -> Dict[str, Any]:
        """Analyze message to determine agent routing"""
        message_lower = user_message.lower()
        
        # Email-related keywords
        if any(word in message_lower for word in self.EMAIL_KEYWORDS):
            return {
                "agent": "email_agent",
                "params": {"action": "check_inbox"},
                "requires_action": True
            }
        
        # Calendar-related keywords
        if any(word in message_lower for word in self.CALENDAR_KEYWORDS):
            return {
                "agent": "calendar_agent",
                "params": {"action": "check_events"},
                "requires_action": True
            }
        
        # Reminder-related keywords
        if any(word in message_lower for word in self.REMINDER_KEYWORDS):
            return {
                "agent": "reminder_agent",
                "params": {"action": "set_reminder"},
                "requires_action": True
            }
        
        # Payment-related keywords
        if any(word in message_lower for word in self.PAYMENT_KEYWORDS):
            return {
                "agent": "payment_agent",
                "params": {"action": "process_payment"},
                "requires_action": True
            }
        
        # Local services keywords
        if any(word in message_lower for word in self.LOCAL_SERVICE_KEYWORDS):
            return {
                "agent": "local_services",
                "params": {"action": "handle_service"},
                "requires_action": True
            }
        
        # No specific agent routing needed
        return {
            "agent": None,
            "params": {},
            "requires_action": False
        }
