import asyncio
import logging
import os

import dotenv
import google.auth
import vertexai
from agents.commander.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.types import Content, Part
from utils.config import config

# Configure Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("google_adk").setLevel(logging.DEBUG)
# Suppress noisy HTTP logs so you can see the agent's thought process clearly
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- CONFIGURATION ---
MAX_STEPS = 30  # Safety Brake: Stop after 15 iterations no matter what.


async def call_agent_async():
    # Initialize the ADK runtime components
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, app_name="commander", session_service=session_service
    )

    # Create a session using the service
    session = await session_service.create_session(
        app_name="commander", user_id="default_user"
    )

    # Prepare the input message
    prompt = "Start the investigation. Find me 500 H100s."
    message = Content(role="user", parts=[Part(text=prompt)])

    print(f"🛑 [System] Safety Limit set to {MAX_STEPS} steps.")
    step_count = 0

    # Run the agent and print the response
    async for event in runner.run_async(
        session_id=session.id, user_id="default_user", new_message=message
    ):
        step_count += 1
        
        # --- 1. THE SAFETY BRAKE ---
        if step_count > MAX_STEPS:
            print(f"\n❌ [System] TERMINATING: Hit max step limit ({MAX_STEPS}).")
            print("   Likely cause: Infinite loop due to recurring tool errors (404/Connection Refused).")
            break  # Force exit

        # --- 2. SUCCESS CONDITION ---
        if event.is_final_response():
            # Check if there is actual text content
            if event.content and event.content.parts:
                print(f"\n🤖 [Commander]: {event.content.parts[0].text}")
            else:
                print("\n🤖 [Commander]: (Returned final response with no text)")
            break 
            
        # --- 3. PROGRESS INDICATOR ---
        # If it's not final, the agent is thinking/calling tools
        print(f"   ⚙️ [System] Step {step_count}: Processing...")


def main():
    print("🚀 [System] Incident Command War Room Initialized.")
    print("Context: Production halted. Missing 500 H100 GPUs.")

    application_default_credentials, _ = google.auth.default()
    print(f"Project: {config.PROJECT_ID}, Region: {config.REGION}")
    vertexai.init(project=config.PROJECT_ID, location=config.REGION)

    asyncio.run(call_agent_async())


if __name__ == "__main__":
    main()