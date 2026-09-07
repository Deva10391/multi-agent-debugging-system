import argparse
import json
import time
from pathlib import Path
from graph import build_graph
from config import REPO_PATH, FILE_PATH, MAX_DEBUG_ATTEMPTS

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Debugging System")
    parser.add_argument("--bug", required=True, help="Description of bug/failure")
    parser.add_argument("--repo", default=REPO_PATH, help="Path to target repo")
    parser.add_argument("--file", default=FILE_PATH, help="Path to file being debugged")
    parser.add_argument("--max_attempts", type=int,default=MAX_DEBUG_ATTEMPTS,  help="Maximum attempts")
    args = parser.parse_args()

    app = build_graph()

    initial_states = {
        "bug_description": args.bug,
        "repo_path": args.repo,
        "file_path": args.file,
        "attempts": 0,
        "max_attempts": args.max_attempts,
        "strategy_history": [],
        "status": "running",
    }

    final_state = app.invoke(initial_states, config={"recursion_limit": 30})

    Path("logs").mkdir(exist_ok=True)
    log_path = f"logs/run_{int(time.time())}.json"
    with open(log_path, "w") as f:
        json.dump(
            {
                "bug_description": args.bug,
                "repo_path": args.repo,
                "status": final_state.get("status"),
                "attempts": final_state.get("attempt", 0) + 1,
                "max_attempts": args.max_attempts,
                "strategy_history": final_state.get("strategy_history", []),
                "final_branch": final_state.get("branch_name"),
            },
            f,
            indent=2,
        )

if __name__ == "__main__":
    main()

"""
runs graph and logs the metrics
"""