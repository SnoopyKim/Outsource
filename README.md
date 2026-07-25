# Outsource

> Outsource helps a Maker turn underspecified intent into an accepted outcome.

**Makers** are solo builders and solopreneurs who create and operate products with AI agents. **Outsource** is a Codex Plugin for the substantial work that should not depend on one lucky prompt: cross-cutting features, risky changes, and long-running projects that need discovery, delivery discipline, verification, feedback, and continuity.

```text
Maker intent
    ↓
qualify → deep interview → delivery contract → deliver → verify → review
                         ↑                              │          │
                         └──────── change ──────────────┘          ↓
                                                       handoff ← accept
                                                                  ↓
                                                                learn
```

The Maker owns purpose, constraints, meaningful choices, feedback, and acceptance. Outsource owns the missing delivery work: discovering consequential gaps, proposing scope and outputs, designing tests and evidence, selecting an execution strategy, producing the result, and presenting it for judgment.

Loops, graphs, multi-agent teams, and direct execution are strategies. They are not the goal.

## Engagement modes

Outsource matches process weight to the work:

- **Direct** — small, clear, low-risk requests. Execute with minimal clarification and verify the result.
- **Scoped** — bounded but ambiguous, cross-cutting, or meaningfully risky work. Run a focused interview and confirm a compact Delivery Contract.
- **Project** — large, long-running, multi-milestone, externally dependent, or difficult-to-reverse work. Use durable state, repeated Maker reviews, change management, acceptance, and handoff.

Outsource starts with the simplest reliable mode and increases structure only when the evidence justifies it.

## Deep Interview

The Maker is not expected to arrive with a complete specification, implementation plan, output format, and test suite.

Outsource first inspects the available project context, then adaptively interviews for information that could materially change:

- the desired outcome and why it matters;
- current product, users, workflow, and constraints;
- scope and explicit non-goals;
- meaningful preferences and authority boundaries;
- damaging failure modes and required confidence;
- operations, maintenance, launch, and handoff;
- assumptions that need investigation or a small experiment.

The interview ends when Outsource can make a responsible proposal—not when it has exhausted a fixed questionnaire or removed every uncertainty.

## Delivery Contract

Scoped and Project work produces a shared, versioned Delivery Contract containing:

- intended outcome and current context;
- scope and non-goals;
- constraints and approval points;
- recommended approach and alternatives;
- deliverables and milestones;
- Outsource-proposed acceptance criteria, tests, and evidence;
- assumptions, risks, open decisions, and change policy.

Technical execution, verification, and Maker acceptance are kept distinct:

```text
EXECUTED  → the planned result exists
VERIFIED  → required evidence passes
ACCEPTED  → the Maker reviews and accepts it
```

## Execution strategies

Outsource chooses after understanding the work:

- direct execution for simple tasks;
- a sequential verification loop for coupled work;
- parallel agents for independent scopes with exclusive ownership;
- graph orchestration when branching, joins, permissions, or recovery paths must be explicit;
- human gates for consequential external or hard-to-reverse actions.

One Delivery Orchestrator remains accountable for the contract, authority, state, integration, evidence, and final claims. Host-native agents, worktrees, goals, schedulers, and permission controls are used when available rather than reimplemented.

## Governed self-improvement

Outsource can improve while it is used, but it does not silently rewrite itself.

Learning is separated into:

1. **Project memory** — facts and decisions that apply to one project.
2. **Maker Profile** — confirmed reusable Maker preferences and operating constraints.
3. **Outsource protocol** — reusable skills, interview rules, templates, scripts, adapters, and evaluations.

Reusable protocol changes follow:

```text
observe → diagnose → propose → Maker approval → experiment → verify
                    ↑                                │
                    └──────── rollback ←─────────────┤
                                                     ↓
                                                   adopt
```

Changes to Outsource source require an inspectable proposal, explicit Maker authorization, bounded edits, regression checks, and an adopt-or-rollback decision. Private learning belongs in a Maker-controlled ignored directory; secrets and raw private customer data are never learned as reusable preferences.

## Current v0.1

The `outsource` Plugin currently provides one primary `$outsource` Skill with:

- engagement qualification;
- Deep Interview guidance and readiness rules;
- a canonical Delivery Contract;
- an outer project-delivery lifecycle;
- strategy selection for direct, loop, parallel, graph, and human-gated work;
- execution ownership, verification, diagnosis, and repair rules;
- feedback, change request, acceptance, and handoff semantics;
- a governed learning protocol for project memory, Maker Profile, and Outsource itself.

This is a protocol-first version. It does not yet add a database, background daemon, visual project dashboard, cost telemetry, or cross-host state service.

The previous `loop-engineering` Plugin remains in this repository as a compatibility and focused execution strategy during the Outsource transition.

## Install locally

Add this repository's local Marketplace, then install Outsource:

```bash
codex plugin marketplace add ./path/to/codex-loop-engineering
codex plugin add outsource@agent-harnesses
```

Start a new Codex task after installation so `$outsource` is discovered in a clean context.

## Install from Git

```bash
codex plugin marketplace add SnoopyKim/codex-loop-engineering --ref main
codex plugin add outsource@agent-harnesses
```

Source: <https://github.com/SnoopyKim/codex-loop-engineering>

The repository URL retains its historical name for now; the primary Plugin and product name are Outsource.

## Update a local development install

After changing Outsource, update its cachebuster, reinstall it from the registered Marketplace, and test it in a new Codex task:

```bash
python3 path/to/plugin-creator/scripts/update_plugin_cachebuster.py ./plugins/outsource
codex plugin add outsource@agent-harnesses
```

Do not hand-edit the Marketplace file or an installed plugin cache to force an update.

## Project principles

- Optimize for the Maker's accepted outcome, not agent activity.
- Ask only questions whose answers could materially change delivery.
- Let Outsource propose implementation and testing instead of delegating specification work back to the Maker.
- Preserve decisions, assumptions, changes, evidence, and next actions needed to resume.
- Use the simplest execution topology that can deliver reliably.
- Separate contract defects, misunderstandings, new requests, preferences, and next-phase ideas.
- Treat passing tests as evidence, not as Maker acceptance.
- Never broaden permissions, external actions, or self-modification authority implicitly.

## Security and permissions

- Installation grants no additional permissions and bypasses no system or Maker policy.
- The active runtime determines tools, models, concurrency, approvals, and sandbox boundaries.
- Outsource does not promise automatic approvals, unlimited background work, cross-machine state transfer, hard token limits, commits, pushes, deployments, purchases, or outbound communication without authorization.
- Keep secrets in the environment or an approved secret store.
- Store private Maker research and learning in an ignored or otherwise approved private location.
