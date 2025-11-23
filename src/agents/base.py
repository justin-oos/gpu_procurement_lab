import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from utils.config import config
from typing import List, Dict, Any


class BaseAgent:
    def __init__(
        self, model_name: str = "gemini-3-pro-preview", system_instruction: str = ""
    ):
        vertexai.init(project=config.PROJECT_ID, location=config.REGION)
        self.model = GenerativeModel(
            model_name, system_instruction=[system_instruction]
        )
        self.chat: ChatSession = self.model.start_chat()
        self.tools = {}

    def register_tool(self, name: str, func: callable):
        self.tools[name] = func

    def _execute_tool_call(self, tool_name: str, **kwargs) -> Any:
        if tool_name in self.tools:
            print(
                f"  [TOOL EXEC] {self.__class__.__name__} calling {tool_name} with {kwargs}"
            )
            return self.tools[tool_name](**kwargs)
        raise ValueError(f"Tool {tool_name} not found.")

    def generate_reply(self, prompt: str) -> str:
        # In a real ADK implementation, tool calling would be automatic.
        # Here we wrap the basic generation for the scaffold.
        response = self.chat.send_message(prompt)
        return response.text
