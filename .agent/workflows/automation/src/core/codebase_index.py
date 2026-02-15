"""
Codebase Indexer for Semantic RAG
Extends KnowledgeBase to index actual project code.
"""
import os
from pathlib import Path
from .knowledge_base import KnowledgeBase
from .config import PROJECT_ROOT

class CodebaseIndex(KnowledgeBase):
    """Manages semantic indexing of the actual project code"""
    
    def __init__(self):
        super().__init__()
        self.storage_path = PROJECT_ROOT / ".agent" / "automation" / "codebase_index.json"
        self.store.storage_path = self.storage_path
        self.store.load() # Re-load if exists
        
        # Paths to ignore to keep index clean and small
        self.ignore_dirs = {
            '.git', '.vols', 'node_modules', '.venv', '__pycache__', 
            'dist', 'build', '.pio', 'artifak', '.agent/automation'
        }
        self.allowed_extensions = {'.py', '.js', '.vue', '.cpp', '.h', '.ts', '.html', '.css', '.md'}

    def index_project(self, force: bool = False):
        """Index all relevant code files in the project"""
        if self.store.data and not force:
            return

        print(f"Indexing project code from {PROJECT_ROOT}...")
        # Note: We keep standards in the store too, or clear if we want fresh code-only index
        # For simplicity, let's just clear for now so it's a dedicated code index
        self.store.clear()
        
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                path = Path(root) / file
                if path.suffix in self.allowed_extensions:
                    self._index_code_file(path)
        
        self.store.save()
        print(f"✓ Indexed {len(self.store.data)} code chunks.")

    def _index_code_file(self, file_path: Path):
        """Index a code file by splitting into manageable chunks"""
        try:
            content = file_path.read_text(errors='ignore')
            rel_path = file_path.relative_to(PROJECT_ROOT)
            
            # Simple chunking by lines (approx 100-200 lines or logical blocks)
            lines = content.splitlines()
            chunk_size = 50 # Smaller chunks for code precision
            
            for i in range(0, len(lines), chunk_size):
                chunk_lines = lines[i:i + chunk_size + 10] # 10 lines overlap
                chunk_text = "\n".join(chunk_lines)
                
                if len(chunk_text.strip()) > 50:
                    self.store.add_text(
                        text=f"File: {rel_path}\n---\n{chunk_text}",
                        metadata={"source": str(rel_path), "type": "code", "start_line": i+1}
                    )
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def query_code(self, query: str, top_k: int = 3) -> str:
        """Find relevant code snippets for the current task"""
        if not self.store.data:
            self.index_project()
            
        results = self.store.search(query, top_k=top_k)
        
        if not results:
            return ""
            
        formatted = []
        for res in results:
            src = res['metadata'].get('source', 'unknown')
            line = res['metadata'].get('start_line', 1)
            formatted.append(f"--- SNIPPET FROM {src} (Line {line}) ---\n{res['text']}")
            
        return "\n\n".join(formatted)
