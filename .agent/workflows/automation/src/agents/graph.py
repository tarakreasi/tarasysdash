"""
LangGraph-based "Pod" Architecture for Autonomous Coding
Splits reasoning into: Architect -> Coder -> Verifier
"""
import os
import subprocess
import re
from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pathlib import Path

from .state import AgentState
from ..core.llm import get_llm
from ..core.config import MODEL_SMART, MODEL_FAST, OLLAMA_BASE_URL, PROJECT_ROOT

# --- 1. THE ARCHITECT NODE ---
def architect_node(state: AgentState):
    """
    Architect: Analyzes the task and creates a high-level technical strategy.
    Does NOT write code or commands. Focuses on 'HOW' and 'WHERE'.
    """
    task = state.get("task", "")
    context = state.get("context", "")
    
    # Use Smart Model for planning
    llm = get_llm(model=MODEL_SMART, temperature=0.3)
    
    system_prompt = f"""You are the Lead Architect.
TASK: {task}
CONTEXT:
{context}

Your job is to devise a TECHNICAL STRATEGY.
1. Identify which files need to be created or modified.
2. Outline the logic changes required.
3. Identify potential risks.

Output purely the execution plan in a clear, numbered list. 
DO NOT write code. DO NOT output bash commands.
Target Audience: A Senior DevOps/Coder who will execute your plan.
"""
    
    msg = HumanMessage(content="Please provide the technical strategy.")
    response = llm.invoke([SystemMessage(content=system_prompt), msg])
    
    return {
        "strategy": response.content,
        "messages": [response]
    }

# --- 2. THE CODER NODE ---
def coder_node(state: AgentState):
    """
    Coder: Takes the Architect's strategy and converts it into BASH/AIDER commands.
    Focuses on syntax and tool usage.
    """
    task = state.get("task", "")
    strategy = state.get("strategy", "")
    project_root = state.get("project_root", str(PROJECT_ROOT))
    
    # Use Smart Model for coding precision
    llm = get_llm(model=MODEL_SMART, temperature=0.2)
    
    system_prompt = f"""You are the Senior Coder.
You allow the Architect's strategy to guide you.
You operate in a Linux environment via BASH commands.

TASK: {task}
STRATEGY:
{strategy}

PROJECT ROOT: {project_root}

INSTRUCTIONS:
1. Translate the Strategy into BASH commands.
2. Use `aider` for ALL code modifications.
   ```bash
   export OLLAMA_API_BASE={OLLAMA_BASE_URL}
   /home/twantoro/.local/bin/aider --model ollama/{MODEL_SMART} --yes --message "Instruction" target_file
   ```
3. ALWAYS verify your work using `cat` or `grep`.
4. Output specific BASH commands in ```bash blocks.
5. If you have finished all steps in the strategy, output "MISSION COMPLETE".
"""

    messages = state.get("messages", [])
    # Filter only relevant history to save context (optional optimization)
    
    response = llm.invoke([SystemMessage(content=system_prompt)] + messages[-3:])
    
    return {
        "messages": [response]
    }

# --- 3. THE EXECUTOR NODE (System) ---
def execute_node(state: AgentState):
    """
    System Executor: Runs the bash commands output by the Coder.
    """
    messages = state.get("messages", [])
    project_root = state.get("project_root", str(PROJECT_ROOT))
    
    if not messages:
        return {}
        
    last_message = messages[-1]
    content = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    # Extract bash commands
    bash_pattern = r'```(?:bash|sh)?\n(.*?)```'
    matches = re.findall(bash_pattern, content, re.DOTALL)
    
    if not matches:
        return {"review_status": "pending"} # Let verifier decide or loop back
        
    outputs = []
    for cmd in matches:
        cmd = cmd.strip()
        if not cmd: continue
        
        print(f"\n⚡ [EXECUTOR] Running: {cmd[:60]}...")
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=project_root,
                capture_output=True, text=True, timeout=300
            )
            output = f"CMD: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}\nCode: {result.returncode}"
            outputs.append(output)
        except Exception as e:
            outputs.append(f"CMD: {cmd}\nERROR: {str(e)}")
            
    combined_output = "\n---\n".join(outputs)
    return {
        "messages": [HumanMessage(content=f"Execution Results:\n{combined_output}")]
    }

# --- 4. THE VERIFIER NODE (QA) ---
def verifier_node(state: AgentState):
    """
    QA Engineer: Reviews the execution output.
    Decides if we need to retry (Self-Heal) or if we are done.
    """
    messages = state.get("messages", [])
    last_output = messages[-1].content
    
    # Simple heuristic for now: If massive stderr error, reject.
    # Ideally use LLM, but for speed let's use a fast LLM or heuristic
    
    if "ERROR:" in last_output or "Error:" in last_output or "failed" in last_output.lower():
         # Check if it's a real error or just incidental
         llm = get_llm(model=MODEL_FAST, temperature=0.1)
         prompt = f"""Analyze this execution log. Did the command succeed or fail? 
         If minor warning, say PASS. If critical failure, say FAIL.
         
         LOG:
         {last_output[:2000]}
         
         Output only PASS or FAIL.
         """
         res = llm.invoke([HumanMessage(content=prompt)])
         status = "rejected" if "FAIL" in res.content.upper() else "approved"
    else:
        status = "approved"
        
    # Check for "MISSION COMPLETE" signal from Coder
    coder_msgs = [m.content for m in messages if hasattr(m, "content") and "MISSION COMPLETE" in m.content]
    is_complete = len(coder_msgs) > 0
    
    if is_complete and status == "approved":
        return {"review_status": "approved"}
    elif status == "rejected":
        # Add guidance for the coder
        return {
            "review_status": "rejected", 
            "messages": [HumanMessage(content="❌ QA REJECTED: Previous command failed. Please fix the error.")]
        }
    else:
        return {"review_status": "pending"}

# --- CONDITIONAL LOGIC ---
def router(state: AgentState) -> Literal["architect", "coder", "verifier", "executor", "end"]:
    # Initial state
    if not state.get("strategy"):
        return "architect"
    
    last_msg = state["messages"][-1]
    
    # If we just executed, go to verifier
    if isinstance(last_msg, HumanMessage) and "Execution Results" in last_msg.content:
        return "verifier"
        
    # If Verifier Approved and Mission Complete -> End
    if state.get("review_status") == "approved":
        return "end"
        
    # If Verifier Rejected -> Back to Coder
    if state.get("review_status") == "rejected":
        return "coder"
        
    # If Coder just spoke -> Go to Executor
    # (Assuming Coder outputted commands)
    return "executor" # logic simplified for demo

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(AgentState)

workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", execute_node)
workflow.add_node("verifier", verifier_node)

workflow.set_entry_point("architect")

workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "executor")
workflow.add_edge("executor", "verifier")

def verifier_routing(state: AgentState):
    status = state.get("review_status")
    if status == "approved":
        return END
    elif status == "rejected":
        return "coder"
    else:
        return "coder" # Continue working

workflow.add_conditional_edges(
    "verifier",
    verifier_routing,
    {
        END: END,
        "coder": "coder"
    }
)

graph = workflow.compile()

def run_agent(task_name: str, plan: str, context: str = ""):
    """Entry point"""
    initial = {
        "task": task_name, 
        "context": context, 
        "project_root": str(PROJECT_ROOT),
        "messages": [],
        "review_status": "pending"
    }
    return graph.invoke(initial)
