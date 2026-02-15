# .agent/workflows/automation/src/librarian/retriever.py
import json
import struct
from typing import List, Dict, Any
import sqlite_vec

class LibrarianRetriever:
    def __init__(self, db_manager, embedding_service):
        self.db = db_manager.db
        self.embedder = embedding_service

    def query(self, user_query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # 1. Get query embedding
        query_vector = self.embedder.get_embedding(user_query)
        
        # Common pattern for sqlite-vec:
        
        sql = """
            SELECT 
                c.content,
                c.chunk_index,
                c.metadata,
                f.path,
                vec_distance_cosine(c.embedding, ?) as distance
            FROM chunks c
            JOIN files f ON c.file_id = f.id
            ORDER BY distance
            LIMIT ?
        """
        
        # We must serialise the vector to bytes/json string if the driver doesn't do it auto.
        # Often sqlite-vec expects a JSON string representation of the array for '?'
        import json
        vector_json = json.dumps(query_vector)
        
        results = []
        try:
            cursor = self.db.execute(sql, [vector_json, top_k])
            for row in cursor:
                    # Row is tuple: (content, chunk_index, metadata, path, distance)
                    results.append({
                        "content": row[0],
                        "path": row[3],
                        "score": row[4], 
                        "metadata": row[2]
                    })
        except Exception as e:
            print(f"Search error: {e}")
            import traceback
            traceback.print_exc()
            
        return results