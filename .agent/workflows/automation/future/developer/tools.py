# .agent/workflows/automation/src/developer/tools.py
import os
from typing import List, Dict, Any

# Import from Librarian we built in Sprint 4.2
# Ensure sys.path is handled in caller, or relative imports if package structure allows.
# We assume 'src' is in path.
from librarian.service import Librarian

class DeveloperTools:
    def __init__(self, librarian: Librarian):
        self.librarian = librarian

    def search_codebase(self, query: str) -> str:
        """
        Semantic search of the codebase.
        Use this to understand how existing code works or where things are defined.
        :param query: Natural language query (e.g., "how is the database initialized?")
        :return: Context strings with file paths.
        """
        return self.librarian.query(query, top_k=5)

    def read_file(self, file_path: str) -> str:
        """
        Read the exact content of a file.
        :param file_path: Absolute or relative path to the workspace root.
        :return: File content or error message.
        """
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, file_path: str, content: str) -> str:
        """
        Write content to a file. Overwrites existing content.
        Also creates parent directories if needed.
        :param file_path: Target path.
        :param content: Text content to write.
        :return: Success message.
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            # Re-index this file immediately so the Librarian knows about it?
            # For now, minimal.
            try:
                self.librarian.indexer.index_file(file_path)
            except:
                pass # Don't fail write if indexer fails
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"
    
    def list_dir(self, directory: str = ".") -> str:
        """
        List files in a directory.
        :return: List of filenames.
        """
        try:
            items = os.listdir(directory)
            return ", ".join(items)
        except Exception as e:
            return f"Error listing dir: {e}"