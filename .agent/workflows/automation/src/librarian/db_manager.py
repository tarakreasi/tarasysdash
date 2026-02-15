# .agent/workflows/automation/src/librarian/db_manager.py
import sqlite_utils
import sqlite_vec
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = ".agent/workflows/automation/memory/librarian.db"):
        self.db_path = Path(db_path)
        # Ensure parent directory exists
        if not self.db_path.parent.exists():
             self.db_path.parent.mkdir(parents=True, exist_ok=True)
             
        self.db = sqlite_utils.Database(str(self.db_path))
        self.db.conn.enable_load_extension(True)
        sqlite_vec.load(self.db.conn)
        self.db.conn.enable_load_extension(False)
        self._init_schema()
    
    def _init_schema(self):
        # Files table
        self.db["files"].create({
            "id": int,
            "path": str,
            "last_modified": float,
            "hash": str,
        }, pk="id", not_null={"path"}, if_not_exists=True)
        
        # Ensure unique constraint separately if needed or via transform, but simple create is fine for now
        self.db["files"].create_index(["path"], unique=True, if_not_exists=True)

        # Chunks table
        self.db["chunks"].create({
            "id": int,
            "file_id": int,
            "chunk_index": int,
            "content": str,
            "embedding": float, 
            "metadata": str,
        }, pk="id", foreign_keys=[("file_id", "files", "id")], if_not_exists=True)