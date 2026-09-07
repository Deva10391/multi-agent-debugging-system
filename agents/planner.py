from state import BugState
from utils.llm import call_llm

SYSTEM_PROMPT = """
i need you to help me in debugging as a strategist; i'll share the bug description & history of failed strategies; and i seek that you provide me with ONE strategy to try next, to fix the bug;
how?- by staying concise & technical (so i can feed it directly to a code-fixing agent);
don't repeat the failed strategies;
i seek ONLY the diagnosis in plain text + strategy, not any form of code/ diff;
"""

def planner_node(state: BugState) -> dict:
    print('planning')

    history = state.get("strategy_history", [])
    history_text = ("\n".join(f"- {h}" for h in history) if history else "(none yet)")
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
    print('planning complete')

    return res

"""
reads the report, figures what is broken and specifies next approach
"""