from state import BugState
from utils.llm import call_llm

SYSTEM_PROMPT = """

"""

def planner_node(state: BugState) -> dict:
    history = state.get("strategy_history", [])
    history_text = ("\n".join(f"- {h}" for h in history) if history else "(none yet")
    user_prompt = f"""
    Bug Description:
    {state['bug_description']}

    Strategies already taken:
    {history_text}

    Provide the next diagnosis + strategy.
    """

    diagnosis = call_llm(SYSTEM_PROMPT, user_prompt)

    res = {
        "diagnosis": diagnosis,
        "strategy_history": history + [diagnosis],
    }
    return res

"""
reads the report, figures what is broken and specifies next approach
"""