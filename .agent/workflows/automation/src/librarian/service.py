# .agent/workflows/automation/src/librarian/service.py
import os
from .db_manager import DatabaseManager
from .embeddings import EmbeddingService
from .indexer import LibrarianIndexer
from .retriever import LibrarianRetriever
from .context import ContextBuilder

class Librarian:
    def __init__(self, workspace_root: str, db_path: str = None):
        self.root = workspace_root
        
        # Defaults
        if not db_path:
            # Use standard location relative to agent
            db_path = ".agent/workflows/automation/memory/librarian.db"
            
        self.db = DatabaseManager(db_path)
        self.embedder = EmbeddingService() # Defaults to nomic
        
        self.indexer = LibrarianIndexer(self.db, self.embedder)
        self.retriever = LibrarianRetriever(self.db, self.embedder)
        self.builder = ContextBuilder()
        
    def index(self):
        """Scan and index the workspace."""
        print(f"Librarian: Indexing {self.root}...")
        self.indexer.scan_and_index(self.root)
        
    def query(self, user_query: str, top_k: int = 10) -> str:
        """Retrieve relevant context for a query."""
        results = self.retriever.query(user_query, top_k=top_k)
        return self.builder.format_context(results)