import hashlib
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class EasypaisaClient:
    """Easypaisa payment integration (Sandbox mode)"""
    
    def __init__(self, store_id: str, password: str, merchant_id: str):
        self.store_id = store_id
        self.password = password
        self.merchant_id = merchant_id
        self.base_url = "https://easypay-api.sandbox.com"  # Sandbox URL
    
    def generate_hash(self, data_string: str) -> str:
        """Generate secure hash for Easypaisa request"""
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    async def create_payment_link(
        self,
        amount: float,
        mobile_number: str,
        description: str = "Payment"
    ) -> Dict[str, Any]:
        """
        Create payment link for customer
        
        Args:
            amount: Payment amount in PKR
            mobile_number: Customer mobile number
            description: Payment description
            
        Returns:
            Payment link details
        """
        try:
            # Generate unique order ID
            order_id = f"EP{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
            
            # Prepare payment data
            payment_data = {
                'storeId': self.store_id,
                'orderId': order_id,
                'transactionAmount': str(amount),
                'transactionType': 'MA',  # Mobile Account
                'mobileAccountNo': mobile_number,
                'emailAddress': '',
                'orderRefNum': order_id,
                'tokenExpiry': '3600',  # 1 hour
                'description': description
            }
            
            # Generate hash
            hash_string = f"{self.store_id}{order_id}{amount}{mobile_number}{self.password}"
            payment_data['secureHash'] = self.generate_hash(hash_string)
            
            # Create payment URL
            payment_url = f"{self.base_url}/easypay/Index.jsf"
            
            logger.info(f"Created Easypaisa payment link for {mobile_number}: {order_id}")
            
            return {
                "payment_url": payment_url,
                "order_id": order_id,
                "amount": amount,
                "form_data": payment_data
            }
        except Exception as e:
            logger.error(f"Failed to create Easypaisa payment link: {str(e)}")
            raise
    
    async def check_payment_status(self, order_id: str) -> Dict[str, Any]:
        """
        Check payment transaction status
        
        Args:
            order_id: Order reference ID
            
        Returns:
            Payment status details
        """
        try:
            inquiry_data = {
                'storeId': self.store_id,
                'orderId': order_id,
                'merchantId': self.merchant_id
            }
            
            # Generate hash for inquiry
            hash_string = f"{self.store_id}{order_id}{self.password}"
            inquiry_data['secureHash'] = self.generate_hash(hash_string)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/easypay/api/inquire",
                    json=inquiry_data,
                    timeout=30.0
                )
                response.raise_for_status()
                
                return response.json()
        except Exception as e:
            logger.error(f"Failed to check Easypaisa payment status: {str(e)}")
            raise
    
    async def process_bill_payment(
        self,
        amount: float,
        mobile_number: str,
        consumer_number: str,
        bill_type: str = "UTILITY"
    ) -> Dict[str, Any]:
        """
        Process utility bill payment
        
        Args:
            amount: Bill amount in PKR
            mobile_number: Customer mobile number
            consumer_number: Consumer/reference number
            bill_type: Type of bill (UTILITY, TELECOM, etc.)
            
        Returns:
            Payment details
        """
        try:
            order_id = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
            
            payment_data = {
                'storeId': self.store_id,
                'orderId': order_id,
                'transactionAmount': str(amount),
                'transactionType': 'BillPayment',
                'mobileAccountNo': mobile_number,
                'consumerNumber': consumer_number,
                'billType': bill_type,
                'description': f'{bill_type} Bill Payment'
            }
            
            hash_string = f"{self.store_id}{order_id}{amount}{consumer_number}{self.password}"
            payment_data['secureHash'] = self.generate_hash(hash_string)
            
            logger.info(f"Processing {bill_type} bill payment: {order_id}")
            
            return {
                "order_id": order_id,
                "amount": amount,
                "consumer_number": consumer_number,
                "payment_data": payment_data
            }
        except Exception as e:
            logger.error(f"Failed to process bill payment: {str(e)}")
            raise
