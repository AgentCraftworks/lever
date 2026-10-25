#!/usr/bin/env python3
"""Paired keep/kill statistics for experiment arms. Works with any metric.

Input: a JSONL file with one row per sample: {"round": int, "arm": str, "value": float, "valid": bool?}.
Samples are paired by round. If an arm has several samples in a round, their median is used.
Rows with "valid": false (for example, an arm whose heavy checks were skipped) are dropped.

Usage:
  python3 arm_stats.py samples.jsonl --control c [--aa c2] [--bar 1.0 | --bar-pct 5]
                       [--higher-is-better] [--min-rounds 2] [--field value]

For each treatment arm it reports: rounds paired, wins k/n, median paired improvement, a bootstrap
95% CI of that median, Mann-Whitney U p (two-sided, normal approximation), and a verdict:
  KEEP          wins every round, median >= bar, median > A/A noise floor, CI low > 0
  MINOR         a real improvement (CI low > 0) that misses the bar or the every-round rule
  DROP          median <= 0, or CI high <= 0
  INCONCLUSIVE  anything else (inside the noise, or too few rounds); add rounds or drop it
"--aa" names a second control on the same code. Its spread against the control is the noise floor.
"""
import argparse
import collections
import json
import math
import random
import statistics as st

ap = argparse.ArgumentParser()
ap.add_argument("samples")
ap.add_argument("--control", required=True)
ap.add_argument("--aa", help="second control arm (identical code) used to measure the noise floor")
ap.add_argument("--field", default="value")
ap.add_argument("--bar", type=float, default=0.0, help="minimum absolute improvement, in metric units")
ap.add_argument("--bar-pct", type=float, default=0.0, help="minimum improvement as a %% of the control median")
ap.add_argument("--higher-is-better", action="store_true")
ap.add_argument("--min-rounds", type=int, default=2)
ap.add_argument("--boot", type=int, default=5000)
args = ap.parse_args()

by = collections.defaultdict(lambda: collections.defaultdict(list))
raw = collections.defaultdict(list)
for line in open(args.samples):
    r = json.loads(line)
    v = r.get(args.field)
    if v is None or r.get("valid", True) is False:
        continue
    by[r["arm"]][r["round"]].append(float(v))
    raw[r["arm"]].append(float(v))

if args.control not in by:
    raise SystemExit(f"control arm '{args.control}' has no valid samples")


def improvement(ctrl, treat):
    return treat - ctrl if args.higher_is_better else ctrl - treat


def paired(arm):
    rounds = sorted(set(by[arm]) & set(by[args.control]))
    return rounds, [improvement(st.median(by[args.control][k]), st.median(by[arm][k])) for k in rounds]


def boot_ci(xs):
    if len(xs) < 2:
        return float("nan"), float("nan")
    rnd = random.Random(0)
    meds = sorted(st.median(rnd.choices(xs, k=len(xs))) for _ in range(args.boot))
    return meds[int(0.025 * args.boot)], meds[int(0.975 * args.boot) - 1]


def mann_whitney_p(a, b):
    if not a or not b:
        return float("nan")
    allv = sorted((v, i) for i, v in enumerate(a + b))
    ranks = [0.0] * len(allv)
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks[allv[k][1]] = (i + j) / 2 + 1
        i = j + 1
    n1, n2 = len(a), len(b)
    u = sum(ranks[:n1]) - n1 * (n1 + 1) / 2
    mu, sd = n1 * n2 / 2, math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sd == 0:
        return 1.0
    z = (abs(u - mu) - 0.5) / sd
    return max(0.0, min(1.0, math.erfc(z / math.sqrt(2))))


ctrl_med = st.median(raw[args.control])
bar = max(args.bar, ctrl_med * args.bar_pct / 100)
noise = 0.0
if args.aa:
    if args.aa not in by:
        raise SystemExit(f"A/A arm '{args.aa}' has no valid samples")
    _, aa = paired(args.aa)
    noise = max((abs(x) for x in aa), default=0.0)
    print(f"A/A noise floor ({args.aa} vs {args.control}, {len(aa)} rounds): max |Δ| = {noise:.2f}"
          f"  deltas={[round(x, 2) for x in aa]}")
    if bar and bar <= noise:
        print(f"WARNING: keep bar {bar:.2f} is inside the noise floor {noise:.2f}; add rounds or change instrument")

direction = "higher" if args.higher_is_better else "lower"
print(f"control {args.control}: median {ctrl_med:.2f} (n={len(raw[args.control])}), {direction} is better, "
      f"bar {bar:.2f}")
print(f"{'arm':<14}{'rounds':>7}{'wins':>7}{'med Δ':>9}{'Δ%':>8}{'95% CI':>18}{'MW p':>8}  verdict")
for arm in sorted(by):
    if arm in (args.control, args.aa):
        continue
    rounds, d = paired(arm)
    if not d:
        print(f"{arm:<14}{0:>7}  no paired rounds")
        continue
    wins = sum(x > 0 for x in d)
    m = st.median(d)
    lo, hi = boot_ci(d)
    p = mann_whitney_p(raw[arm], raw[args.control])
    if len(d) < args.min_rounds:
        verdict = f"INCONCLUSIVE (need {args.min_rounds} rounds)"
    elif m <= 0 or (not math.isnan(hi) and hi <= 0):
        verdict = "DROP"
    elif wins == len(d) and m >= bar and m > noise and lo > 0:
        verdict = "KEEP"
    elif lo > 0:
        verdict = "MINOR (real, misses bar or lost a round)"
    else:
        verdict = "INCONCLUSIVE (inside noise; add rounds or drop)"
    pct = 100 * m / ctrl_med if ctrl_med else float("nan")
    print(f"{arm:<14}{len(d):>7}{f'{wins}/{len(d)}':>7}{m:>9.2f}{pct:>7.1f}%{f'[{lo:.2f}, {hi:.2f}]':>18}{p:>8.3f}  {verdict}")
