from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PaymentAgent:
    """Payment processing agent for JazzCash and Easypaisa"""
    
    def __init__(self, jazzcash_client=None, easypaisa_client=None):
        self.jazzcash = jazzcash_client
        self.easypaisa = easypaisa_client
    
    async def process_payment_request(
        self,
        provider: str,
        amount: float,
        mobile_number: str,
        description: str = "Payment"
    ) -> Dict[str, Any]:
        """
        Process payment request
        
        Args:
            provider: Payment provider (jazzcash or easypaisa)
            amount: Payment amount
            mobile_number: Customer mobile number
            description: Payment description
            
        Returns:
            Payment link and details
        """
        try:
            logger.info(f"Processing {provider} payment request for {mobile_number}")
            
            if provider.lower() == "jazzcash" and self.jazzcash:
                result = await self.jazzcash.create_payment_link(
                    amount=amount,
                    mobile_number=mobile_number,
                    description=description
                )
                
                return {
                    "success": True,
                    "provider": "JazzCash",
                    "payment_url": result["payment_url"],
                    "transaction_id": result["transaction_id"],
                    "amount": amount,
                    "message": f"JazzCash payment link tayyar hai. Amount: Rs. {amount}"
                }
            
            elif provider.lower() == "easypaisa" and self.easypaisa:
                result = await self.easypaisa.create_payment_link(
                    amount=amount,
                    mobile_number=mobile_number,
                    description=description
                )
                
                return {
                    "success": True,
                    "provider": "Easypaisa",
                    "payment_url": result["payment_url"],
                    "order_id": result["order_id"],
                    "amount": amount,
                    "message": f"Easypaisa payment link tayyar hai. Amount: Rs. {amount}"
                }
            
            return {
                "success": False,
                "message": f"{provider} abhi available nahi hai. Kya aap dusra option try karna chahenge?"
            }
            
        except Exception as e:
            logger.error(f"Failed to process payment: {str(e)}")
            return {
                "success": False,
                "message": "Payment process karne mein masla ho gaya. Kya aap dobara try kar sakte hain?"
            }
    
    async def check_payment_status(
        self,
        provider: str,
        transaction_id: str
    ) -> Dict[str, Any]:
        """
        Check payment status
        
        Args:
            provider: Payment provider
            transaction_id: Transaction/order ID
            
        Returns:
            Payment status
        """
        try:
            logger.info(f"Checking {provider} payment status: {transaction_id}")
            
            if provider.lower() == "jazzcash" and self.jazzcash:
                result = await self.jazzcash.check_payment_status(transaction_id)
                return {
                    "success": True,
                    "status": result.get("status", "unknown"),
                    "message": "Payment ki status check kar li hai."
                }
            
            elif provider.lower() == "easypaisa" and self.easypaisa:
                result = await self.easypaisa.check_payment_status(transaction_id)
                return {
                    "success": True,
                    "status": result.get("status", "unknown"),
                    "message": "Payment ki status check kar li hai."
                }
            
            return {
                "success": False,
                "message": "Payment status check nahi ho saka."
            }
            
        except Exception as e:
            logger.error(f"Failed to check payment status: {str(e)}")
            return {
                "success": False,
                "message": "Status check karne mein masla ho gaya."
            }
    
    async def get_payment_options(self) -> Dict[str, Any]:
        """
        Get available payment options
        
        Returns:
            List of payment options
        """
        options = []
        
        if self.jazzcash:
            options.append({
                "provider": "JazzCash",
                "available": True,
                "description": "Mobile wallet payment"
            })
        
        if self.easypaisa:
            options.append({
                "provider": "Easypaisa",
                "available": True,
                "description": "Mobile wallet payment"
            })
        
        return {
            "success": True,
            "options": options,
            "message": "Yeh payment options available hain:"
        }
