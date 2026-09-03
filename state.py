from typing import TypedDict, List, Optional

class BugState(TypedDict, total=False):
    bug_description: str
    repo_path: str
    attempt: str
    max_attempts: str
    branch_name: str
    diagnosis: str
    strategy: List[str]
    patch_diff: str
    test_stdout: str
    test_passed: bool
    critic_decision: str
    status: str

"""
passed between each node of the StateGraph
for reproducability
"""