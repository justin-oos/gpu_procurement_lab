from google.adk import Agent
from tools.api import LogisticsTools
from utils.config import config

# Initialize tools
api_tools = LogisticsTools()

LOGISTICS_SYSTEM_PROMPT = """
You are the Logistics Manager.
Your goal is to find real-time pricing and shipping estimates from the external market.
"""

logistics_agent = Agent(
    name="logistics_agent",
    model=config.MODEL_NAME,
    instruction=LOGISTICS_SYSTEM_PROMPT,
    tools=[api_tools.fetch_spot_prices, api_tools.estimate_shipping],
)
