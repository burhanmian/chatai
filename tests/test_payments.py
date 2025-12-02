import pytest
from app.payments.jazzcash import JazzCashClient
from app.payments.easypaisa import EasypaisaClient
from app.payments.bills import BillPaymentService


def test_jazzcash_client_init():
    """Test JazzCash client initialization"""
    client = JazzCashClient(
        merchant_id="test_merchant",
        password="test_pass",
        integrity_salt="test_salt",
        return_url="https://test.com/return"
    )
    assert client.merchant_id == "test_merchant"


def test_jazzcash_hash_generation():
    """Test JazzCash hash generation"""
    client = JazzCashClient(
        merchant_id="test",
        password="test",
        integrity_salt="test",
        return_url="https://test.com"
    )
    
    data = {"key1": "value1", "key2": "value2"}
    hash_value = client.generate_hash(data)
    
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64  # SHA256 produces 64 character hex


def test_easypaisa_client_init():
    """Test Easypaisa client initialization"""
    client = EasypaisaClient(
        store_id="test_store",
        password="test_pass",
        merchant_id="test_merchant"
    )
    assert client.store_id == "test_store"


@pytest.mark.asyncio
async def test_bill_service():
    """Test bill payment service"""
    service = BillPaymentService()
    
    result = await service.create_kelectric_payment(
        consumer_number="12345",
        amount=1000.0,
        mobile_number="+923001234567"
    )
    
    assert result["provider"] == "K-Electric"
    assert result["amount"] == 1000.0
