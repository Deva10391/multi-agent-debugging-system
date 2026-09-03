from state import BugState
from utils.llm import call_llm
from utils.git_utils import create_attempt_branch, apply_patch_and_comit
from sandbox.docker_runner import run_tests_in_sandbox

SYSTEM_PROMPT = """

"""

def executor_node(state: BugState) -> dict:
    attempt = state.get("attempt", 0)
    branch = create_attempt_branch(state["repo_path"], attempt)

    user_prompt = f"""
    Diagnosis and Strategy:
    {state['diagnosis']}

    Bug Description:
    {state['bug_description']}

    Produce the unified diff now.
    """
    patch_diff = call_llm(SYSTEM_PROMPT, user_prompt)
    apply_patch_and_comit(
        state["repo_path"], patch_diff, message=f"attempt {attempt}: {branch}"
    )

    passed, output = run_tests_in_sandbox(state['repo_path'])

    res = {
        "branch_name": branch,
        "patch_diff": patch_diff,
        "test_passed": passed,
        "test_stdout": output,
        }
    return res

"""
to unify diff (of code), apples it in isolation, and triggers sandbox test
"""