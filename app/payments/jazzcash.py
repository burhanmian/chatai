import hashlib
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class JazzCashClient:
    """JazzCash payment integration (Sandbox mode)"""
    
    def __init__(self, merchant_id: str, password: str, integrity_salt: str, return_url: str):
        self.merchant_id = merchant_id
        self.password = password
        self.integrity_salt = integrity_salt
        self.return_url = return_url
        self.base_url = "https://sandbox.jazzcash.com.pk"
    
    def generate_hash(self, data: Dict[str, str]) -> str:
        """Generate secure hash for JazzCash request"""
        sorted_values = [str(data[key]) for key in sorted(data.keys()) if key != 'pp_SecureHash']
        hash_string = self.integrity_salt + '&' + '&'.join(sorted_values)
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
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
            # Generate unique reference
            transaction_id = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
            
            # Prepare payment data
            payment_data = {
                'pp_Version': '1.1',
                'pp_TxnType': 'MWALLET',
                'pp_Language': 'EN',
                'pp_MerchantID': self.merchant_id,
                'pp_SubMerchantID': '',
                'pp_Password': self.password,
                'pp_TxnRefNo': transaction_id,
                'pp_Amount': str(int(amount * 100)),  # Convert to paisa
                'pp_TxnCurrency': 'PKR',
                'pp_TxnDateTime': datetime.now().strftime('%Y%m%d%H%M%S'),
                'pp_BillReference': transaction_id,
                'pp_Description': description,
                'pp_TxnExpiryDateTime': datetime.now().strftime('%Y%m%d%H%M%S'),
                'pp_ReturnURL': self.return_url,
                'pp_MobileNumber': mobile_number,
                'pp_CNIC': '',
                'ppmpf_1': '',
                'ppmpf_2': '',
                'ppmpf_3': '',
                'ppmpf_4': '',
                'ppmpf_5': ''
            }
            
            # Generate secure hash
            payment_data['pp_SecureHash'] = self.generate_hash(payment_data)
            
            # Create payment URL
            payment_url = f"{self.base_url}/CustomerPortal/transactionmanagement/merchantform"
            
            logger.info(f"Created JazzCash payment link for {mobile_number}: {transaction_id}")
            
            return {
                "payment_url": payment_url,
                "transaction_id": transaction_id,
                "amount": amount,
                "form_data": payment_data
            }
        except Exception as e:
            logger.error(f"Failed to create JazzCash payment link: {str(e)}")
            raise
    
    async def check_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Check payment transaction status
        
        Args:
            transaction_id: Transaction reference ID
            
        Returns:
            Payment status details
        """
        try:
            inquiry_data = {
                'pp_Version': '1.1',
                'pp_TxnType': 'INQUIRY',
                'pp_Language': 'EN',
                'pp_MerchantID': self.merchant_id,
                'pp_Password': self.password,
                'pp_TxnRefNo': transaction_id
            }
            
            inquiry_data['pp_SecureHash'] = self.generate_hash(inquiry_data)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/CustomerPortal/transactionmanagement/inquirytransaction",
                    data=inquiry_data,
                    timeout=30.0
                )
                response.raise_for_status()
                
                return response.json()
        except Exception as e:
            logger.error(f"Failed to check JazzCash payment status: {str(e)}")
            raise
