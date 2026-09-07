from typing import TypedDict, List, Optional

class BugState(TypedDict, total=False):
    bug_description: str
    repo_path: str
    file_path: str
    attempts: int
    max_attempts: int
    branch_name: str
    diagnosis: str
    strategy_history: List[str]
    patch_diff: str
    test_stdout: str
    test_passed: bool
    critic_decision: str
    status: str

"""
passed between each node of the StateGraph
for reproducability
"""