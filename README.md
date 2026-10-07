# Autonomous Multi-Agent Debugging System
 
## Problem
 
Single-shot AI code-fix demos give one patch with no verification and no recovery when the patch is wrong.
 
## Solution
 
A LangGraph loop of three agents: Planner → Executor → Critic. The Executor rewrites the target file on its own scratch git branch and runs the repo's pytest inside a Docker sandbox. The Critic accepts on pass; on fail it writes a 1–3 sentence technical failure reason into the strategy history and routes back to the Planner, which must not repeat failed strategies. The loop stops on success or at the attempt limit (default 3), then escalates.
 
## Speciality
 
- Every accepted patch is verified by tests in an isolated container, never on the host.
- Failure reasons feed the next strategy, so retries are not blind.
- Each attempt is committed on its own branch (GitPython) and each run is logged to `logs/run_<timestamp>.json`.
- Measured result (`results.txt`): 15 runs, 100% success, 0% escalation, all fixed on attempt 1.
## Architecture
 
```
Bug report
   │
   ▼
┌─────────┐     ┌───────────┐      ┌────────┐
│ Planner │ ──▶ │ Executor  │ ──▶ │Sandbox │
│ (Groq)  │     │ (Groq +   │      │(Docker)│
└─────────┘     │ GitPython)│      └────────┘
   ▲            └───────────┘          │
   │                                   ▼
   │             ┌────────┐       ┌─────────┐
   └──retry────  │ Critic │  ◀──  │ pytest  │
      (new       │ (Groq) │       │ results │
      strategy)  └────────┘       └─────────┘
                       │
                  pass │ escalate
                       ▼
                 Patch accepted
```
 
## Simplified Working
 
You describe a bug and point at a file. It proposes a fix, tests it in a sandbox, and if the test fails it learns why and tries a different fix.
 
## Utilities
 
- LangGraph — state machine across Planner / Executor / Critic
- Groq API — LLM for all three roles (default `openai/gpt-oss-20b`, temperature 0)
- GitPython — one branch per attempt
- Docker — sandboxed test execution (30 s timeout)
- pytest — pass/fail verdict
- `metrics.py` — success and escalation rate by attempt count
## To Run
 
for installation,
```
pip install -r requirements.txt
 
mkdir repo && cd repo
git init -b main
printf '__pycache__/\n.pytest_cache/\n' > .gitignore
printf 'def factorial(n):\n    r = 0\n    for i in range(1, n + 1):\n        r *= i\n    return r\n' > repo_file.py
printf 'from repo_file import factorial\n\ndef test_factorial():\n    assert factorial(5) == 120\n    assert factorial(0) == 1\n' > test_repo_file.py
git add -A && git commit -m "buggy baseline"
cd ../
```
to run-
1. open docker.desktop
2. in cli, run
```
docker build -t debugger-sandbox:latest -f sandbox/Dockerfile.sandbox .
python main.py --bug "the code is supposed to find out factorial of number it gets; it is not doing that" --repo ./repo --file repo_file.py
```
you may even change based on your requirement
 
## To Get Metrics/ Performance
 
run-
 
```
chmod +x eval_cmds.sh
./eval_cmds.sh
python metrics.py
```