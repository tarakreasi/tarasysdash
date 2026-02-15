# .agent/workflows/automation/src/developer/brain.py
import json
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = """You are an Autonomous Developer Agent.
You have access to the following tools:
- search_codebase(query): Search for code.
- read_file(file_path): Read file content.
- write_file(file_path, content): Write file content.
- list_dir(directory): List files.

You must reply with a strictly valid JSON object. Do not output markdown code blocks.
Format:
{
    "thought": "Reasoning about what to do next",
    "action": "tool_name_or_finish",
    "args": { ... arguments for tool ... }
}

Important argument names:
- Use 'file_path' not 'path' for read_file and write_file.
- Use 'directory' not 'path' for list_dir.

If you have completed the objective, set action to "finish".
"""

class AgentBrain:
    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        self.llm = ChatOllama(model=model_name, format="json", temperature=0)

    def decide_action(self, objective: str, tool_output_history: list) -> dict:
        # Construct history text
        history_text = ""
        for item in tool_output_history:
            history_text += f"\nAction: {item['action']}\nResult: {item['result']}\n"
        
        prompt = f"Objective: {objective}\n\nHistory of actions:\n{history_text}\n\nWhat is the next step?"
        
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content.strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback or error handling
            print(f"JSON Error from LLM: {content}")
            return {"thought": "Error parsing JSON", "action": "error", "args": {"raw": content}}