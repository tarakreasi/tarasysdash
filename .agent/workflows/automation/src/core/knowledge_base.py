"""
Knowledge Base Management for Agent Automation
Handles indexing and retrieval of code standards and project context.
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from .vector_store import SimpleVectorStore
from .config import AGENT_DIR

class KnowledgeBase:
    """Manages the semantic knowledge of the agent"""
    
    def __init__(self):
        storage_path = AGENT_DIR / "automation" / "knowledge_base.json"
        self.store = SimpleVectorStore(storage_path=str(storage_path))
        self.standards_dir = AGENT_DIR / "system" / "profiles" / "default" / "standards"
        
        # External knowledge sources (History, Sparring results, etc.)
        self.external_sources = [
            Path("/home/twantoro/.gemini/antigravity/knowledge"),
            Path("/home/twantoro/.gemini/antigravity/brain"),
            Path("/home/twantoro") # For .gemini/*.md root files
        ]

    def index_standards(self, force: bool = False):
        """Index all markdown files in the standards directory"""
        if not self.standards_dir.exists():
            print(f"⚠ Standards directory not found: {self.standards_dir}")
            return

        # Simple check: if already indexed and not forced, skip
        if self.store.data and not force:
            return

        print(f"Indexing standards from {self.standards_dir}...")
        self.store.clear()
        
        for root, _, files in os.walk(self.standards_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = Path(root) / file
                    self._index_file(file_path, base_dir=self.standards_dir, source_type="standard")
        
        # Index external sources
        print("Indexing external knowledge sources...")
        for source_path in self.external_sources:
            if not source_path.exists():
                continue
            
            # Special case for home root: only .gemini/*.md
            if source_path == Path("/home/twantoro"):
                gemini_root = source_path / ".gemini"
                if gemini_root.exists():
                    for f in gemini_root.glob("*.md"):
                        self._index_file(f, base_dir=gemini_root, source_type="history")
                continue

            for root, _, files in os.walk(source_path):
                for file in files:
                    # Only index markdown files, avoid huge binary/json files
                    if file.endswith(".md"):
                        file_path = Path(root) / file
                        # Skip if too deep or noise
                        if "node_modules" in str(file_path): continue
                        
                        self._index_file(file_path, base_dir=source_path, source_type="sparring_history")
        
        self.store.save()
        print(f"✓ Indexed {len(self.store.data)} chunks of knowledge (including external history).")

    def _index_file(self, file_path: Path, base_dir: Path, source_type: str = "standard"):
        """Index a single file by splitting into logical chunks (headers)"""
        try:
            content = file_path.read_text(errors='ignore')
            rel_path = file_path.relative_to(base_dir.parent if base_dir.parent != Path("/") else base_dir)
            
            # Split by markdown headers
            chunks = []
            current_chunk = []
            
            for line in content.splitlines():
                if line.startswith("#"):
                    if current_chunk:
                        chunks.append("\n".join(current_chunk))
                    current_chunk = [line]
                else:
                    current_chunk.append(line)
            
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                
            # Add to store
            for chunk in chunks:
                if len(chunk.strip()) > 30: # Higher threshold for history
                    self.store.add_text(
                        text=f"Source ({source_type}): {rel_path}\n---\n{chunk}",
                        metadata={"source": str(rel_path), "type": source_type}
                    )
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def query_standards(self, query: str, top_k: int = 3) -> str:
        """Query relevant standards for a given task"""
        if not self.store.data:
            self.index_standards()
            
        results = self.store.search(query, top_k=top_k)
        
        if not results:
            return ""
            
        formatted_results = []
        for res in results:
            src = res['metadata'].get('source', 'unknown')
            formatted_results.append(f"--- FROM {src} ---\n{res['text']}")
            
        return "\n\n".join(formatted_results)
