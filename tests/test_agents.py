import pytest
from app.agents.orchestrator import AgentOrchestrator
from app.agents.email_agent import EmailAgent
from app.agents.payment_agent import PaymentAgent


def test_orchestrator_init():
    """Test orchestrator initialization"""
    orchestrator = AgentOrchestrator(api_key="test_key")
    assert orchestrator.llm is not None


def test_orchestrator_routing():
    """Test message routing logic"""
    orchestrator = AgentOrchestrator(api_key="test_key")
    
    # Test email routing
    result = orchestrator._analyze_routing("check my email", "")
    assert result["agent"] == "email_agent"
    
    # Test payment routing
    result = orchestrator._analyze_routing("make a jazzcash payment", "")
    assert result["agent"] == "payment_agent"
    
    # Test calendar routing
    result = orchestrator._analyze_routing("schedule a meeting", "")
    assert result["agent"] == "calendar_agent"


@pytest.mark.asyncio
async def test_email_agent():
    """Test email agent"""
    agent = EmailAgent()
    
    result = await agent.check_inbox()
    assert "success" in result


@pytest.mark.asyncio
async def test_payment_agent():
    """Test payment agent"""
    agent = PaymentAgent()
    
    options = await agent.get_payment_options()
    assert "success" in options
