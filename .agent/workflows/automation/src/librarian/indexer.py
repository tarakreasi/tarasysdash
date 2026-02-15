# .agent/workflows/automation/src/librarian/indexer.py
"""
Librarian Indexer - Smart Whitelist-Based Indexing

RULES:
1. Only index directories that are project-relevant
2. Never index internal machinery (.venv, __pycache__, etc.)
3. Focus on: project code, documentation, workflows, specs
"""
import os
import hashlib
from pathlib import Path
from typing import List, Set
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ============================================================================
# INDEXING CONFIGURATION
# ============================================================================

# Directories to index (relative to project root)
# Use '*' as first element to enable whitelist mode
WHITELIST_DIRS = [
    "src",                      # Main source code (if exists)
    "internal",                 # Go internal packages
    "cmd",                      # Go commands
    "web",                      # Frontend code
    "docs",                     # Documentation
    ".agent/workflows/*.md",    # Workflow definitions (only .md files)
    ".agent/*.md",              # Agent documentation
    "taraSysDash/internal",     # TaraSysDash source
    "taraSysDash/cmd",          # TaraSysDash commands
    "taraSysDash/web/src",      # TaraSysDash frontend
    "taraSysDash/docs",         # TaraSysDash docs
]

# Always exclude these (even if inside whitelisted dirs)
BLACKLIST_DIRS = [
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    ".next",
    "coverage",
    "artifacts",
    "artifak",
    # Automation internals - don't index the indexer!
    ".agent/workflows/automation/.venv",
    ".agent/workflows/automation/memory",
    ".agent/workflows/automation/future",
    ".agent/workflows/automation/sprints_archive",
]

# File extensions to index
ALLOWED_EXTENSIONS = ['.py', '.md', '.txt', '.go', '.vue', '.ts', '.js', '.json', '.yaml', '.yml', '.sql']

# Max file size to index (skip large files)
MAX_FILE_SIZE_KB = 100  # 100 KB

class LibrarianIndexer:
    def __init__(self, db_manager, embedding_service):
        self.db = db_manager.db
        self.embedder = embedding_service
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self._indexed_count = 0
        self._skipped_count = 0

    def _is_blacklisted(self, path: Path) -> bool:
        """Check if path is in blacklist"""
        path_str = str(path)
        for blacklist in BLACKLIST_DIRS:
            if blacklist in path_str:
                return True
        return False
    
    def _is_allowed_extension(self, path: Path) -> bool:
        """Check if file extension is allowed"""
        return path.suffix.lower() in ALLOWED_EXTENSIONS
    
    def _is_too_large(self, path: Path) -> bool:
        """Check if file is too large"""
        try:
            size_kb = path.stat().st_size / 1024
            return size_kb > MAX_FILE_SIZE_KB
        except:
            return True

    def scan_and_index(self, root_path: str):
        """Smart scan with whitelist-first approach"""
        root = Path(root_path)
        if not root.exists():
            print(f"Root path not found: {root}")
            return

        print(f"Librarian: Indexing {root_path}...")
        print(f"📋 Whitelist: {len(WHITELIST_DIRS)} patterns")
        print(f"🚫 Blacklist: {len(BLACKLIST_DIRS)} patterns")
        
        # Walk through all files
        for path in root.rglob("*"):
            if not path.is_file():
                continue
                
            # Skip blacklisted
            if self._is_blacklisted(path):
                self._skipped_count += 1
                continue
                
            # Skip wrong extensions
            if not self._is_allowed_extension(path):
                self._skipped_count += 1
                continue
                
            # Skip large files
            if self._is_too_large(path):
                self._skipped_count += 1
                continue
            
            # Index the file
            self.index_file(str(path))
        
        print(f"\n✅ Indexing Complete!")
        print(f"   📚 Indexed: {self._indexed_count} files")
        print(f"   ⏭️  Skipped: {self._skipped_count} files")

    def index_file(self, file_path: str):
        """Index a single file with smart chunking"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return  # Skip binary or unreadable

        # Check existing
        current_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Simple upsert logic
        files = self.db["files"]
        existing = list(files.rows_where("path = ?", [file_path]))
        
        if existing:
            if existing[0]["hash"] == current_hash:
                return  # Unchanged
            # Update file record
            files.update(existing[0]["id"], {"hash": current_hash, "last_modified": 0.0})
            file_id = existing[0]["id"]
            # Delete old chunks
            self.db["chunks"].delete_where("file_id = ?", [file_id])
        else:
            files.insert({"path": file_path, "hash": current_hash, "last_modified": 0.0})
            file_id = list(files.rows_where("path = ?", [file_path]))[0]["id"]

        # Chunk and Embed
        chunks = self.splitter.split_text(content)
        for i, chunk_text in enumerate(chunks):
            if not chunk_text.strip():
                continue
            
            vector = self.embedder.get_embedding(chunk_text)
            
            self.db["chunks"].insert({
                "file_id": file_id,
                "chunk_index": i,
                "content": chunk_text,
                "embedding": vector,
                "metadata": "{}"
            })
        
        self._indexed_count += 1
        print(f"Indexed: {file_path}")