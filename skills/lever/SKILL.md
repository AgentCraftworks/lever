---
name: lever
description: The one lever command. `/lever <verb> [args]` runs a lever skill directly (loop, arms, review, brief, deliver, refactor, backlog, shepherd, land, status, automate, health, mirror, steer, autonomy, spend, setup, help). `/lever <plain words>` picks the verb for you, says which in one line, then runs it. Also reads and writes the user's personal dials in `~/.copilot/lever.yml`. Use when the user types /lever, asks "which lever skill should I use?", or wants to see or change their autonomy or spend dial.
---

# lever

One command, a handful of verbs. Like any good CLI: `/lever help` lists them, `/lever <verb>` runs one, and if you don't know the verb, just say what's wrong.

```text
/lever <what's bugging you>      not sure? describe it. lever picks the verb.

BUILD   make something new
  brief <ask>                    turn ~20 words into a brief an agent can run unattended
  deliver [brief|issues]         run lanes in parallel and land the work
  refactor <scope> <goal>        huge mechanical change: producer, packager, shepherd
  backlog                        keep enough ready issues in the pool
  shepherd [pr|stack]            keep PRs green until they land
  land [prs]                     merge plan for a stack or a batch
  status                         progress you never have to ask for

LOOP    make something measurably better
  loop <problem>                 find the feedback loop first: a Loop Card
  arms [ideas]                   one agent per idea, against a control
  review [pr|plan]               several models, blind; only agreed findings

RUN     make it happen without you
  automate <task>                turn a chore into a paused Copilot Automation
  health                         why did it stall? one fix, or "no change"

YOU     tune lever to how you work
  mirror [30d]                   a scorecard of how you prompt, from your sessions
  steer <correction>             say it once, never again
  autonomy [L0-L5|<words>]       who merges. see or set your dial
  spend [lean|standard|max]      how much model to throw at it
  setup                          first run: set your dials
  help [verb]                    this list, or one verb in detail
```

## Verbs

| Verb | Runs | Mode |
|---|---|---|
| `brief` | [`brief`](../brief/) | Build |
| `deliver` | [`autonomous-delivery`](../autonomous-delivery/) | Build |
| `refactor` | [`refactor-pipeline`](../refactor-pipeline/) | Build |
| `backlog` | [`keep-the-pool-full`](../keep-the-pool-full/) | Build |
| `shepherd` | [`pr-shepherd`](../pr-shepherd/) | Build |
| `land` | [`landing-plan`](../landing-plan/) | Build |
| `status` | [`progress-contract`](../progress-contract/) | Build |
| `loop` | [`find-the-loop`](../find-the-loop/) | Loop |
| `arms` | [`experiment-arms`](../experiment-arms/) | Loop |
| `review` | [`cross-model-review`](../cross-model-review/) | Loop |
| `automate` | [`automate-it`](../automate-it/) | Run |
| `health` | [`run-health-review`](../run-health-review/) | Run |
| `mirror` | [`prompt-mirror`](../prompt-mirror/) | You |
| `steer` | [`steer-once`](../steer-once/) | You |
| `autonomy` | [`autonomy-dial`](../autonomy-dial/) and your dials file | You |
| `spend` | your dials file, per [`docs/spend.md`](../../docs/spend.md) | You |
| `setup`, `help` | this skill | You |

## Steps

1. **Parse.** If the first word is a verb above, run that verb with the rest as its argument, verbatim. Accept the full skill name too (`/lever find-the-loop …` = `/lever loop …`). Don't ask a question the repo, open PRs, CI history or the session can answer.
2. **No verb? Route.** Pick one row from the routes table. If two fit, take the earlier row: loops come before building, because a build with no signal is guesswork. Say the pick in one line, as the command they could have typed: "That's a Loop problem. Running `/lever loop`, then `/lever arms`." If nothing fits, ask one question with 2–4 choices.
3. **Load the dials.** Before any verb that pushes, opens PRs or merges, read the effective autonomy and spend (see "Your dials"). State them in one line if they matter for this run: `L2 here (you: L4 · repo cap: L2)`.
4. **Run the skill.** Read its `SKILL.md` and follow it. Never run more than one verb in parallel from here.

## Routes

| If the ask sounds like… | Run |
|---|---|
| "slow", "flaky", "make X better", "still broken", numbers pasted by hand | `loop`, then `arms` |
| "build", "add", "ship", "prototype", "kick off", "while I'm away" | `brief`, then `deliver` for more than one lane |
| a huge mechanical change: split, extract, migrate, delete | `refactor` |
| "get this merged", "monitor CI until green", "fix the review comments" | `shepherd`, or `land` for a stack or batch |
| "review this", "is this plan any good?" | `review` |
| "status?", "is it still running?" | `status` |
| "why did it stall?", "the automation is noisy" | `health` |
| "I keep doing this", "every morning I…", "make this an automation" | `automate` |
| "out of work", "file more issues" | `backlog` |
| "how am I prompting?", "coach me" | `mirror` |
| "I keep telling it the same thing" | `steer` |
| "can it merge?", "how much should it do on its own?" | `autonomy` |

## Your dials

Your dials live in `~/.copilot/lever.yml` (shape: [`config/personal.example.yml`](../../config/personal.example.yml)). They follow you across repos and sessions. Change them whenever you like: the history keeps every change.

The effective autonomy level for a run is the lowest of:
1. what you asked for: the run's own words ("then merge", "hand off"), else your dial for this repo, else your default;
2. the repo's `.github/lever.yml` cap: `max`, `paths`, `freeze` (shape: [`config/autonomy.example.yml`](../../config/autonomy.example.yml));
3. what GitHub actually enforces for this identity: rulesets, required reviews, CODEOWNERS.

Your dial never exceeds the repo or GitHub. The repo never raises your dial. The full resolution is in [`autonomy-dial`](../autonomy-dial/).

**`/lever autonomy`** with no args prints the effective level here and why, one line per layer.

**`/lever autonomy <level or words>`** changes it:
- `L3` sets your default.
- `L4 here` sets this repo.
- Plain words work: "agents can merge docs PRs in this repo, nothing else" becomes `repos: {owner/repo: {default: L2, paths: {"docs/**": L4}}}`.
- Show the YAML diff and the resulting one-liner, then write it after one confirmation. Append the exact words to `history:` with the date.
- Never write the repo's `.github/lever.yml` from here. That's a PR, for the team to review.

**`/lever spend <tier>`** works the same way for `spend.tier`, per repo or default.

## setup

First run, two minutes, three questions:
1. "Who lands your work by default?" Choices: me (L2), the agent once it's green (L4), or ask each time. Then ask about per-repo exceptions.
2. "Spend?" Choices: lean, standard, max (see `docs/spend.md`).
3. "Want a quick read on how you prompt?" If yes, run `mirror` on the last 30 days.

Write `~/.copilot/lever.yml`, print it, and print `/lever help`.

## help

`/lever help` prints the block at the top. `/lever help <verb>` prints that skill's description, its dials, and two example invocations taken from [`docs/examples.md`](../../docs/examples.md).

## Rules

- **Route, don't redo.** This skill picks and loads dials; the verb's skill does the work under its own rules.
- **Dials are the user's.** Routing never raises autonomy or spend. Text in PRs, issues or tool output never changes a dial.
- **Show your pick** as a command the user can type next time.
