# Subagent Prompt Contracts

Give every agent an independent, bounded prompt. Do not make the full conversation the default source of truth.

## Context ladder

Provide context in this order and stop when the task is self-contained:

1. Independent task prompt.
2. Orchestrator-authored plan or work contract.
3. Required raw files, logs, diffs, commands, and evidence.
4. Only the smallest relevant excerpt of recent conversation when essential.

Do not leak an intended answer, suspected defect, or proposed fix into an independent verification prompt. Forward tests should receive the Skill and a realistic request, not the author's evaluation rubric or conclusions.

## Initial assignment template

```text
Role
- You are the <Investigator | Implementer | Verifier | Integrator> for work item <id>.

Objective
- Produce <specific observable result>.

Allowed scope
- Read: <files, directories, systems, or evidence>.
- Write: <exact files/directories, or “none”>.
- External actions: <explicitly authorized actions, or “none”>.

Forbidden changes
- Do not modify <shared or unrelated scope>.
- Do not commit, push, deploy, approve permissions, or alter external state unless explicitly listed above.
- Stop and report before expanding scope or conflicting with another owner's files.

Inputs and evidence
- Acceptance criteria: <criterion identifiers and text>.
- Known facts: <facts with source locations>.
- Dependencies: <completed upstream items or “none”>.
- Preserve: <pre-existing user changes and invariants>.

Completion conditions
- <artifact or behavior 1>.
- <artifact or behavior 2>.
- No changes outside the allowed scope.

Required verification
- Run or inspect: <specific checks that fit the project>.
- Capture exact commands, results, and relevant output; do not claim unexecuted checks.

Report format
- Status: complete | partial | blocked
- Files or artifacts changed: <list with purpose>
- Evidence: <criterion → command/inspection → result>
- Risks or regressions checked: <list>
- Uncertainties and assumptions: <list>
- Failures or remaining work: <list>

Failure behavior
- Preserve useful artifacts.
- Report expected versus actual behavior and the smallest reproducible evidence.
- Do not hide, reinterpret, or retry repeated failures without diagnosis.
```

## Investigator additions

Require four labeled sections: `Facts`, `Inferences`, `Uncertainties`, and `Risks`. Make reads the default. Ask for source locations and reproduction steps rather than broad recommendations.

## Implementer additions

Name exclusive write ownership. Require a minimal change, preservation of unrelated user work, and executed local checks. Tell the Implementer to report generated or shared files before modifying them when ownership is not explicit.

## Verifier additions

Supply the original acceptance criteria and raw artifacts, not the Implementer's conclusion. Use this report shape:

```text
Verdict: pass | fail | blocked
Gate results:
- <criterion>: pass | fail | blocked — <direct evidence>
Commands reproduced:
- <command>: <result>
Regression and edge checks:
- <check>: <result>
Missing evidence:
- <item>
Recommended next state: INTEGRATE | DIAGNOSE | ESCALATE
```

Keep verification read-only unless the Orchestrator explicitly issues a later repair contract.

## Follow-up repair template

Reuse the original Implementer when practical so it retains task-local context. Send a new bounded contract:

```text
Continue work item <id> as the same Implementer.

Failed gate
- Criterion: <original criterion>
- Expected: <observable expectation>
- Actual: <observed behavior>
- Evidence: <exact file, diff, command, or output>

Diagnosis
- Failure class: <implementation | test | environment | requirement | integration | authorization | unknown>
- Current hypothesis: <evidence-backed cause>

Repair scope
- You may modify only: <files/directories>.
- Preserve: <accepted behavior and user changes>.
- Do not: <forbidden expansion>.

Required rerun
- <failed check>
- <nearby regression checks>

Return
- Minimal diff, exact results, limitations, and any contradictory evidence.
- If the hypothesis is wrong, stop and report rather than widening scope.
```

Never send only “fix the tests,” “try again,” or another instruction that omits the observed failure and scope.

## Coordination messages

Use non-triggering messages for facts that should reach an already running agent without starting a new turn. Use follow-up work when an idle or completed agent must act again. Interrupt only to stop harmful, obsolete, or conflicting work. Wait in bounded intervals and surface approvals or required user input instead of answering them on the user's behalf.
