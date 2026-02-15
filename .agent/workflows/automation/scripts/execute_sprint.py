#!/usr/bin/env python3
"""
Sprint Executor (The "Worker Hand")
Parses a Sprint Markdown file and executes file creation tasks.
Supports two modes:
1. Direct Extraction: If code block exists in MD.
2. AI Generation: If code missing, asks Qwen (via API).
"""

import requests
import json
import os
import re
import argparse
import sys
from typing import List, Dict, Any

# CONFIGURATION
QWEN_API_URL = "http://10.42.1.10:8081/v1/chat/completions"
MODEL_NAME = "qwen2.5-7b.gguf"

# Load Coding Standards
STANDARDS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "rules", "CODING_STANDARDS.md")
CODING_RULES = ""
if os.path.exists(STANDARDS_PATH):
    with open(STANDARDS_PATH, "r") as f:
        CODING_RULES = f.read()

def generate_file_content(filename: str, task_context: str) -> str:
    """Ask Qwen to generate content for a SINGLE file."""
    
    # Tuned System Prompt
    system_prompt = f"""You are a Senior Software Engineer acting as a Code Generator.
    
    YOUR GOAL: Generate production-ready code file.
    
    STRICT CODING STANDARDS:
    {CODING_RULES}
    
    OUTPUT FORMAT:
    - Return ONLY the raw code.
    - No markdown blocks (if possible).
    - No conversational filler ("Here is the code").
    """
    
    user_prompt = f"""
    TASK: Generate content for file `{filename}`.
    
    CONTEXT / REQUIREMENTS:
    {task_context}
    
    Implement the full code now.
    """
    
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.1, # Precise mode
        "stream": False
    }
    
    print(f"🤖 AI Generating: {filename} (Applied Standards)...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"   ⚠️ Retry {attempt+1}/{max_retries}...")
            
            response = requests.post(QWEN_API_URL, json=data, timeout=120)
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Cleanup markdown artifacts
                content = re.sub(r'^```[a-z]*\n', '', content)
                content = re.sub(r'\n```$', '', content)
                content = content.strip()
                
                if not content:
                    print("   ❌ Error: Empty content received.")
                    continue
                    
                return content
            else:
                print(f"   ❌ API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
            
    print(f"❌ Failed after {max_retries} attempts.")
    return None

def parse_sprint_tasks(content: str) -> List[Dict[str, Any]]:
    """Parse Sprint MD for tasks."""
    tasks = []
    
    # Split by "### Task" headers
    sections = re.split(r'### Task \d+:', content)
    
    for section in sections[1:]: # Skip preamble
        # 1. Find Filename
        file_match = re.search(r'\*\*File\*\*: `(.*?)`', section)
        if not file_match:
            continue
        filename = file_match.group(1).strip()
        
        # 2. Check for Content Block
        content_match = re.search(r'\*\*Content\*\*:\s*```[a-z]*\n(.*?)```', section, re.DOTALL)
        
        if content_match:
            tasks.append({
                "type": "extract",
                "filename": filename,
                "content": content_match.group(1)
            })
        else:
            tasks.append({
                "type": "generate",
                "filename": filename,
                "context": section
            })
            
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Execute a Sprint Plan")
    parser.add_argument("sprint_file", help="Path to sprint markdown file")
    args = parser.parse_args()
    
    # Resolve path
    sprint_path = os.path.abspath(args.sprint_file)
    if not os.path.exists(sprint_path):
        print(f"❌ File not found: {sprint_path}")
        sys.exit(1)

    print(f"📖 Reading Sprint: {os.path.basename(sprint_path)}")
    with open(sprint_path, "r") as f:
        content = f.read()
    
    tasks = parse_sprint_tasks(content)
    print(f"📋 Found {len(tasks)} tasks.")
    
    if not tasks:
        print("⚠️ No tasks found. Check format (expects '### Task X:' and '**File**:').")
    
    success_count = 0
    
    for task in tasks:
        filename = task['filename']
        content = ""
        
        # Execute Strategy
        if task['type'] == 'extract':
            print(f"⚡ Extracting: {filename} (Fast)")
            content = task['content']
        else:
            print(f"🤔 Thinking: {filename} (Qwen GPU)")
            content = generate_file_content(filename, task['context'])
            
        # Write to Disk
        if content:
            # Safe write with dir creation
            filepath = os.path.abspath(filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, "w") as f:
                f.write(content)
            print(f"✅ Created: {filename}")
            success_count += 1
        else:
            print(f"❌ Failed: {filename}")

    print(f"\n✨ Execution Complete. {success_count}/{len(tasks)} files generated.")

if __name__ == "__main__":
    main()
