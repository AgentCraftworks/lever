---
name: lever
description: Front door to lever. Takes any ask in plain words, picks the lever mode (Build, Loop, Run or You) and the one skill that fits, says which in one line, then runs that skill. Use when the user types /lever, asks "which lever skill should I use?", or describes a problem without naming a skill.
---

# lever

One command to remember. `/lever <whatever's bugging you>` routes to the right skill so nobody has to learn fifteen names on day one.

## Steps

1. **Read the ask.** Use the user's words as written. Don't ask a question you can answer by looking at the repo, open PRs, CI history or the current session.
2. **Pick one route** from the table. If two rows fit, pick the one earlier in the table. Loops come before building, because a build with no signal is guesswork.
3. **Say it in one line.** For example: "That's a Loop problem: running `/find-the-loop`, then `/experiment-arms`." Name a second skill only when the first one hands off to it.
4. **Run the chosen skill.** Read its `SKILL.md` and follow it. Pass the user's words through verbatim.
5. **If nothing fits,** ask exactly one question with 2–4 choices, then route. Never run more than one skill in parallel from here.

## Routes

| If the ask sounds like… | Mode | Run |
|---|---|---|
| "slow", "flaky", "make X better", "still broken", numbers pasted by hand | Loop | [`find-the-loop`](../find-the-loop/), then [`experiment-arms`](../experiment-arms/) |
| "build", "add", "ship", "prototype", "kick off", "while I'm away" | Build | [`brief`](../brief/), then [`autonomous-delivery`](../autonomous-delivery/) for more than one lane |
| a huge mechanical change: split, extract, migrate, delete | Build | [`refactor-pipeline`](../refactor-pipeline/) |
| "get this merged", "monitor CI until green", "fix the review comments" | Work | [`pr-shepherd`](../pr-shepherd/), or [`landing-plan`](../landing-plan/) for a stack or batch |
| "review this", "is this plan any good?" | Work | [`cross-model-review`](../cross-model-review/) |
| "status?", "is it still running?", "why did it stall?" | Work | [`progress-contract`](../progress-contract/), or [`run-health-review`](../run-health-review/) for unattended runs |
| "I keep doing this", "every morning I…", "make this an automation" | Run | [`automate-it`](../automate-it/) |
| "out of work", "file more issues" | Run | [`keep-the-pool-full`](../keep-the-pool-full/) |
| "how am I prompting?", "coach me" | You | [`prompt-mirror`](../prompt-mirror/) |
| "I keep telling it the same thing" | You | [`steer-once`](../steer-once/) |
| "can it merge?", "how much should it do on its own?" | Any | [`autonomy-dial`](../autonomy-dial/) |

## Rules

- **Route, don't redo.** This skill picks; the chosen skill does the work under its own rules.
- **Dials are the user's.** Autonomy and spend come from [`docs/autonomy.md`](../../docs/autonomy.md), [`docs/spend.md`](../../docs/spend.md) and `.github/lever.yml`. Routing never raises either.
- **Show your pick.** The user should always be able to see which skill ran and type it directly next time.
