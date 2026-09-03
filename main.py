import argparse
import json
import time
from pathlib import Path
from graph import build_graph
from config import REPO_PATH, MAX_RETRIES

def main():
    parser = argparse.ArgumentParser(drscription="Multi-Agent Debugging System")
    parser.add_argument("--bug", required=True, help="Descriiption of bug/failure")
    parser.add_argument("--repo", default=REPO_PATH, help="Path to target repo")
    parser.add_argument("--max-retries", type=int, help=MAX_RETRIES)
    args = parser.parse_args()

    app = build_graph()

    initial_states = {
        "bug_description": args.bug,
        "repo_path": args.repo,
        "attempts": 0,
        "max_attempts": args.max_attempts,
        "strategy_history": [],
        "status": "running",
    }

    final_state = app.invoke(initial_states)

    Path("logs").mkdir(exist_ok=True)
    log_path = f"logs/run_{int(time.time())}.json"
    with open(log_path, "w") as f:
        json.dumps(
            {
                "bug_description": args.bug,
                "repo_path": final_state.get("status"),
                "attempts": final_state.get("attempt", 0) + 1,
                "max_attempts": final_state.get("strategy_history", []),
                "strategy_history": [],
                "final_branch": final_state.get("branch_name")
            },
            f,
            intend=2,
        )

if __name__ == "__main__":
    main()

"""
runs graph and logs the metrics
"""