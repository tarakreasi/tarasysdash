import os
import re
import requests
import sys
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# --- CONFIGURATION & LOGGING ---
QWEN_API_URL = "http://10.42.1.10:8081/v1/chat/completions"
MODEL_NAME = "qwen2.5-coder-7b-instruct"

logging.basicConfig(
    filename='.agent/executor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- HELPER CLASSES ---

class CodeExtractor:
    """Smart Extraction Logic for AI Responses."""
    
    EXTENSION_MAP = {
        '.py': ['python', 'py'],
        '.js': ['javascript', 'js'],
        '.ts': ['typescript', 'ts'],
        '.vue': ['vue', 'html', 'javascript'],
        '.php': ['php'],
        '.go': ['go'],
        '.html': ['html'],
        '.css': ['css'],
        '.json': ['json'],
        '.md': ['markdown', 'md']
    }

    @staticmethod
    def extract(text: str, filename: str) -> str:
        """
        Extracts code from markdown text based on filename extension priorities.
        Strategy:
        1. Search for fenced blocks matching expected extension (e.g. ```vue).
        2. If multiple, take the longest.
        3. If none match extension, take the longest generic fenced block.
        4. Fallback: Strip fences if they wrap the entire content.
        """
        file_ext = Path(filename).suffix.lower()
        targets = CodeExtractor.EXTENSION_MAP.get(file_ext, [])
        
        # 1. Try Specific Languages
        candidates = []
        for lang in targets:
            pattern = f"```{lang}\n(.*?)```"
            matches = re.findall(pattern, text, re.DOTALL)
            candidates.extend(matches)
            
        if candidates:
            # Return the longest candidate (avoids grabbing small example blocks)
            return max(candidates, key=len).strip()

        # 2. Try Generic Blocks
        generic_matches = re.findall(r"```\w*\n(.*?)```", text, re.DOTALL)
        if generic_matches:
            # Sort by length descending
            return max(generic_matches, key=len).strip()
            
        # 3. Fallback: Raw Strip (if AI forgot language tag or just output code)
        if "```" in text:
            # Try to strip start/end fences
            cleaned = re.sub(r'^```\w*\n', '', text)
            cleaned = re.sub(r'\n```$', '', cleaned)
            return cleaned.strip()

        # 4. Raw text (assuming Qwen obeyed 'Output Only Code')
        return text.strip()

class SprintParser:
    """Parses Sprint Markdown into Structured Tasks."""
    
    @staticmethod
    def parse(content: str) -> Tuple[List[Dict[str, Any]], str]:
        tasks = []
        contract = ""
        
        try:
            # 1. Preamble Extraction
            if "### Task 1:" in content:
                preamble_parts = content.split("### Task 1:")
                contract = preamble_parts[0].strip()
            
            # 2. Task Extraction
            # Regex captures "### Task N:" until next task or simple end
            task_blocks = re.split(r'(?=### Task \d+:)', content)
            
            for block in task_blocks:
                if not block.strip().startswith("### Task"):
                    continue
                    
                # Extract components
                filename_match = re.search(r'\*\*File\*\*: `(.*?)`', block)
                if not filename_match: continue
                
                filename = filename_match.group(1).strip()
                
                # Check Type
                content_match = re.search(r'\*\*Content\*\*:\s*```[a-z]*\n(.*?)```', block, re.DOTALL)
                instruction_match = re.search(r'\*\*Instruction\*\*:(.*?)(?=\n\*\*|$)', block, re.DOTALL)
                
                if content_match:
                    tasks.append({
                        "type": "extract",
                        "filename": filename,
                        "content": content_match.group(1)
                    })
                elif instruction_match:
                    tasks.append({
                        "type": "generate",
                        "filename": filename,
                        "instruction": instruction_match.group(1).strip(),
                        "raw_block": block
                    })
        
        except Exception as e:
            logging.error(f"Parsing Error: {e}")
            print(f"❌ Parsing Error: {e}")
            
        return tasks, contract

class AIClient:
    """Handles communication with Qwen Server."""
    
    def __init__(self, debug_path: Path):
        self.debug_path = debug_path

    def generate(self, filename: str, system_prompt: str, user_prompt: str) -> Optional[str]:
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 8192,
            "temperature": 0.1, # Precision mode
            "stream": False
        }
        
        try:
            response = requests.post(QWEN_API_URL, json=data, timeout=180)
            if response.status_code == 200:
                raw_text = response.json()['choices'][0]['message']['content']
                self._log_debug(filename, raw_text)
                return CodeExtractor.extract(raw_text, filename)
            else:
                logging.error(f"API Error {response.status_code}: {response.text}")
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            logging.error(f"Request Exception: {e}")
            print(f"   ❌ Connection Error: {e}")
            
        return None

    def _log_debug(self, filename: str, content: str):
        with open(self.debug_path, "a") as f:
            f.write(f"\n--- AI RAW RETURN: {filename} ---\n")
            f.write(content[:1000] + "\n...(truncated)...\n" if len(content) > 1000 else content)
            f.write("\n-------------------------------\n")

# --- MAIN EXECUTOR ---

class SprintExecutor:
    def __init__(self, coding_rules: str = ""):
        self.coding_rules = coding_rules
        self.ai = AIClient(Path(".agent/debug_executor.log"))

    def execute(self, sprint_path: Path) -> bool:
        print(f"📖 Reading Sprint: {sprint_path.name}")
        content = sprint_path.read_text()
        
        tasks, contract = SprintParser.parse(content)
        
        print(f"📋 Found {len(tasks)} tasks.")
        if contract:
            print("📜 Contract found & injected.")
            
        success_count = 0
        for task in tasks:
            print(f"👉 Processing: {task['filename']} ({task['type']})")
            
            if self._handle_task(task, contract):
                success_count += 1
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed")
                
        return success_count == len(tasks)

    def _handle_task(self, task: Dict[str, Any], contract: str) -> bool:
        filename = task['filename']
        final_content = ""
        
        if task['type'] == 'extract':
            final_content = task['content']
        
        elif task['type'] == 'generate':
            # Construct Context
            full_context = f"""
BLUEPRINT / CONTRACT:
{contract}

---
TASK INSTRUCTION:
File: {filename}
Instruction: {task['instruction']}
"""
            # Construct System Prompt
            system_prompt = f"""You are Qwen 2.5 Coder, a Senior Software Architect.
GOAL: Write the file `{filename}` strictly following the Blueprint.

RULES:
1. Output ONLY the code content. No markdown fences if possible, but if used, use correct language tag.
2. NO conversational filler ("Here is the code...").
3. FOLLOW CONTRACT: Use exact variable names, interfaces, and logic from Blueprint.
4. {self.coding_rules}
"""
            final_content = self.ai.generate(filename, system_prompt, full_context)
            
        if final_content and len(final_content) > 10: # Sanity check
            self._write_file(filename, final_content)
            return True
            
        return False

    def _write_file(self, filename: str, content: str):
        path = Path(filename).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
