# Orchestration Protocol

Use this protocol to run a bounded, evidence-based engineering loop in any project or technology stack.

## Runtime discovery

Before assigning work, inspect the active runtime rather than relying on remembered capabilities:

1. Identify available coordination operations for creating, listing, messaging, following up with, interrupting, and waiting for agents.
2. Identify the model and reasoning choices the runtime actually exposes when selection is permitted.
3. Inspect live agents and usable concurrency. Count the Orchestrator and preserve enough capacity to coordinate and repair.
4. Inspect workspace instructions, permissions, current changes, and whether multiple agents share a filesystem or use isolated workspaces.
5. Record unavailable capabilities and choose the fallback path. Never emulate a forbidden capability or claim one exists.

Treat runtime values as observations for the current task. Do not write model identifiers, reasoning tiers, or slot counts into reusable rules.

## State ledger

Maintain a compact ledger with:

```text
objective:
acceptance criteria:
non-goals:
current state:
work items: id | owner | scope | write ownership | dependencies | status
evidence: criterion | artifact or command | result | source
failures: cycle | gate | observation | classification | disposition
decisions and assumptions:
remaining risks:
```

Keep one state active at a time. State transitions are decisions made by the Orchestrator, not by a subagent.

## State contracts

| State | Entry condition | Owner | Required input | Expected output | Exit condition and next state | Failure action |
|---|---|---|---|---|---|---|
| `INTAKE` | A user supplies an eligible request. | Orchestrator | User objective, explicit delegation authorization, workspace context | Observable acceptance criteria, boundaries, non-goals, authorization notes | Objective is actionable → `DISCOVER` | Material ambiguity requiring a user choice → `ESCALATE` |
| `DISCOVER` | Intake is actionable but facts or constraints need confirmation. | Orchestrator; Investigator when useful | Acceptance criteria, source artifacts, instructions, current workspace/runtime state | Facts, inferences, uncertainties, risks, candidate verification commands | Evidence is sufficient to plan → `PLAN` | Missing authority or inaccessible essential source → `ESCALATE`; otherwise narrow assumptions and continue discovery |
| `PLAN` | Relevant evidence and constraints are known. | Orchestrator | Discovery report and acceptance criteria | Dependency-aware work items, ownership map, verification strategy, rollback or containment notes where relevant | Every item is independently understandable and testable → `ASSIGN` | Coupled or conflicting scopes → revise the plan before assignment |
| `ASSIGN` | A safe work breakdown exists. | Orchestrator | Work items, role needs, runtime capacity, prompt contract | Named owners, self-contained prompts, write boundaries, dependencies, reporting formats | Each active agent has one bounded contract → `EXECUTE` | Capacity shortage → sequence roles or use fallback; ownership ambiguity → return to `PLAN` |
| `EXECUTE` | Contracts and ownership are acknowledged. | Investigator or Implementer for assigned item; Orchestrator coordinates | Task prompt, permitted artifacts, upstream evidence | Investigation report or scoped changes plus executed local checks and limitations | All required work items return inspectable artifacts → `VERIFY` | Agent stalls, expands scope, or conflicts → stop affected item, preserve artifacts, reassign or return to `PLAN` |
| `VERIFY` | Candidate artifacts and implementation evidence exist. | Verifier where available; Orchestrator owns gate decision | Acceptance criteria, raw diff/files, commands and outputs, known risks | Per-criterion pass/fail/blocked verdict with reproducible evidence | All gates pass → `INTEGRATE`; any correctable gate fails → `DIAGNOSE` | Unverifiable essential behavior or new authorization needed → `ESCALATE` |
| `DIAGNOSE` | Verification reports at least one failure. | Orchestrator, optionally Investigator or independent Verifier | Exact failed gate, expected vs actual result, raw evidence, prior cycles | Root-cause hypothesis, failure class, affected scope, revised repair and verification plan | A bounded repair is justified → `REPAIR` | Same failure persists or evidence contradicts assumptions → reopen `DISCOVER`; decision/authority needed → `ESCALATE` |
| `REPAIR` | A diagnosed, authorized repair exists. | Prefer the original Implementer; Orchestrator controls scope | Follow-up contract, failure evidence, allowed files, required reruns | Minimal corrective change and fresh evidence | Repair artifact is inspectable → `VERIFY` | Repair expands ownership or invalidates plan → `PLAN`; unsafe or unauthorized action → `ESCALATE` |
| `INTEGRATE` | Independent verification gates pass. | Orchestrator or designated Integrator | Verified work items, ownership map, user baseline, integration checks | Coherent final diff/artifact, aggregate check results, preserved user changes | Every criterion remains satisfied after integration → `COMPLETE` | Conflict or regression → `DIAGNOSE` |
| `COMPLETE` | Integration passes and no required work remains. | Orchestrator | Final evidence matrix, limitations, workspace status, Goal state if requested | User-facing outcome, changes, evidence, limitations, next steps | Final report delivered; requested Goal marked complete | Newly discovered failure means completion was premature; resume at `DIAGNOSE` |
| `ESCALATE` | A material user decision, additional authority, inaccessible external state, or unresolved repeated failure prevents safe progress. | Orchestrator | Blocker evidence, attempted alternatives, risk | Concise blocker plus concrete user choices and consequences | User resolves blocker → appropriate prior state | Do not guess, broaden authority, or report success |

## Roles and dynamic sizing

### Orchestrator

Own the objective, acceptance criteria, plan, prompts, dependencies, ownership map, state transitions, evidence review, integration, and final decision. Inspect source artifacts directly. Do not accept an agent's completion claim without evidence.

### Investigator

Examine code, documents, logs, behavior, and constraints. Work read-only unless the contract explicitly grants a narrow write. Separate verified facts, inferences, uncertainties, and risks. Return evidence another role can reproduce.

### Implementer

Modify only the declared scope. Avoid unrelated refactors and formatting. Preserve existing changes. Run assigned checks, report exact results, and disclose failures or incomplete items.

### Verifier

Start from acceptance criteria and raw artifacts. Prefer direct inspection and reproduced commands over the Implementer's narrative. Check omissions, regressions, edge cases, policy compliance, and assumptions. Remain read-only by default.

### Integrator

Use this as an Orchestrator responsibility unless shared files or many independent results justify a separate owner. Resolve conflicts only inside the assigned integration scope and rerun aggregate gates.

Scale roles to useful independence and live capacity. Combine roles sequentially when necessary, but never let an Implementer self-approve the same evidence without a distinct verification pass. Keep the Orchestrator in control even when only one execution slot exists.

## Ownership and parallelism

- Assign exclusive write ownership by exact files or non-overlapping directories before parallel implementation.
- Allow parallel read-only investigation and verification when they do not mutate shared state.
- Give one Integrator ownership of shared manifests, indexes, schemas, generated lockfiles, or other convergence points.
- Require an agent that discovers an out-of-scope change to report it and wait; amend the plan before authorizing the change.
- Inspect the working tree before and after assignments. Treat pre-existing changes as user-owned unless proven otherwise.
- Never revert or delete unrelated work. Request approval for destructive actions.

If agents share a filesystem, avoid asking one agent to reapply changes already present. If they use isolated workspaces, define how the Orchestrator will receive and integrate artifacts without assuming commits or pushes are authorized.

## Goal policy

Create a Goal only on explicit user request. Describe the final outcome, not the subtask list. Set a token budget only when the user explicitly provides one. Manage work items in the plan and state ledger. Mark the Goal complete only when every completion gate passes. Mark it blocked only under the runtime's blocking rules, not because the task is difficult or a loop limit was reached.

## Single-agent fallback

Use the fallback when subagents are unavailable, forbidden, wasteful for the task, or capacity is exhausted:

1. Keep the same states and ledger.
2. Perform investigation before planning.
3. Implement only after declaring scope and expected evidence.
4. End the implementation pass, then begin a fresh verification pass from the original criteria and raw diff.
5. Classify failures and run the same bounded repair loop.
6. Disclose that verification was perspective-separated but not independently executed by another agent.

## Limits and escalation

Recommend at most three `VERIFY → DIAGNOSE → REPAIR` cycles unless the user sets a different bound. Treat the bound as a review point, never as a success condition. On a repeated failure:

1. Revisit assumptions.
2. Recollect original evidence.
3. Classify the failure.
4. Revise the plan rather than repeat the command blindly.
5. Seek a different verification perspective when useful and available.
6. Decide whether a user choice or new authority is required.

Never promise hard per-agent token limits, hard execution timeouts, unlimited background work, automatic approvals, live session transfer between computers, unauthorized commits/pushes/deployments, or runtime capabilities that are not present.
