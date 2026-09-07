from state import BugState
from utils.llm import call_llm

SYSTEM_PROMPT = """
as a critic, i need you to help me understanding why the given fix-attempt failed;
how?- by responding in 1-3 sentences only;
sharing only the specific Technical reason (wrong logic/file/syntax/test assertion/ et cetera);
be it precise and actionable as i'll be appending it to strategy-history for the code-base;
"""

def critic_node(state: BugState) -> dict:
    print('criticizing')
    attempt = state.get("attempt", 0)
    max_attempts = state.get("max_attempts", 5)

    if state.get("test_passed"):
        return {"critic_decision": "accept", "status": "success"}

    if attempt + 1 >= max_attempts:
        return {"critic_decision": "escalate", "status": "escalated"}

    failure_reason = call_llm(SYSTEM_PROMPT, state.get("test_stdout", ""))
    history = state.get("strategy_history", [])
    if history:
        history[-1] = f"{history[-1]} --> FAILED: {failure_reason}"
    else:
        history.append(f"FAILED: {failure_reason}")

    res = {
        "critic_decision": "retry",
        "attempt": attempt + 1,
        "strategy_history": history,
    }
    print('criticiz-ation complete')

    return res

"""
to test the results and accept/escalate intelligently
"""