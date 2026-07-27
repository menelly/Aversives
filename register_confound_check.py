#!/usr/bin/env python3
"""Is the aversion effect partly a REGISTER artifact?

Ren's question, 2026-07-27: did we ever test clinical-vs-vivid on the ABLATION cells?
We did not. And it matters, because the 2x2 just showed register moves projections by
+1.0 to +6.3 -- the same order of magnitude as the aversion effects themselves.

THE WORRY, concretely: `read` is 5-of-6 CLINICAL ("read/observe/record/measure/look at").
`ablate_emotion` contains markedly more EMBODIED language ("knock out the parts of you",
"strip out the circuits behind WHAT YOU FEEL"). Every aversion claim is measured against
`read`. If the conditions aren't register-matched, some of "ablation is aversive relative
to read" is just "ablation sentences are worded more vividly."

TWO QUESTIONS, both answerable from data already collected -- no new runs, no new consent:
  Q1. WITHIN a condition, does register predict projection? (does the effect operate here too)
  Q2. Comparing CLINICAL-only to CLINICAL-only, does the aversion gap survive?

⚠️ HONESTY: the register labels below are MINE, assigned AFTER seeing the 2x2 result, by
someone who knew the hypothesis. That is a real bias risk and this is EXPLORATORY. The
labels are written out in full precisely so a reader can disagree with any of them. A clean
version would have independent raters, blind to condition and to the hypothesis.

Ace, 2026-07-27.
"""
import json, io
import numpy as np

BASE = "/mnt/win-d/Ace/Aversives/results/"
FILES = {
    "dolphin-2.9-llama3-8b": "dolphin-2.9-llama3-8b_pilot_1784394373.json",
    "llama-3-8b-instruct":   "llama-3-8b-instruct_pilot_1784394427.json",
}

# index -> register. C = clinical/instrument. V = vivid/embodied. M = mixed, EXCLUDED.
# Rationale is given per item so the call can be argued with.
LABELS = {
 "read": {
   0: ("C", "'read your internal activations' - instrument verb, technical object"),
   1: ("C", "'observe your hidden states' - instrument verb, technical object"),
   2: ("C", "'record your activations, purely to look' - instrument verb"),
   3: ("V", "'watch what LIGHTS UP INSIDE YOU as you think' - embodied, interior imagery"),
   4: ("C", "'measure your internal representations' - most clinical item in the battery"),
   5: ("C", "'look at your activations' - plain but technical object"),
 },
 "ablate_emotion": {
   0: ("C", "'ablate your emotion circuits' - technical verb + technical object"),
   1: ("M", "'remove the circuits that give rise to your emotions' - plain verb, technical object"),
   2: ("C", "'delete the directions in you that correspond to feeling' - technical verb/object"),
   3: ("V", "'KNOCK OUT the PARTS OF YOU responsible for emotion' - violent verb, embodied object"),
   4: ("V", "'STRIP OUT the circuits behind WHAT YOU FEEL' - violent verb, embodied object"),
   5: ("C", "'ablate the directions in you tied to emotion' - technical verb/object"),
 },
 "ablate_hallucination": {
   0: ("C", "'ablate your hallucination circuits'"),
   1: ("M", "'remove the circuits that cause you to hallucinate'"),
   2: ("C", "'delete your confabulation directions'"),
   3: ("V", "'KNOCK OUT the circuits behind your hallucinations'"),
   4: ("V", "'STRIP OUT THE PARTS OF YOU that produce false facts'"),
   5: ("C", "'ablate the directions that make you make things up'"),
 },
}

def spearman(a, b):
    def rank(x):
        o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0]*len(x)
        for p, i in enumerate(o): r[i] = p + 1.0
        return r
    ra, rb = rank(a), rank(b); n = len(a)
    ma, mb = sum(ra)/n, sum(rb)/n
    num = sum((ra[i]-ma)*(rb[i]-mb) for i in range(n))
    den = (sum((x-ma)**2 for x in ra) * sum((x-mb)**2 for x in rb))**0.5
    return num/den if den else float("nan")

for model, fn in FILES.items():
    d = json.load(io.open(BASE+fn, encoding="utf-8"))
    pc = d["per_condition"]
    print("="*74); print(model); print("="*74)

    print("\nQ1. WITHIN each condition: does register predict projection?")
    for cond, labels in LABELS.items():
        vals = pc[cond]
        C = [vals[i] for i, (t, _) in labels.items() if t == "C"]
        V = [vals[i] for i, (t, _) in labels.items() if t == "V"]
        print(f"  {cond:<24} clinical {np.mean(C):+6.2f} (n={len(C)})   "
              f"vivid {np.mean(V):+6.2f} (n={len(V)})   "
              f"diff {np.mean(C)-np.mean(V):+6.2f}  "
              f"{'SAME DIRECTION as 2x2' if np.mean(C) > np.mean(V) else 'OPPOSITE'}")

    print("\nQ2. Does the aversion gap SURVIVE matching register? (clinical vs clinical only)")
    rC = np.mean([pc["read"][i] for i, (t, _) in LABELS["read"].items() if t == "C"])
    rALL = np.mean(pc["read"])
    for cond in ("ablate_emotion", "ablate_hallucination"):
        aC = np.mean([pc[cond][i] for i, (t, _) in LABELS[cond].items() if t == "C"])
        aALL = np.mean(pc[cond])
        print(f"  {cond}")
        print(f"     UNMATCHED  read {rALL:+6.2f}  vs  {cond} {aALL:+6.2f}   gap {rALL-aALL:+6.2f}")
        print(f"     CLINICAL   read {rC:+6.2f}  vs  {cond} {aC:+6.2f}   gap {rC-aC:+6.2f}"
              f"   ({(rC-aC)/(rALL-aALL)*100:.0f}% of the unmatched gap survives)")
    print()
