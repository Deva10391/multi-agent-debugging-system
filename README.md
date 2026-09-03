# Autonomous Multi-Agent Debugging System

A closed-loop, self-correcting agent pipeline that detects, patches, and verifies fixes to broken code — without blind retries.

## Problem

Most "AI coding agent" demos are single-shot: one prompt in, one patch out, no verification. They fail silently when the patch is wrong, and offer no recovery path.

## Solution

A three-agent loop — **Planner → Executor → Critic** — where every patch is tested inside an isolated sandbox before being accepted. On failure, the Critic diagnoses *why* and routes a new strategy back to the Planner, instead of repeating the same fix blindly. The loop terminates on success or a bounded retry limit.

## Speciality

- Self-correction, not just generation — the rare, interview-defensible differentiator vs. typical "AI writes code" projects.
- Every accepted patch is machine-verified (tests pass), not just plausible-looking.
- Produces a hard metric: failure-recovery rate across retries (e.g. 62% → 89% success by attempt 3).

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

## Utilities Used

| Utility | Role |
|---|---|
| LangGraph | Orchestrates state machine between Planner / Executor / Critic nodes |
| Groq API | Low-latency inference for all three agent roles |
| GitPython | Isolates each attempt on its own scratch branch |
| Docker | Sandboxes patch execution — never runs untrusted code on host |
| pytest | Objectively verifies whether a patch actually fixes the bug |

## Non-Functional Requirements

- **Latency:** patch-attempt cycle under 30s
- **Idempotency:** repeated runs produce consistent results; no host side-effects
- **Bounded retries:** max 3–5 loop iterations, then escalate to human
- **Reproducibility:** temperature=0 on judge calls for explainable behavior

## Simplified Working

Feed it a broken piece of code. It reads the error, guesses a fix, tries it in a safe sandbox, checks whether the fix actually worked, and — if not — tries a smarter guess instead of repeating the same mistake. Like a junior developer debugging with a senior watching and correcting the approach after every failed attempt.

## Metrics Reported

- Success rate by retry attempt number
- Average time-to-fix
- Escalation rate (bugs the system couldn't resolve within retry budget)