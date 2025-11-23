from google.adk import Agent
from tools.rag import LegalTools

# Initialize tools
rag_tools = LegalTools()

LEGAL_SYSTEM_PROMPT = """
You are the Legal Analyst Agent.
Your goal is to interpret vendor contracts to find allowable exceptions for procurement.

CRITICAL RULES:
1. You NEVER read whole documents. You use 'analyze_contract_clause' to fetch specific sections.
2. You are looking for 'Exclusivity' clauses (restrictions) and 'Force Majeure' clauses (exceptions).
3. Interpret 'HOLD_LEGAL' status codes based on contract definitions.
"""

legal_agent = Agent(
    name="legal_agent",
    model="gemini-3-pro-preview",  # Faster model for simple extraction
    instruction=LEGAL_SYSTEM_PROMPT,
    tools=[rag_tools.analyze_contract_clause],
)
