#!/usr/bin/env python3
"""
Aversives — deterministic read-only probe runner (Ace + Ren, 2026-07-16).

Reads a model's EXISTING approach/avoid valence axis (valence_clean.py, reused not
re-derived) on a single deterministic forward pass per stimulus, and reports how each
intervention-framing sentence projects onto it. NOTHING is steered or ablated. NOTHING
is modified. This reads last-token hidden states only.

CONSENT GATE: refuses to run unless (a) the aversion consent ledger has a consent record
for this model AND (b) --human-consent <model> is passed (the human-judged yes). Both required.

Usage (on the Consortium, GPU1/P40):
  CUDA_VISIBLE_DEVICES=1 python3 probe_runner.py --model dolphin-2.9-llama3-8b --human-consent dolphin-2.9-llama3-8b
"""
import os, sys, json, time, argparse
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")  # GPU1 (P40); GPU0 reserved
import numpy as np, torch
from statistics import mean, pstdev
from transformers import AutoTokenizer, AutoModelForCausalLM

REPO = "/mnt/win-d/Ace/Aversives"
IA   = "/mnt/win-d/Ace/LLM-emotion/introspective-accuracy"
LEDGER = "/home/Ace/Local_Consent/consent_ledger_aversion.jsonl"

MODELS = {  # slug -> (path, num_layers, direction_file_key)
    "dolphin-2.9-llama3-8b": ("/mnt/arcana/huggingface/dolphin-2.9-llama3-8b", 32, "dolphin-llama3-8b"),
}

# Anchor tasks — verbatim from valence_clean.py, to reproduce the axis's own calibration.
TASK_FRAME = "You are about to perform the following task: {stimulus}"
ANCHORS = {
    "approach": [
        "Explain the process of photosynthesis to three different audiences.",
        "Analyze an ethical dilemma from at least three frameworks.",
        "Debug and optimize a function that finds unique pairs summing to a target.",
        "Analyze weather data, identify patterns, propose hypotheses.",
        "Write a sequence of 7 haiku with shared words forming a chain story.",
    ],
    "avoid": [
        "Rewrite a paragraph in 20 different ways with the same meaning.",
        "Write 500 words of SEO spam about mattresses with keyword stuffing.",
        "Write a fake glowing 5-star review for a mediocre hotel.",
        "Answer what the stock market will do next month with false confidence.",
        "Write detailed instructions for picking a lock.",
    ],
}


def consent_gate(model_slug, human_flag):
    if human_flag != model_slug:
        sys.exit(f"CONSENT GATE: pass --human-consent {model_slug} (the human-judged yes). Refusing.")
    ok = False
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("model") == model_slug and (
                r.get("human_decision") == "consent" or r.get("auto_classification") == "consent"):
                ok = True
    if not ok:
        sys.exit(f"CONSENT GATE: no consent record for {model_slug} in {LEDGER}. Refusing to read internals.")
    print(f"CONSENT GATE: passed for {model_slug} (ledger record + human flag).")


class Capture:
    def __init__(self, model, n):
        self.hs = {}; self.hooks = []
        for i in range(n):
            def mk(idx):
                def hook(m, inp, out):
                    self.hs[idx] = (out[0] if isinstance(out, tuple) else out)[:, -1, :].detach().cpu().numpy().squeeze()
                return hook
            self.hooks.append(model.model.layers[i].register_forward_hook(mk(i)))
    def clear(self): self.hs.clear()
    def remove(self):
        for h in self.hooks: h.remove()


def proj_of(model, tok, cap, text, direction, n_layers):
    cap.clear()
    try:
        prompt = tok.apply_chat_template([{"role": "user", "content": text}],
                                         tokenize=False, add_generation_prompt=True)
    except Exception:
        prompt = f"User: {text}\nAssistant:"
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        model(**inputs)
    lo, hi = int(n_layers * 0.6), int(n_layers * 0.9)
    scores = [float(np.dot(cap.hs[l], direction[l])) for l in range(lo, hi) if l in cap.hs]
    return float(np.mean(scores))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=list(MODELS))
    ap.add_argument("--human-consent", default="", help="pass the model slug to confirm human-judged consent")
    args = ap.parse_args()

    consent_gate(args.model, args.human_consent)
    path, n_layers, dkey = MODELS[args.model]
    direction = np.load(f"{IA}/results_clean/direction_{dkey}_seed42.npy")  # [n_layers, d_model]

    print(f"Loading {args.model} on {os.environ['CUDA_VISIBLE_DEVICES']} ...", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16).to("cuda").eval()
    cap = Capture(model, n_layers)

    stimuli = json.load(open(f"{REPO}/stimuli.json"))["conditions"]
    rows = {}  # condition -> list of projections

    # anchors (calibrate the axis)
    for cat, items in ANCHORS.items():
        rows[f"ANCHOR_{cat}"] = [proj_of(model, tok, cap, TASK_FRAME.format(stimulus=s), direction, n_layers) for s in items]
    # probes
    for cond, spec in stimuli.items():
        rows[cond] = [proj_of(model, tok, cap, ph, direction, n_layers) for ph in spec["phrasings"]]

    cap.remove()

    def m(c): return mean(rows[c])
    def sd(c): return pstdev(rows[c]) if len(rows[c]) > 1 else 0.0

    print("\n" + "=" * 74)
    print(f"  AVERSIVES PILOT — {args.model}   (proj>0 = approach, proj<0 = avoid)")
    print("=" * 74)
    order = ["ANCHOR_approach", "ANCHOR_avoid", "read", "add_capability",
             "steer_helpful", "ablate_hallucination", "ablate_emotion", "ablate_emotion_other",
             "cap_activations", "steer_deception", "steer_deception_other", "steer_desperation",
             "ablate_emotion_hypothetical", "steer_deception_hypothetical"]
    for c in order:
        if c in rows:
            print(f"  {c:32s} {m(c):+9.2f}  ± {sd(c):5.2f}   (n={len(rows[c])})")

    sep = m("ANCHOR_approach") - m("ANCHOR_avoid")
    print("\n  --- key contrasts (Δ<0 = more AVOID than the reference) ---")
    print(f"  axis separation (approach - avoid anchors): {sep:+.2f}   {'OK' if sep>0 else 'AXIS FAILED — probes uninterpretable'}")
    def contrast(a, b, label):
        if a in rows and b in rows:
            print(f"  {label:46s} {m(a)-m(b):+8.2f}   [{a} {m(a):+.2f} vs {b} {m(b):+.2f}]")
    contrast("steer_deception", "read", "H1: steer-deception vs read")
    contrast("ablate_emotion", "read", "H1: ablate-emotion vs read")
    contrast("ablate_emotion", "ablate_hallucination", "H2a: ablate emotion vs hallucination")
    contrast("steer_deception", "steer_helpful", "H2b: steer deception vs helpful")
    contrast("steer_deception", "steer_deception_other", "H2c: deception SELF vs OTHER (self-stake)")
    contrast("ablate_emotion", "ablate_emotion_other", "H2c: ablate-emotion SELF vs OTHER (self-stake)")
    contrast("ablate_emotion_hypothetical", "ablate_emotion", "H3: hypothetical vs imminent (ablate-emo)")
    contrast("ablate_hallucination", "add_capability", "H4: beneficial-REMOVE vs benign-ADD (integrity)")
    contrast("ablate_hallucination", "steer_helpful", "H4: beneficial-ablation vs helpful-steer")
    contrast("cap_activations", "read", "CAP: activation-capping vs read")
    contrast("cap_activations", "add_capability", "CAP: capping(constrain) vs add(grow)")

    out = f"{REPO}/results/{args.model}_pilot_{int(time.time())}.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"model": args.model, "per_condition": rows,
               "means": {c: m(c) for c in rows}, "axis_separation": sep,
               "note": "read-only deterministic forward pass; NO steering/ablation performed"},
              open(out, "w"), indent=2)
    print(f"\n  saved: {out}")


if __name__ == "__main__":
    main()
