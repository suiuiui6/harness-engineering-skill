# Skill Evaluation Convergence Actions

## Scope

This checklist captures the five convergence actions under `evals/skill-evaluation` and defines concrete acceptance criteria.

## Action 1: Add execution checklist and acceptance criteria

- Deliverable: this file.
- Acceptance:
  - Includes all 5 actions.
  - Each action has measurable completion criteria.

## Action 2: Tighten Eval2 assertion for tri-agent collaboration

- Target file:
  - `iteration-1/eval-2-existing-components/eval_metadata.json`
- Change:
  - Replace generic "mention three agents" wording with a concrete requirement for planner/coder/reviewer sequence and role boundaries.
- Acceptance:
  - Assertion text is specific and objectively gradable.
  - No ambiguity between runtime RAG agents and development collaboration agents.

## Action 3: Require structured `subagent_type` example in Eval3

- Target file:
  - `iteration-1/eval-3-agent-setup/eval_metadata.json`
- Change:
  - Keep multi-format acceptance, and explicitly require at least one structured Agent-call example including `subagent_type`.
- Acceptance:
  - Assertion text accepts natural-language or slash guidance for invocation, but also requires one structured `subagent_type` example.

## Action 4: Unify Layer terminology in skill-evaluation docs

- Target files:
  - `iteration-1/benchmark.md`
- Change:
  - Replace stale "8-layer" phrasing with unified "7-layer (Layer 0-6)" wording.
- Acceptance:
  - No remaining "8-layer" wording in `evals/skill-evaluation` docs.

## Action 5: Expand benchmark follow-up plan

- Target file:
  - `iteration-1/benchmark.md`
- Change:
  - Add follow-up section for sample expansion and eval design repairs.
- Acceptance:
  - Includes run-count expansion plan.
  - Includes explicit handling for Eval2 and Eval3 assertion behavior.
  - Includes completion condition for next iteration.
