# codex-loop-engineering

`loop-engineering` is a stack-independent Codex Plugin for running substantial engineering work as an evidence-driven feedback loop:

```text
understand → investigate → plan → assign → implement → verify
                                      ↑          ↓
                                      └─ repair ← diagnose
```

Codex remains the orchestrator. It owns the completion criteria, gives bounded work contracts to subagents, inspects their changes and evidence, sends failures back for repair, and performs final integration. The Plugin does not add models, permissions, background execution, or external state transfer; it teaches Codex how to use capabilities that the active runtime and user authorization already provide.

## When to use it

Invoke `$loop-engineering`, or explicitly ask Codex for multi-agent, subagent, team, parallel investigation/implementation/verification, an orchestrator-led workflow, or repeated verify-and-repair work through completion.

Representative uses include:

- Investigate a cross-cutting defect, divide independent module fixes, and verify the integrated behavior.
- Build a feature across separable components while one owner controls shared files and another independently tests the result.
- Analyze a failing migration, repair it through bounded validation loops, and escalate if the same failure persists.
- Coordinate a technology-neutral documentation, configuration, and implementation change with traceable acceptance evidence.

Do not form a team automatically for a simple question, explanation, tiny single-file edit, or other task where delegation would cost more than it helps. If the user explicitly invokes the Skill for a small task, preserve the verification discipline but use the single-agent fallback.

## Install locally

From any machine with this repository available, add its repo-local Marketplace and install the Plugin:

```bash
codex plugin marketplace add ./path/to/codex-loop-engineering
codex plugin add loop-engineering@agent-harnesses
```

Start a new Codex task after installation so the Skill is discovered in a clean context.

## Install from Git

Add this repository as a Git-backed Marketplace and install the Plugin:

```bash
codex plugin marketplace add SnoopyKim/codex-loop-engineering --ref main
codex plugin add loop-engineering@agent-harnesses
```

Source: <https://github.com/SnoopyKim/codex-loop-engineering>

## Update a local development install

After changing the Plugin itself, use the `plugin-creator` cachebuster helper, reinstall from the already registered local Marketplace, and then validate it in a new Codex task:

```bash
python3 path/to/plugin-creator/scripts/update_plugin_cachebuster.py ./plugins/loop-engineering
codex plugin add loop-engineering@agent-harnesses
```

Do not hand-edit the Marketplace file to force a refresh.

## Update a Git install

Refresh the configured Git Marketplace snapshot, reinstall the Plugin, and then validate it in a new Codex task:

```bash
codex plugin marketplace upgrade agent-harnesses
codex plugin add loop-engineering@agent-harnesses
```

## Operating model

The Skill discovers available agent and coordination capabilities at runtime, sizes the team to the useful work and live concurrency, and assigns non-overlapping file ownership before parallel writes. Investigators are read-only by default, implementers stay inside their declared scope, and verifiers independently inspect source artifacts and executed checks. Verification failures move through diagnosis and repair, normally for no more than three cycles unless the user sets another limit. Reaching the limit never counts as success.

When subagents are unavailable, disallowed, or wasteful, Codex executes the same state machine sequentially and explicitly separates implementation from a fresh verification pass.

## Security and permissions

- Installation grants no additional permissions and bypasses no system or user policy.
- The active machine's Codex settings determine available tools, models, concurrency, approvals, and sandbox boundaries.
- The Skill never promises automatic approvals, unlimited background work, cross-machine live-session transfer, hard per-agent token or time limits, commits, pushes, deployments, or external changes without authorization.
- Keep secrets in the environment or an approved secret store; this repository contains no credentials or machine-specific paths.
