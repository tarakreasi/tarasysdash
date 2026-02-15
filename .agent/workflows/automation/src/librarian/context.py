# .agent/workflows/automation/src/librarian/context.py
from typing import List, Dict, Any

class ContextBuilder:
    def __init__(self):
        pass

    def format_context(self, results: List[Dict[str, Any]], max_tokens: int = 4096) -> str:
        context_parts = []
        current_tokens = 0
        
        # Header
        header = "Below are relevant code snippets from the codebase:\n\n"
        current_tokens += len(header) / 3.5
        context_parts.append(header)
        
        for res in results:
            path = res.get("path", "unknown")
            content = res.get("content", "")
            
            # Format:
            # <file path="path/to/file">
            # content
            # </file>
            
            entry = f'<file path="{path}">\n{content}\n</file>\n\n'
            entry_tokens = len(entry) / 3.5 # Rough approximation
            
            if current_tokens + entry_tokens > max_tokens:
                break
                
            context_parts.append(entry)
            current_tokens += entry_tokens
            
        return "".join(context_parts).strip()