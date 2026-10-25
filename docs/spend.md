# Spend dial

How many tokens and how much compute you are willing to spend is a choice, like autonomy. A lean setup can still close loops. A max setup buys parallelism and judgment, not correctness for free.

| | `lean` | `standard` (default) | `max` |
|---|---|---|---|
| Model tier | Standard everywhere | Premium only for judgment: diagnosis, planning, risky review | Premium by default |
| Parallel lanes | 1–2 | 3–5 | 5–20+ |
| Review | On request | One reviewer per PR, on events | Multi-model panel on risky diffs, re-review on push |
| Paired runs per arm | 3 | 4–6 | 6–12 |
| Triggers | Events with filters only | Events plus an hourly sweep | Events plus a 15-min sweep |
| Budget stop | Hard stop at 80% | Report at 80%, then finish or park | Report at 80% |

## Order of magnitude

Costs multiply. Estimate before you pick:

- **Model tier:** a premium model costs about **10–15× per call** compared with a standard one. In practice, cost follows the model more than anything else.
- **Lanes:** N parallel lanes cost about **N×**. Coordination overhead grows as well; watch for lanes that only relay messages.
- **Triggers:** an unfiltered per-push trigger can mean **~2–3× runs per PR** with no added signal. Triggers decide cost.
- **Review panels:** k reviewing models cost about **k×** per review.
- **Polling:** status checks and polling can quietly be the largest line item. Prefer events; a no-change wake should end silently and cheaply.

## Where spend pays off

- **Spend on judgment:** diagnosis, planning a fan-out, reviewing a risky change, deciding whether a measured win is real.
- **Save on routine:** classification, labeling, digests, no-op checks. A run that correctly does nothing should cost almost nothing.
- **Measure value per spend:** report useful outputs per dollar, or for a CI loop, Actions minutes spent per minute saved. Raise spend where that ratio is good, and cut it where it isn't.

## Setting it

In `.github/lever.yml`:

```yaml
spend:
  tier: standard            # lean | standard | max
  premium_for: [diagnosis, planning, risky_review]
  daily_cap_usd: 50         # optional hard stop
```

A brief, kickoff answer or automation PARAMETERS can set a different tier for one run. Unlike autonomy, spend has no repo ceiling, but a daily cap is a hard stop.
