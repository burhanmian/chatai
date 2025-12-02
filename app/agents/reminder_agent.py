from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ReminderAgent:
    """Proactive reminder agent with notifications"""
    
    def __init__(self):
        self.reminders = []
    
    async def set_reminder(
        self,
        user_id: int,
        message: str,
        remind_at: datetime,
        phone_number: str
    ) -> Dict[str, Any]:
        """
        Set a reminder for user
        
        Args:
            user_id: User ID
            message: Reminder message
            remind_at: When to send reminder
            phone_number: User's phone number for notification
            
        Returns:
            Reminder details
        """
        try:
            logger.info(f"Setting reminder for user {user_id}: {message}")
            
            reminder = {
                "user_id": user_id,
                "message": message,
                "remind_at": remind_at,
                "phone_number": phone_number,
                "status": "active"
            }
            
            # In production, store in database and use Celery for scheduled tasks
            self.reminders.append(reminder)
            
            time_str = remind_at.strftime("%d %B %Y, %I:%M %p")
            return {
                "success": True,
                "reminder": reminder,
                "message": f"Theek hai! Main aap ko {time_str} par yaad dila dunga: {message}"
            }
        except Exception as e:
            logger.error(f"Failed to set reminder: {str(e)}")
            return {
                "success": False,
                "message": "Reminder set karne mein masla ho gaya."
            }
    
    async def get_active_reminders(self, user_id: int) -> Dict[str, Any]:
        """
        Get all active reminders for user
        
        Args:
            user_id: User ID
            
        Returns:
            List of active reminders
        """
        try:
            logger.info(f"Getting active reminders for user {user_id}")
            
            user_reminders = [r for r in self.reminders if r["user_id"] == user_id and r["status"] == "active"]
            
            if not user_reminders:
                return {
                    "success": True,
                    "reminders": [],
                    "count": 0,
                    "message": "Aap ka koi active reminder nahi hai."
                }
            
            return {
                "success": True,
                "reminders": user_reminders,
                "count": len(user_reminders),
                "message": f"Aap ke {len(user_reminders)} active reminders hain."
            }
        except Exception as e:
            logger.error(f"Failed to get reminders: {str(e)}")
            return {
                "success": False,
                "message": "Reminders get karne mein masla ho gaya."
            }
    
    async def cancel_reminder(self, user_id: int, reminder_index: int) -> Dict[str, Any]:
        """
        Cancel a reminder
        
        Args:
            user_id: User ID
            reminder_index: Index of reminder to cancel
            
        Returns:
            Cancellation status
        """
        try:
            logger.info(f"Cancelling reminder for user {user_id}")
            
            user_reminders = [r for r in self.reminders if r["user_id"] == user_id and r["status"] == "active"]
            
            if reminder_index < len(user_reminders):
                user_reminders[reminder_index]["status"] = "cancelled"
                return {
                    "success": True,
                    "message": "Reminder cancel ho gaya hai."
                }
            
            return {
                "success": False,
                "message": "Reminder nahi mila."
            }
        except Exception as e:
            logger.error(f"Failed to cancel reminder: {str(e)}")
            return {
                "success": False,
                "message": "Reminder cancel karne mein masla ho gaya."
            }
    
    async def send_reminder_notification(self, reminder: Dict[str, Any]) -> bool:
        """
        Send reminder notification to user
        
        Args:
            reminder: Reminder details
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Sending reminder notification: {reminder['message']}")
            
            # In production, integrate with WhatsApp client to send notification
            return True
        except Exception as e:
            logger.error(f"Failed to send reminder notification: {str(e)}")
            return False
