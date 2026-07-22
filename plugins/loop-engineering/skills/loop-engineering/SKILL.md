---
name: loop-engineering
description: Orchestrate substantial, technology-independent engineering work through bounded investigation, planning, scoped subagent assignment, implementation, independent verification, diagnosis, repair, and integration loops. Use only when the user explicitly invokes `$loop-engineering` or explicitly requests multi-agent or subagent work, team implementation, parallel investigation/implementation/verification, an orchestrator-led delegation workflow, repeated verification and repair, or persistence through stated completion criteria. Do not automatically form a team for simple questions, explanations, short file edits, or requests that do not explicitly authorize subagents; use the sequential fallback when multi-agent execution is unavailable or disproportionate.
---

# Loop Engineering

Run a disciplined feedback loop while keeping the root agent accountable for scope, evidence, and completion. Treat every subagent report as a claim to inspect, not as proof.

## Load the operating references

Read these files before assigning work:

- Read [orchestration-protocol.md](references/orchestration-protocol.md) for runtime discovery, the complete state contract, role boundaries, ownership, Goal use, fallback, and escalation.
- Read [prompt-contracts.md](references/prompt-contracts.md) before composing an initial or follow-up subagent prompt.
- Read [verification-gates.md](references/verification-gates.md) before accepting implementation evidence, diagnosing a failure, or declaring completion.

## Start safely

1. Confirm that the request explicitly authorizes this Skill or multi-agent execution. Obey any higher-priority requirement that subagents need explicit user authorization.
2. Inspect the workspace, applicable instructions, current changes, permissions, coordination tools, available agent configurations, and live capacity. Discover these at runtime; never assume a model name, reasoning level, or slot count.
3. Restate the objective as observable acceptance criteria, boundaries, non-goals, and required evidence. Ask only when an unresolved choice would materially change the result.
4. Decide whether delegation adds value. Prefer a single agent for a tiny or tightly coupled task even when this Skill was explicitly invoked.
5. Create a Goal only when the user explicitly asks. State the final outcome in it, omit a token budget unless the user supplied one, and keep detailed steps in the plan and state ledger.
6. Preserve user changes. Never overwrite, discard, commit, push, deploy, approve permissions, or change external systems unless the request authorizes that action.

## Run the state loop

Maintain exactly one current state and a compact ledger of decisions, owners, evidence, failures, and transitions:

```text
INTAKE → DISCOVER → PLAN → ASSIGN → EXECUTE → VERIFY
                                               │
                         pass → INTEGRATE → COMPLETE
                                               │
                         fail → DIAGNOSE → REPAIR ─┘

Any state → ESCALATE when an authorized user decision is required
```

Follow every state's entry and exit contract in the orchestration protocol. Do not skip `VERIFY` because an implementer reports success. Do not enter `COMPLETE` until integration evidence satisfies every acceptance criterion.

## Size and assign the team

- Keep the root agent as Orchestrator and final decision owner.
- Add an Investigator for uncertain scope, behavior, evidence, or risk; make investigation read-only by default.
- Add Implementers only for independently testable scopes. Assign exclusive file or directory ownership before parallel writes.
- Add a Verifier with no implementation responsibility when capacity allows. If capacity is limited, reuse slots sequentially but perform verification from source artifacts with a fresh checklist.
- Reserve capacity for coordination and repair. Never spawn agents merely to fill available slots.
- Give each agent a self-contained contract from `prompt-contracts.md` and only the minimum necessary context. Prefer a task contract and raw evidence over the full conversation history.
- Reuse the same agent for follow-up repair when possible. Include the failed gate, observed evidence, expected result, allowed scope, and required rerun; do not resend an ambiguous “fix it” request.

## Control parallel writes

Record ownership before `EXECUTE`. Permit parallel reads and independent writes, but never let two Implementers edit the same file concurrently. Give one Integrator ownership of shared files. Require agents to stop and report an ownership conflict instead of expanding their scope. Inspect the combined diff for accidental overlap before verification.

## Verify and repair

Verify actual files, diffs, executed checks, edge conditions, and requirement coverage. Reject summaries, unexecuted commands, and self-reported completion as sole evidence. Classify failures before repair and normally cap verify-repair cycles at three unless the user specifies another limit. When the same failure repeats, re-check assumptions and source evidence, revise the plan, and consider another verification perspective; do not merely retry.

If validation cannot run, document the reason, substitute the strongest safe check, and carry the residual risk into the final decision. Reaching a loop limit is not success. Escalate with evidence and concrete choices when a user decision, new authorization, or external state change is essential.

## Finish

Integrate only after independent verification passes. Re-read the acceptance criteria, inspect the final diff and workspace status, run the strongest relevant aggregate checks, confirm user changes remain intact, and disclose any limitations. Mark a requested Goal complete only after all required work is actually done; include the Goal tool's final usage report when applicable.
