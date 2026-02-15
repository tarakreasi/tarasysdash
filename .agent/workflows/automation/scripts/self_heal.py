#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import json
import re

# CONFIG
QWEN_URL = "http://10.42.1.10:8081/v1/chat/completions"
MODEL = "qwen2.5-7b.gguf"
CONTRACT_PATH = "docs/specs/DOMAIN_CONTRACT.md"

def get_contract():
    if os.path.exists(CONTRACT_PATH):
        with open(CONTRACT_PATH, "r") as f:
            return f.read()
    return "No contract found."

def ask_qwen_to_fix(file_path, error_log, current_code):
    contract = get_contract()
    
    # Truncate error log to keep it relevant and avoid token limits
    truncated_log = error_log[-3000:] if len(error_log) > 3000 else error_log
    
    prompt = f"""You are a Senior Debugger. A test failed for the file `{file_path}`.
    
    DOMAIN CONTRACT (Source of Truth):
    {contract}
    
    ERROR LOG (Tail):
    {truncated_log}
    
    CURRENT CODE:
    {current_code}
    
    TASK:
    1. Analyze why it failed based on the log and the contract.
    2. Fix the code.
    3. Ensure field names match the CONTRACT exactly (e.g., use 'title' not 'description' if specified).
    4. Return ONLY the full corrected code. No explanations.
    """
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert coder. Return raw code only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    print(f"🧠 Qwen is analyzing the error and patching `{file_path}`...")
    try:
        response = requests.post(QWEN_URL, json=data, timeout=120)
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            # Cleanup markdown
            content = re.sub(r'^```[a-z]*\n', '', content)
            content = re.sub(r'\n```$', '', content)
            return content.strip()
    except Exception as e:
        print(f"❌ API Error: {e}")
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: self_heal.py [target_file] [test_command]")
        sys.exit(1)
        
    target_file = sys.argv[1]
    test_cmd = sys.argv[2:] # Everything after target_file
    
    print(f"🛡️ Starting Self-Healing for `{target_file}`...")
    
    max_iterations = 3
    for i in range(max_iterations):
        print(f"\n🔄 Iteration {i+1}/{max_iterations}")
        print(f"🧪 Running: {' '.join(test_cmd)}...")
        
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS! `{target_file}` passed verification.")
            sys.exit(0)
            
        print(f"❌ FAILED. Captured {len(result.stdout + result.stderr)} chars of error.")
        
        # Get current code
        with open(target_file, "r") as f:
            current_code = f.read()
            
        # Ask Qwen to fix
        fixed_code = ask_qwen_to_fix(target_file, result.stdout + result.stderr, current_code)
        
        if fixed_code:
            with open(target_file, "w") as f:
                f.write(fixed_code)
            print(f"📝 Applied patch to `{target_file}`.")
        else:
            print("❌ Qwen failed to provide a fix.")
            break
            
    print("\n🛑 Self-healing reached max iterations or failed.")
    sys.exit(1)

if __name__ == "__main__":
    main()
