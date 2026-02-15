    # .agent/workflows/automation/verify_agent_full.py
    import sys
    import os
    
    # Add src
    sys.path.append(os.path.join(os.getcwd(), "src"))
    
    from developer.brain import AgentBrain
    
    # Check if we can connect to Ollama before running full test
    try:
        brain = AgentBrain()
        print("✅ Ollama connection check passed (Brain init success).")
        # We won't run a full loop here to avoid non-deterministic LLM output in verification.
        # But we verify the import structure works for the CLI.
    except Exception as e:
        print(f"⚠️ Ollama check warning: {e}")
        # Don't fail the build if Ollama isn't up, but note it.
    