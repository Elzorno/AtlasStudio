# Interactive Shell

## Status

Specification only. No code exists yet. This document designs the behavior of `atlas` run with no arguments, for a future implementation work order to build against, per `ATLAS_CLI_SPEC.md`'s "Status" section.

## Purpose

Every command in `ATLAS_CLI_SPEC.md` already works as a single one-shot invocation (`atlas today`, `atlas next`, ...), which is what a script or CI check needs. A human running several commands in a row across one session wants something lighter: a persistent prompt that already knows the project, already ran `atlas status` once, and lets each following command drop the `atlas ` prefix. This document designs that prompt. It is a convenience layer over the exact same command dispatch table `ATLAS_CLI_SPEC.md` defines - not a second parser, not a second set of behaviors, and not a new execution model.

## Launching

```text
$ atlas

AtlasStudio v1.0

Project:
The Last Sword Protocol

Studio Health:
Healthy

Journey:
I

atlas>
```

Running `atlas` with no command and no arguments launches the shell. Running `atlas <command>` (with a recognized command name) never launches the shell - it always runs that one command and exits, exactly as documented in `ATLAS_CLI_SPEC.md` and `COMMAND_REFERENCE.md`. The shell is opt-in by omission, not a wrapper every invocation passes through.

The startup banner is produced by running `atlas status` once (`ATLAS_CLI_SPEC.md`'s `atlas status` command) and rendering its fields as the four labeled blocks shown above: `Project`, `Studio Health`, `Journey`, plus - only when nonzero - a fifth `Router` block showing pending/blocked counts, matching `atlas status`'s own text-mode output. If `atlas status` itself fails (for example, an unreadable graph file), the banner shows the specific error in place of the `Studio Health` block and still opens the prompt - a broken health check should be visible immediately, not hide the shell entirely.

## Prompt Behavior

The prompt is `atlas> `. Each line typed at the prompt is parsed exactly as if it had been passed to `atlas` on the command line with the leading `atlas` word removed - `atlas> today` behaves identically to running `atlas today` from a regular shell, dispatched through the same in-process command table (not a new subprocess per line, so repeated commands inside one session stay fast). Quoting rules for multi-word arguments (`atlas> ask "What should Codex work on?"`) follow ordinary shell-style quoting.

A bare `atlas` typed at the `atlas>` prompt (i.e., typing the program's own name again) is treated as a no-op that re-prints the current status banner - a natural typo-recovery behavior for a user who forgets they're already inside the shell.

Blank input (pressing Enter with nothing typed) does nothing and reprints the prompt. There is no default command run on Enter.

## Help

`help` (or `?`) with no arguments prints the Command Groups table from `ATLAS_CLI_SPEC.md` - one line per group, not all fifteen commands at once, so the first screen of help stays scannable. `help <command>` prints that command's full Purpose/Inputs/Outputs entry from `ATLAS_CLI_SPEC.md` verbatim - the shell's help text is generated from that specification document, not maintained as a separate copy, so the two can never drift apart silently.

```text
atlas> help

Situational awareness   today, next, status, doctor, history
Natural-language        ask
Routing & work          route, work, dispatch
Quality gates           review, playtest, validate
Knowledge & graph       graph, planner
Production milestones   release

Type `help <command>` for full detail, or `exit` to leave the shell.
```

## History

The shell keeps an in-session, line-based command history - every line successfully parsed and dispatched, in order, held in memory for the life of the shell process. Arrow-key recall (up/down through prior lines at the prompt) is standard REPL behavior and is expected from whatever line-editing library the future implementation uses (matching common Python REPL conventions - e.g. `readline`/`prompt_toolkit`-style behavior - rather than a bespoke implementation).

This in-session recall is distinct from `atlas history` (`ATLAS_CLI_SPEC.md`), which is a real `atlas` command querying the router log, work order status transitions, and Decision Records - persistent, cross-session, and unrelated to what was typed at this particular prompt. Running `atlas> history --work-order WO-0020` inside the shell calls that command normally; it does not search the shell's own line buffer. Naming them the same word twice (shell line-recall vs. the `atlas history` command) is intentional and mirrors how `git`'s own shell history and `git log` are two unrelated things a user is expected to already distinguish.

No shell-history line is ever persisted to disk by this design. A future implementation may add that (matching typical shell `~/.*_history` conventions) but it is not specified here, since nothing in AtlasStudio's daily loop currently depends on cross-session recall of typed commands - only on `atlas history`'s persistent, structured records.

## Autocomplete (Future)

Not specified for v1. `help`'s Command Groups table is v1's discoverability mechanism instead: a user unsure what to type runs `help`, not tab-completion. When autocomplete is added in a future work order, it should complete against exactly two vocabularies and no others, to avoid guessing at free text it cannot validate:

- The fifteen command names and their documented subcommands (`work create`, `work review`, `playtest record`, and so on) - a closed, enumerable list already defined in `ATLAS_CLI_SPEC.md`.
- Work order IDs, for any command taking one as a positional argument (`work show`, `work review`, `history --work-order`, `playtest record --work-order`) - completed from `work-orders/*.md` filenames at prompt time.

Autocomplete must never attempt to complete the free-text argument to `atlas ask` or `atlas route` - those are natural-language input, not a closed vocabulary, and completing against them would imply a false sense of a fixed command set for what is deliberately open text.

## Status Banner

The four-block banner shown at launch is not re-printed automatically after every command - a shell that reprinted its own banner after each line would push real command output off the top of a normal-sized terminal. Instead:

- `atlas status` typed explicitly re-prints the banner on demand.
- Any command that changes something the banner reports (a `work create` write, a `playtest record` status change, a `dispatch`) prints a one-line delta immediately after its own output, e.g. `(Studio Health unchanged; Router: 1 pending_approval, was 0)`, rather than the full banner - visible enough to notice a change, quiet enough not to duplicate the whole snapshot every time.
- `exit`/`quit` does not reprint the banner on the way out.

## Error Handling

An unrecognized command name prints exactly the message an ordinary shell would for a mistyped word, plus a pointer to `help`:

```text
atlas> revie
Unknown command: revie
Did you mean: review?
Type `help` to see all commands.
```

"Did you mean" suggestions are limited to an exact-prefix or single-edit match against the known command list - a real fuzzy-match algorithm is not specified here as a v1 requirement, only the behavior of offering one clear candidate when an obvious one exists and staying silent when it doesn't (never suggesting a wrong command with false confidence).

A command that fails (nonzero exit per `ATLAS_CLI_SPEC.md`'s shared exit code table) prints its normal failure output and returns to the `atlas>` prompt - the shell itself never exits because a single command failed. This matches every other command's own failure behavior already being non-fatal to the rest of a session (`atlas today` keeps running even when a repository is unclean; `atlas work review` keeps printing even when a check fails).

Ctrl-C during a running command cancels that command only (matching standard REPL signal handling) and returns to the prompt; it does not exit the shell. Ctrl-D on an empty prompt line, or typing `exit` or `quit`, ends the shell session cleanly with exit code 0.

No command inside the shell ever behaves differently from its one-shot invocation because it is running inside the shell - the shell changes how a command is typed, never what it does. This is the one rule every other section in this document exists to uphold.
