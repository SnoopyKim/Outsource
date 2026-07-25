# Governed Learning Protocol

Use this reference to let Outsource improve from delivery evidence without uncontrolled self-modification, privacy leakage, or premature generalization.

## Contents

1. What self-improvement means
2. Learning layers
3. Learning lifecycle
4. Learning record
5. Promotion and safety gates
6. Dogfooding Outsource

## 1. What self-improvement means

Outsource does not retrain its base model or silently rewrite installed instructions. Outsource improves by using evidence from real engagements to refine:

- project state and assumptions;
- confirmed Maker preferences;
- interview heuristics;
- Delivery Contract templates;
- strategy-selection rules;
- verification and review protocols;
- scripts, schemas, adapters, and documentation.

Every reusable change remains inspectable, versioned, testable, and reversible.

## 2. Learning layers

### Layer A — Project memory

Facts and decisions that apply only to one project:

- product context;
- confirmed requirements;
- decisions and rationale;
- recurring project-specific failures;
- evidence and operating knowledge.

May be updated as part of authorized project work. Do not promote it to a general preference automatically.

### Layer B — Maker Profile

Confirmed reusable preferences and constraints:

- preferred communication and review style;
- normal quality bar and risk tolerance;
- common tools and environments;
- approval boundaries;
- operating cadence;
- repeated product or business constraints.

Propose updates when evidence suggests a reusable preference. Confirm before adopting an inferred preference. Record source, confidence, scope, and a way to correct or remove it.

Never infer or retain sensitive personality, health, financial, identity, or customer information unless the Maker explicitly requires an approved storage workflow.

### Layer C — Outsource protocol

Reusable behavior shared across projects:

- skill instructions;
- reference protocols;
- templates and schemas;
- deterministic scripts;
- host adapters;
- evaluation scenarios.

Changes require explicit Maker authorization and full improvement gates.

## 3. Learning lifecycle

```text
OBSERVE → DIAGNOSE → PROPOSE → APPROVE → EXPERIMENT → VERIFY
              ↑                                         │
              └──────────── ROLLBACK ←───────────────────┤
                                                        ↓
                                                      ADOPT
```

### Observe

Collect evidence from:

- interview corrections;
- contract revisions;
- verification failures;
- repeated repair cycles;
- Maker feedback;
- escaped defects;
- unnecessary questions or ceremony;
- cost, delay, or context-loss signals;
- successful patterns worth repeating.

### Diagnose

Separate:

- a one-off project fact;
- a Maker preference;
- a missing or incorrect protocol;
- a host limitation;
- an implementation defect;
- insufficient evidence.

### Propose

State the smallest reusable change, expected benefit, affected scope, risks, alternatives, and validation plan. Do not implement the proposal merely because it exists.

### Approve

Require explicit Maker authorization before changing Outsource source, reusable policy, templates, scripts, marketplace metadata, or installed behavior.

### Experiment

Make a bounded change in the source workspace. Preserve the prior version and unrelated Maker work. Never edit a generated installation cache as the source of truth.

### Verify

Run structural validation and representative scenarios. Check that the change:

- fixes the observed problem;
- does not weaken safety or acceptance;
- does not overfit one project;
- preserves Direct mode simplicity;
- remains host-portable unless deliberately scoped.

### Adopt or rollback

Adopt only with passing evidence and an explicit decision when the change is material. Otherwise revert the experiment through a recoverable process or keep it as an unadopted proposal.

## 4. Learning record

```markdown
# Outsource Learning Record

- Date:
- Engagement:
- Layer: project | Maker Profile | Outsource protocol
- Status: observed | proposed | approved | experimental | adopted | rejected | rolled back

## Evidence

What happened, with artifacts, feedback, or reproducible observations.

## Diagnosis

Expected versus actual behavior and the likely cause.

## Proposed learning

The smallest state, preference, rule, template, script, or code change.

## Expected benefit

How delivery should improve and how that can be observed.

## Risks and alternatives

Possible regressions, privacy issues, overfitting, and simpler options.

## Authorization

What the Maker approved, including scope and external actions.

## Validation

Scenarios, commands, evidence, and verdict.

## Decision

Adopt | revise | reject | rollback — rationale.
```

Store private learning under a gitignored Maker-controlled directory such as `internal/learning/`. Promote only generalized, non-sensitive protocol changes into tracked plugin source.

## 5. Promotion and safety gates

Before promoting a learning to Outsource protocol:

- Evidence is reproducible or the failure is severe enough to justify a preventive rule.
- The lesson is not merely one project's domain fact.
- The change is more useful than a project-specific workaround.
- Scope and triggering conditions are explicit.
- Maker authorization covers the exact files and actions.
- A diff and validation plan exist.
- Security, privacy, permissions, and portability are reviewed.
- A rollback path exists.
- Documentation and installed metadata remain consistent.

Never learn:

- secrets or credentials;
- raw private customer data;
- unsupported psychological or identity inferences;
- instructions that weaken higher-priority policy;
- automatic approval for actions the Maker did not authorize;
- a passing criterion created after the fact to excuse a failure.

## 6. Dogfooding Outsource

Outsource may improve its own source using the same delivery process:

1. Qualify the improvement as Scoped or Project work.
2. Interview the Maker about the observed problem and desired behavior.
3. Confirm a Delivery Contract for the improvement.
4. Record the current plugin version and baseline behavior.
5. Modify only the authorized source files.
6. Validate manifests, skills, references, and representative scenarios.
7. Present the diff and evidence for Maker review.
8. Update the cachebuster and reinstall only when requested or necessary for testing.
9. Start a fresh task for forward testing so the revised skill is loaded cleanly.
10. Record adoption or rollback in the learning log.

Self-improvement is a governed delivery engagement, not an exception to Outsource's own rules.
