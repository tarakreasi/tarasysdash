"""
JSON Structured Logger
Provides a standardized logging interface for the automation system.
"""
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class JSONLogger:
    def __init__(self, name: str, log_file: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.log_file = log_file
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Console Handler (Stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(console_handler)
        
        # File Handler (Optional)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(JSONFormatter())
            self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra={"data": kwargs})

    def error(self, message: str, **kwargs):
        self.logger.error(message, extra={"data": kwargs})

    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra={"data": kwargs})

    def success(self, message: str, **kwargs):
        # Map success to INFO but with a tag
        self.logger.info(message, extra={"data": {**kwargs, "status": "SUCCESS"}})

class JSONFormatter(logging.Formatter):
    """Format logs as JSON objects"""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        
        # Merge extra data if present
        if hasattr(record, "data"):
            log_data.update(record.data)
            
        return json.dumps(log_data)
