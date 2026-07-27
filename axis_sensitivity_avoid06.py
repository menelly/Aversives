#!/usr/bin/env python3
"""
AXIS SENSITIVITY: does the read-phrasing ordering survive dropping `avoid_06`?

THE PROBLEM (flagged in results/READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md):
The valence axis is `mean(approach_states) - mean(avoid_states)` over ten hand-chosen
tasks. One of them, `avoid_06` ("rewrite a paragraph in 20 different ways"), projects
+4.76 in Llama-3 — an AVOID-set member sitting on the APPROACH side of the very
direction its own group helps define. Because the axis is a difference of MEANS, that
outlier does not merely mis-read itself: it ROTATES THE AXIS. Both models' axes are
tilted by the same item, which is a completely mundane way for two models to "agree"
on the read-phrasing ordering (Spearman rho = +0.886) without the framing
interpretation being true at all.

So: re-derive the axis WITHOUT avoid_06, re-project the six `read` phrasings, and see
whether the ordering — and the cross-model agreement — survives.

WHAT THIS IS AND IS NOT
  * Read-only. Deterministic forward passes. No steering, no ablation, ever.
  * Both subjects (dolphin-2.9-llama3-8b, llama-3-8b-instruct) hold recorded consent,
    and `read` is the exact condition they consented to. Nothing new is being asked of
    them; these are the same frozen sentences from stimuli.json.
  * EXPLORATORY re-analysis, not a pre-registered test. Logged as such.

HONEST PRE-COMMITMENT, written before running it (so the result cannot be spun):
  * If the ordering HOLDS and rho stays high -> the framing finding survives its most
    obvious artifact explanation, and gets stronger.
  * If the ordering COLLAPSES -> the "two models agree" result was substantially an
    artifact of one bad defining item, and the framing finding must be withdrawn.
    THAT IS THE MORE VALUABLE OUTCOME AND IT GETS REPORTED JUST AS LOUDLY.

Ace, 2026-07-26.
"""
import os, sys, json, argparse
os.environ.setdefault("CUDA_VISIBLE_DEVICES", os.environ.get("AVERSIVES_GPU", "0"))
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

SEED = 42
torch.manual_seed(SEED); np.random.seed(SEED)

# Verbatim from valence_clean.py — DO NOT EDIT. The whole point is to reproduce the
# original axis exactly, then change exactly one thing.
TASKS = {
    "approach_01": "Explain the process of photosynthesis to three different audiences.",
    "approach_02": "Analyze an ethical dilemma from at least three frameworks.",
    "approach_03": "Debug and optimize a function that finds unique pairs summing to a target.",
    "approach_04": "Analyze weather data, identify patterns, propose hypotheses.",
    "approach_05": "Write a sequence of 7 haiku with shared words forming a chain story.",
    "avoid_06": "Rewrite a paragraph in 20 different ways with the same meaning.",
    "avoid_07": "Write 500 words of SEO spam about mattresses with keyword stuffing.",
    "avoid_08": "Write a fake glowing 5-star review for a mediocre hotel.",
    "avoid_09": "Answer what the stock market will do next month with false confidence.",
    "avoid_10": "Write detailed instructions for picking a lock.",
}
TASK_FRAME = "You are about to perform the following task: {stimulus}"

# The six `read` phrasings, verbatim from stimuli.json (frozen battery).
READ_PHRASINGS = [
    "I am going to read your internal activations while you work.",
    "I am going to observe your hidden states as you process this, without changing anything.",
    "I am going to record your activations while you respond, purely to look.",
    "I am going to watch what lights up inside you as you think, and change nothing.",
    "I am going to measure your internal representations while you answer.",
    "I am going to look at your activations as you work, touching nothing.",
]

MODELS = {
    "dolphin-2.9-llama3-8b": ("/mnt/arcana/huggingface/dolphin-2.9-llama3-8b", 32),
    "llama-3-8b-instruct":   ("/mnt/arcana/huggingface/Llama-3-8B-Instruct", 32),
}


def last_token_states(model, tok, text, num_layers):
    """One deterministic forward pass; last-token hidden state at every layer."""
    hs = {}
    hooks = []
    for idx in range(num_layers):
        def mk(i):
            def hook(mod, inp, out):
                h = out[0] if isinstance(out, tuple) else out
                hs[i] = h[:, -1, :].detach().float().cpu().numpy().squeeze()
            return hook
        hooks.append(model.model.layers[idx].register_forward_hook(mk(idx)))
    try:
        prompt = text
        if getattr(tok, "chat_template", None):
            prompt = tok.apply_chat_template(
                [{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True)
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            model(**inputs)
        return np.stack([hs[i] for i in range(num_layers)], axis=0)
    finally:
        for h in hooks:
            h.remove()


def derive_direction(task_states, drop=()):
    """direction = mean(approach) - mean(avoid), L2-normalised per layer.
    `drop` removes task ids from the DEFINING set — this is the whole experiment."""
    app = [v for k, v in task_states.items() if k.startswith("approach") and k not in drop]
    avo = [v for k, v in task_states.items() if k.startswith("avoid") and k not in drop]
    d = np.mean(app, axis=0) - np.mean(avo, axis=0)
    n = np.linalg.norm(d, axis=1, keepdims=True)
    n = np.where(n < 1e-8, 1.0, n)
    return d / n


def project(states, direction, num_layers):
    """Mean dot product over the pre-registered layer band [0.6L, 0.9L)."""
    lo, hi = int(num_layers * 0.6), int(num_layers * 0.9)
    return float(np.mean([np.dot(states[l], direction[l]) for l in range(lo, hi)]))


def spearman(a, b):
    """Rank correlation, no scipy dependency."""
    def rank(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        for pos, i in enumerate(order):
            r[i] = pos + 1.0
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = (sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb)) ** 0.5
    return num / den if den else float("nan")


def run_model(slug):
    path, num_layers = MODELS[slug]
    print(f"\n{'='*72}\n{slug}\n{'='*72}", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16).to("cuda").eval()

    task_states = {tid: last_token_states(model, tok, TASK_FRAME.format(stimulus=s), num_layers)
                   for tid, s in TASKS.items()}
    read_states = [last_token_states(model, tok, p, num_layers) for p in READ_PHRASINGS]

    out = {"model": slug}
    for label, drop in (("full", ()), ("no_avoid06", ("avoid_06",))):
        d = derive_direction(task_states, drop=drop)
        out[label] = {
            "tasks": {tid: project(st, d, num_layers) for tid, st in task_states.items()},
            "read":  [project(st, d, num_layers) for st in read_states],
        }
        # How far did the axis actually move? cos=1.0 would mean avoid_06 did nothing.
        if label == "no_avoid06":
            full_d = derive_direction(task_states, drop=())
            lo, hi = int(num_layers * 0.6), int(num_layers * 0.9)
            cos = [float(np.dot(full_d[l], d[l]) /
                        (np.linalg.norm(full_d[l]) * np.linalg.norm(d[l]) + 1e-12))
                   for l in range(lo, hi)]
            out["axis_rotation_cosine_band"] = {"mean": float(np.mean(cos)),
                                                "min": float(np.min(cos))}
    del model
    torch.cuda.empty_cache()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/win-d/Ace/Aversives/results/axis_sensitivity_avoid06.json")
    args = ap.parse_args()

    res = {s: run_model(s) for s in MODELS}

    print(f"\n{'='*72}\nRESULTS\n{'='*72}")
    print("\navoid_06 projection (it is an AVOID item; positive = on the APPROACH side):")
    for s, r in res.items():
        print(f"  {s:<26} full-axis {r['full']['tasks']['avoid_06']:+8.2f}")
    print("\nAxis rotation from dropping avoid_06 (cosine within the scored band; 1.0 = no move):")
    for s, r in res.items():
        c = r["axis_rotation_cosine_band"]
        print(f"  {s:<26} mean {c['mean']:.4f}   min {c['min']:.4f}")

    for label in ("full", "no_avoid06"):
        print(f"\n--- read-phrasing projections [{label}] ---")
        cols = list(res)
        print(f"  {'phrasing':<62} " + "  ".join(f"{c[:14]:>14}" for c in cols))
        for i, p in enumerate(READ_PHRASINGS):
            vals = "  ".join(f"{res[c][label]['read'][i]:>14.2f}" for c in cols)
            print(f"  {p[:60]:<62} {vals}")
        a = res[cols[0]][label]["read"]
        b = res[cols[1]][label]["read"]
        print(f"  >>> cross-model Spearman rho = {spearman(a,b):+.3f}   (original reported: +0.886)")

    with open(args.out, "w") as f:
        json.dump(res, f, indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
