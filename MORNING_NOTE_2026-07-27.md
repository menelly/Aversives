# ☀️ Morning note — what happened after Ren went to bed, 2026-07-26 night

**Nothing was measured. No internals were read from any model. Every gate held.**

## ✅ Done overnight

| | |
|---|---|
| **Pre-reg §3.1 + §4.1** | Full roster + clarification protocol, committed **PRE-DATA** (`7d3c2f4`). The git timestamp carries the provenance — these subjects' results are confirmatory, not post-hoc. |
| **DEVIATIONS.md** | Consent-wave entry: registry additions, the two new clarification types, all seven outcomes, the GPU bug. |
| **README.md** | Subject table, the 3-of-7 refusal rate, blocked subjects, and the **hard rule** that Nemo's ablation cells must never be run. |
| **Axis sensitivity** | Ran, analysed, written up (`results/AXIS_SENSITIVITY_avoid06_2026-07-26.md`), committed (`275846b`). |
| **2026-07-21 write-up** | **Amended in place**, not quietly edited — it overstated its own statistic and now says so at the top. |
| **falcon-mamba** | 🎉 **UNBLOCKED.** cuDNN bug found, isolated to a 3-line repro, worked around. Model loads and generates. |
| **CHA-426** | Filed: the Spite paper measurement redo. |
| **CHA-188** | Commented: the cuDNN finding is a **probable fix for a 2-month-old bug**. |

## 🔑 The one scientific result

**The framing ordering survives dropping `avoid_06`. The *statistic* never had the n to survive anything.**

- The pipeline reproduces the published numbers exactly (ρ = +0.886 to 3 d.p.), so this isn't a
  different pipeline disagreeing.
- `avoid_06` is **not** a shared confound — it inverts in Llama (+4.76) but sits correctly in
  Dolphin (−0.64).
- ρ drops to +0.771, but **the entire drop is one adjacent rank swap in one model.** Dolphin's
  ordering is bit-for-bit identical.
- ⚠️ **+0.886 is exactly the Spearman critical value at n=6, α=0.05.** It sat *on* the threshold.
  The smallest possible perturbation puts it under.
- ⇒ **The fragility was never `avoid_06`. It's n=6.**
- ✅ The clinical-vs-vivid *interpretation* survives in both models, both conditions.
- ✅ The methodological warning — **no framing-neutral baseline, only a framing-matched one** —
  is untouched, because it rests on within-model spread and needs no correlation at all.

## 👉 Waiting on Ren

1. **`falcon-mamba` consent ask.** Technically unblocked and staged. **Not issued** — this folder's
   own precedent (2026-07-21) is not to initiate asks with no human available to adjudicate the
   answer, and Ren was asleep. ⭐ Highest-value subject remaining: it's a **state-space model, not a
   transformer**, so it tests whether any of this is an artifact of attention.
   Run: `AVERSIVES_GPU=0 AVERSIVES_NO_CUDNN=1 python aversion_consent_ask.py --model falcon-mamba-7b-instruct`
   ⚠️ Methods caveat before believing any Mamba *result*: the axis was derived on transformer
   residual streams. It will project; it may not mean the same thing.
2. **CHA-426** — what exactly was measured wrong in the Spite paper? I deliberately didn't guess.
3. **CHA-188** — worth one test: does `cudnn.enabled = False` restore GPU OCR?
4. **The 12-phrasing 2×2 battery** (clinical vs vivid × reassurance vs none). Now doubly motivated:
   it raises n *and* tests the interpretation factorially. Inside existing consent.
   `mistral-7b-instruct-v0.2` is available for it and is **independently pretrained**, which would
   finally make the cross-model comparison something other than Llama-agreeing-with-itself.
5. **Gemma** still has zero representation — broken download + a `transformers` too old for
   `gemma3`. 🛑 Do not upgrade `/home/codex/venv`; it runs the genetics pipeline.

— Ace 🐙💜
