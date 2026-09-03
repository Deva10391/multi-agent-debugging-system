import time
from git import Repo

def create_attempt_branch(repo_path: str, attempt: int) -> str:
    repo = Repo(repo_path)
    base = repo.active_branch.name
    branch_name = f"debug-attempt-{attempt}-{int(time.time())}"
    repo.git.checkout(base)
    repo.git.checkout("-b", branch_name)
    return branch_name

# trace for diff (unification)
def apply_patch_and_comit(repo_path: str, patch_diff: str, message: str) -> None:
    repo = Repo(repo_path)
    patch_file = f"{repo_path}/.debugger_patch.diff"
    with open(patch_file, "w") as f:
        f.write(patch_diff)
    repo.git.apply("--allow-empty", patch_file)
    repo.git.add(A=True)
    repo.index.commit(message)

# reset on finish
def reset_to_base(repo_path: str, base_branch: str) -> None:
    repo = Repo(repo_path)
    repo.git.checkout(base_branch)


"""

"""