# Verification Gates

Use gates to decide state transitions from evidence, not confidence.

## Evidence hierarchy

Prefer evidence in this order:

1. Direct inspection of final source artifacts and workspace state.
2. Reproduced tests, builds, static analysis, or behavior checks with actual results.
3. Focused inspection of edge cases, regressions, permissions, and integration boundaries.
4. Agent reports that cite inspectable artifacts and captured output.
5. Unsupported summaries or predictions, which do not satisfy a gate.

Do not accept these as completion evidence:

- An agent says “done.”
- A test command is listed but was not run.
- A summary is present but no actual diff or artifact was inspected.
- A failure is ignored or labeled “pre-existing” without baseline evidence.
- Only happy-path behavior was considered where boundary conditions matter.

## Candidate gate

Before independent verification, require:

- Declared changed files or artifacts.
- A diff or equivalent inspectable result.
- Implementer checks with exact outcomes.
- Disclosed failures, skipped checks, assumptions, and limitations.
- Confirmation that changes stayed inside assigned ownership.

Failure means return to `EXECUTE`, `PLAN`, or `ESCALATE` as the evidence dictates; do not ask the Verifier to reconstruct an undocumented implementation.

## Independent verification gate

Verify each acceptance criterion separately:

| Check | Evidence required |
|---|---|
| Required behavior | Direct artifact inspection and the strongest feasible executed behavior check |
| Regression safety | Relevant existing checks plus focused neighboring or boundary checks |
| Scope discipline | Diff and workspace status show no unrelated or conflicting edits |
| User work preservation | Baseline/current comparison accounts for pre-existing changes |
| Policy and security | Applicable instructions, permission boundaries, secret scan, and destructive-action review |
| Portability | No unjustified machine path, project, stack, model, concurrency, or shell assumption |
| Documentation | Usage, limitations, and commands match actual artifacts and observed behavior |

Report `pass`, `fail`, or `blocked` for every criterion. A missing required check is not a pass.

## Failure diagnosis

Classify a failed gate before choosing a repair:

- `implementation`: the artifact does not meet a criterion.
- `test`: the check or fixture is incorrect, incomplete, or stale.
- `environment`: a dependency, permission, platform, or service prevents a valid run.
- `requirement`: criteria are contradictory or materially ambiguous.
- `integration`: individually valid work conflicts when combined.
- `authorization`: the next necessary action exceeds user-granted scope.
- `unknown`: evidence is insufficient; return to discovery instead of guessing.

Record expected versus actual behavior, minimal reproduction, affected criteria, evidence source, and whether the failure repeated from a prior cycle.

## Repair-loop gate

Recommend at most three verification-repair cycles unless the user provides another limit. For every cycle:

1. Give the Implementer the exact failed gate and raw evidence.
2. Preserve already accepted behavior and unrelated user work.
3. Require the failed check and relevant regression checks to run again.
4. Send the result back through the independent verification gate.

If the same failure repeats, do not retry unchanged work. Revisit assumptions and original evidence, revise the plan, and use a different verification perspective when available. At the limit, either produce a new evidence-backed strategy or escalate. Never translate exhaustion into success.

## Integration gate

Before `COMPLETE`, the Orchestrator must confirm:

- Every acceptance criterion has current passing evidence.
- The final combined diff matches the ownership and scope plan.
- Relevant focused and aggregate checks pass after integration.
- Verifier findings are repaired, accepted by an authorized user, or explicitly remain as a blocker.
- Pre-existing user changes remain intact.
- No secrets, credentials, unintended absolute paths, or unauthorized external actions were introduced.
- Known limitations and checks that could not run are documented with residual risk.
- Requested documentation and installation or operating instructions match the final artifact.
- Any explicitly requested Goal is complete in fact before its status is changed.

## When validation cannot run

State the exact blocker and distinguish it from a product failure. Use the strongest safe substitute—such as schema parsing, static inspection, a smaller test, or command discovery—but label it as substitute evidence. Report the untested behavior and its risk. If that behavior is essential to the acceptance criteria, choose `blocked` or `ESCALATE`, not `pass`.
