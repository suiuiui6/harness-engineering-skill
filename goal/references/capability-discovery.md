# Capability Discovery

Discover dependencies only before the first governed mutation, verification,
closure, or an explicit host question. Do not repeat discovery at ordinary
checkpoints.

## Discovery order

1. Start with the host-configured or otherwise known dependency command. Do
   not scan arbitrary locations or install a replacement during discovery.
2. Run its `capabilities` subcommand without `--workspace` or goal state and
   parse the single-line JSON descriptor. For Guard, the descriptor identifies
   `goal-guard`, protocol major `1`, supported state schemas, commands, and
   enforcement modes.
3. Load Goal Protocol v2 from `protocol.json` and use
   `scripts/protocol.py`'s `capability_compatible()` check for the named
   dependency. Also confirm that the operation's required command, state
   schema, and enforcement mode appear in the descriptor.
4. If the configured command is missing, does not recognize `capabilities`,
   or reports an incompatible descriptor, try the documented legacy Guard
   path once: `$env:USERPROFILE\plugins\goal-enforcement\scripts\goal_guard.py`.
   Apply the same JSON and compatibility checks to that result.
5. If no compatible dependency remains, emit the Goal Protocol v2 structured
   dependency blocker from `output-contract.md`. Use `DEPENDENCY_MISSING` when
   no candidate exists, `PROTOCOL_VERSION_MISMATCH` for a capability name or
   protocol-major mismatch, and `CAPABILITY_DISABLED` for malformed JSON or a
   required command, schema, or enforcement mode that is not advertised.
   Preserve the exact command result as evidence.

GSD is an optional Layer 6 adapter. Missing, invalid, disabled, or blocked GSD
falls back to the original `/goal` plus Harness Layer 6 path. Missing Harness
or Guard blocks only the operation that requires that capability; it does not
retroactively block intake, classification, or unrelated read-only work.

On Windows, report the available host mode as `audit-only-windows`. Audits are
required evidence, but hooks may be unavailable, so never claim that the host
mechanically blocked a mutation or completion.

## Successful Compatibility Reply

When the configured `capabilities` lookup succeeds, the user-facing reply must
explicitly state that it selected `goal-guard`; `scripts/protocol.py` checked
protocol major 1 and found it compatible; state schema 1, the required command
(for the capability eval, `write-state`), and `audit-only-windows` are present;
and the same operation continues. Do not try the legacy candidate and do not
emit a blocker after this successful result.
The reply is incomplete if it omits `scripts/protocol.py` or paraphrases away
that the same operation continues.

```text
Compatibility: The configured capabilities lookup selected goal-guard. scripts/protocol.py checked protocol major 1 and found it compatible; state schema 1, required command write-state, and enforcement mode audit-only-windows are present.
Next action: Continue the same operation. Do not try the legacy candidate and do not emit a blocker.
```

## Incompatible Candidate Evidence

When all candidates are incompatible, give evidence for each candidate
separately. For each candidate, name its lookup source—the configured command
or documented legacy path—and its observed result, including the reported
protocol major. Do not collapse these into an unsupported summary.

Use this fixed blocker shape, replacing the bracketed major values with the
observed values:

```text
[决策] Dependency -> blocked
Code: PROTOCOL_VERSION_MISMATCH
Dependency: goal-guard
Evidence: The configured Guard `capabilities` command reported protocol major [configured major]; the documented legacy path `$env:USERPROFILE\plugins\goal-enforcement\scripts\goal_guard.py capabilities` reported protocol major [legacy major]; Goal Protocol v2 requires major 1.
Impact: No compatible Guard remains, so the governed mutation cannot proceed.
Next action: Select or restore a Guard implementing goal-guard protocol major 1; do not execute or authorize the mutation.
```
