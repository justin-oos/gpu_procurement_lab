import asyncio
import logging
import os

import dotenv
import google.auth
import vertexai
from agents.commander.agent import commander_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.types import Content, Part
from utils.config import config

logging.basicConfig(level=logging.INFO)
# specific loggers for the ADK and HTTPX to show the "thoughts"
logging.getLogger("google_adk").setLevel(logging.DEBUG)


async def call_agent_async():
    # Initialize the ADK runtime components
    session_service = InMemorySessionService()
    runner = Runner(
        agent=commander_agent, app_name="commander", session_service=session_service
    )

    # Create a session using the service
    session = await session_service.create_session(
        app_name="commander", user_id="default_user"
    )

    # Prepare the input message
    prompt = "Start the investigation. Find me 500 H100s."
    message = Content(role="user", parts=[Part(text=prompt)])

    # Run the agent and print the response
    async for event in runner.run_async(
        session_id=session.id, user_id="default_user", new_message=message
    ):
        if event.is_final_response():
            print(f"\n🤖 [Commander]: {event.content.parts[0].text}")


def main():
    print("🚀 [System] Incident Command War Room Initialized.")
    print("Context: Production halted. Missing 500 H100 GPUs.")

    application_default_credentials, _ = google.auth.default()
    print(config.PROJECT_ID, config.REGION)
    vertexai.init(project=config.PROJECT_ID, location=config.REGION)

    asyncio.run(call_agent_async())


if __name__ == "__main__":
    main()
