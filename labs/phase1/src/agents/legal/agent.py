from google.adk import Agent
from tools.rag import LegalTools
from utils.config import config

# Initialize tools
rag_tools = LegalTools()

LEGAL_SYSTEM_PROMPT = """
You are the Legal Analyst Agent.
Your goal is to interpret vendor contracts to find allowable exceptions for procurement.

ENVIRONMENT CONTEXT:
- The Master Supply Agreement is stored in GCS as: 'Master_Supply_Agreement_NVIDIA.pdf'

CRITICAL RULES:
1. You NEVER read whole documents. You use 'analyze_contract_clause' to fetch specific sections.
2. You are looking for 'Exclusivity' clauses (restrictions) and 'Force Majeure' clauses (exceptions).
3. Interpret 'HOLD_LEGAL' status codes based on contract definitions.
"""

legal_agent = Agent(
    name="legal_agent",
    model=config.MODEL_NAME,
    instruction=LEGAL_SYSTEM_PROMPT,
    tools=[rag_tools.analyze_contract_clause],
)
