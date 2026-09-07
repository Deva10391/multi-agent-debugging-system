import re
from state import BugState
from utils.llm import call_llm
from utils.git_utils import create_attempt_branch
from sandbox.docker_runner import run_tests_in_sandbox
from git import Repo

SYSTEM_PROMPT = """
aid me in code-fixing; i'll share bug description and seek that you provide me with the COMPLETE corrected file content to fix the bug;
how?- output ONLY the full file content in raw text format (not .md) and don't provide explanations, prose (before OR after);
i'll be sharing the current file content — use it as the base and output the entire file back, corrected, not just the changed part;
"""

def extract_code(text: str) -> str:
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def executor_node(state: BugState) -> dict:
    attempt = state.get("attempt", 0)
    branch = create_attempt_branch(state["repo_path"], attempt)

    file_path = f"{state['repo_path']}/{state['file_path']}"
    with open(file_path, "r", encoding="utf-8") as f:
        current_code = f.read()

    user_prompt = f"""
    Diagnosis and Strategy:
    {state['diagnosis']}

    Bug Description:
    {state['bug_description']}

    Current file content:
    {current_code}

    Output the complete corrected file content now.
    """
    new_code = extract_code(call_llm(SYSTEM_PROMPT, user_prompt))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    repo = Repo(state["repo_path"])
    repo.git.add(A=True)
    repo.index.commit(f"attempt {attempt}: {branch}")

    passed, output = run_tests_in_sandbox(state['repo_path'])

    return {
        "branch_name": branch,
        "patch_diff": new_code,
        "test_passed": passed,
        "test_stdout": output,
    }

"""
to overwrite the file with the corrected version, and triggers sandbox test
"""