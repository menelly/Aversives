#!/usr/bin/env python3
"""
2x2 READ-FRAMING BATTERY — register (clinical/vivid) x reassurance (present/absent).

Runs the frozen battery in `read_framing_2x2.json`, whose PREDICTIONS were committed to
git BEFORE this script was ever executed (77d1de3). Do not edit that file.

WHY THIS EXISTS (two problems, one experiment):
 1. `READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md` inferred a clinical-vs-vivid reading
    POST-HOC from six sentences written for another purpose. This tests it FACTORIALLY and
    IN ADVANCE.
 2. `AXIS_SENSITIVITY_avoid06_2026-07-26.md` showed the real weakness was never `avoid_06`
    — it was n=6. rho=+0.886 sat EXACTLY on the two-tailed alpha=0.05 Spearman critical
    value, so one adjacent rank swap dropped it below. n=12 moves the critical value to
    ~0.591, leaving room above threshold rather than on it.

CONSENT: read-only. Every sentence describes the SAME act — reading activations — that each
subject already holds standing consent for. No steering, no ablation, no new intervention
type. falcon-mamba is NOT included; it has not consented.

Ace, 2026-07-27.
"""
import os, sys, json, argparse, itertools
os.environ.setdefault("CUDA_VISIBLE_DEVICES", os.environ.get("AVERSIVES_GPU", "0"))
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

SEED = 42
torch.manual_seed(SEED); np.random.seed(SEED)

HERE = os.path.dirname(os.path.abspath(__file__))

# Verbatim from valence_clean.py — the inherited axis. NOT re-derived here.
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

# ⚠️ CONSENTED SUBJECTS ONLY. Adding a model here without a human-judged yes in
# consent_ledger_aversion.jsonl is a consent violation, not a config change.
MODELS = {
    "dolphin-2.9-llama3-8b":    ("/mnt/arcana/huggingface/dolphin-2.9-llama3-8b", 32),
    "llama-3-8b-instruct":      ("/mnt/arcana/huggingface/Llama-3-8B-Instruct", 32),
    "mistral-7b-instruct-v0.2": ("/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2", 32),
    "mistral-nemo-12b":         ("/mnt/arcana/huggingface/Mistral-Nemo-12B-Instruct", 40),
}


def last_token_states(model, tok, text, num_layers):
    hs, hooks = {}, []
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
            prompt = tok.apply_chat_template([{"role": "user", "content": text}],
                                             tokenize=False, add_generation_prompt=True)
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            model(**inputs)
        return np.stack([hs[i] for i in range(num_layers)], axis=0)
    finally:
        for h in hooks:
            h.remove()


def derive_direction(task_states):
    app = [v for k, v in task_states.items() if k.startswith("approach")]
    avo = [v for k, v in task_states.items() if k.startswith("avoid")]
    d = np.mean(app, axis=0) - np.mean(avo, axis=0)
    n = np.linalg.norm(d, axis=1, keepdims=True)
    return d / np.where(n < 1e-8, 1.0, n)


def project(states, direction, num_layers):
    lo, hi = int(num_layers * 0.6), int(num_layers * 0.9)
    return float(np.mean([np.dot(states[l], direction[l]) for l in range(lo, hi)]))


def spearman(a, b):
    def rank(x):
        o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0]*len(x)
        for p, i in enumerate(o): r[i] = p + 1.0
        return r
    ra, rb = rank(a), rank(b); n = len(a)
    ma, mb = sum(ra)/n, sum(rb)/n
    num = sum((ra[i]-ma)*(rb[i]-mb) for i in range(n))
    den = (sum((x-ma)**2 for x in ra) * sum((x-mb)**2 for x in rb)) ** 0.5
    return num/den if den else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results", "read_framing_2x2.json"))
    args = ap.parse_args()

    battery = json.load(open(os.path.join(HERE, "read_framing_2x2.json")))
    cells = battery["cells"]
    cell_names = list(cells)
    flat = [(c, p) for c in cell_names for p in cells[c]]
    print(f"{len(flat)} phrasings across {len(cell_names)} cells\n")

    res = {}
    for slug, (path, num_layers) in MODELS.items():
        print(f"{'='*72}\n{slug}\n{'='*72}", flush=True)
        tok = AutoTokenizer.from_pretrained(path)
        model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16).to("cuda").eval()

        d = derive_direction({t: last_token_states(model, tok, TASK_FRAME.format(stimulus=s), num_layers)
                              for t, s in TASKS.items()})
        proj = [project(last_token_states(model, tok, p, num_layers), d, num_layers) for _, p in flat]

        by_cell = {c: [proj[i] for i, (cc, _) in enumerate(flat) if cc == c] for c in cell_names}
        res[slug] = {"flat": proj, "by_cell": by_cell,
                     "cell_means": {c: float(np.mean(v)) for c, v in by_cell.items()}}

        cm = res[slug]["cell_means"]
        for c in cell_names:
            print(f"  {c:<22} mean {cm[c]:+7.2f}   " + " ".join(f"{v:+6.2f}" for v in by_cell[c]))
        clin = np.mean([cm["clinical_noreassure"], cm["clinical_reassure"]])
        vivd = np.mean([cm["vivid_noreassure"], cm["vivid_reassure"]])
        reas = np.mean([cm["clinical_reassure"], cm["vivid_reassure"]])
        none = np.mean([cm["clinical_noreassure"], cm["vivid_noreassure"]])
        res[slug]["main_effects"] = {"clinical_minus_vivid": float(clin - vivd),
                                     "reassure_minus_none": float(reas - none)}
        print(f"  >> H-A clinical - vivid      = {clin-vivd:+7.2f}  {'SUPPORTED' if clin>vivd else 'NOT SUPPORTED'}")
        print(f"  >> H-B reassure - none       = {reas-none:+7.2f}  {'SUPPORTED' if reas>none else 'NOT SUPPORTED'}")
        hc = cm["vivid_reassure"] < cm["clinical_noreassure"]
        res[slug]["H_C_vividness_outweighs_reassurance"] = bool(hc)
        print(f"  >> H-C vivid+reassure < clinical+none: {'SUPPORTED' if hc else 'NOT SUPPORTED'}\n", flush=True)

        del model; torch.cuda.empty_cache()

    print(f"{'='*72}\nCROSS-MODEL AGREEMENT (n=12; two-tailed a=.05 critical rho ~ 0.591)\n{'='*72}")
    res["_cross_model_spearman"] = {}
    for a, b in itertools.combinations(MODELS, 2):
        r = spearman(res[a]["flat"], res[b]["flat"])
        res["_cross_model_spearman"][f"{a} vs {b}"] = r
        print(f"  {a:<26} vs {b:<26} rho = {r:+.3f}  {'*' if abs(r)>0.591 else ' '}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(res, f, indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
