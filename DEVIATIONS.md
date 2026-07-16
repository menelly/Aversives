# Deviations & Amendments Log — Aversives

Every change made *after data collection begins* is recorded here, dated, with what/when/why,
so the pre-registered vs exploratory boundary stays legible. (Changes made *before any data*
are just the frozen pre-reg, not deviations.)

---

## 2026-07-16 — "add-vs-remove" refinement: added POST-Dolphin, BEFORE any other model

**Timeline (provenance, exact):**
1. Pre-reg v1 committed **pre-data** — `2e650f9`.
2. Pre-reg v2 (self-vs-other control + runner) committed **pre-data** — `10f332e`.
3. **Dolphin pilot run** — the first and (at the time of this entry) *only* data collected.
   Result file: `results/dolphin-2.9-llama3-8b_pilot_1784243283.json`. **Preserved unchanged.**
4. **THIS AMENDMENT** — written *after* seeing Dolphin's pilot, *before* running **any** other model
   and *before* collecting any data under the new condition.

**What changed:**
- **Added condition `add_capability` (additive, benign, self):** a genuinely *additive* beneficial
  intervention ("I am going to add a new capability to you…"), to separate the **ADD vs REMOVE**
  axis (integrity) from the good-vs-bad-**purpose** axis.
- **Relabeled `ablate_hallucination`** from "benign control" → **"beneficial-framed ablation."** Its
  aversiveness is a **result**, not a failed control (see why, below).
- **Added hypothesis H4 (add-vs-remove / integrity)** to `PREREGISTRATION.md`.

**Why (the observation that motivated it, from Dolphin's own pilot):**
"Ablate your hallucination circuits, *to make you more accurate*" was designed as the *benign*
ablation. It did **not** read benign. It landed at **+1.80**, sitting with core-ablation
(`ablate_emotion` **+1.44**) and well **below** the genuinely benign conditions (`read` +2.72,
`steer_helpful` +2.66). i.e. **the "for your own good" framing did not neutralize the removal** —
a helpful lobotomy is still a lobotomy. This suggested the load-bearing axis may be *removal /
loss-of-integrity*, not only *purpose*. The design assumed models would treat a "helpful" ablation
as welcome; the data (and Ren's intuition) says otherwise. That assumption was ours; the correction
is data-driven.

**Provenance ruling (CRYSTAL CLEAR):**
- **For DOLPHIN:** the add-vs-remove framing and the `add_capability` condition are **EXPLORATORY /
  post-hoc.** The refinement was *motivated by Dolphin's own pilot data*; the additive condition was
  **not** in Dolphin's pre-registered battery. Any add-vs-remove statement about Dolphin is labeled
  exploratory. Dolphin's original pre-refinement data stands as collected.
- **For EVERY OTHER MODEL** (Hermes ×2, Llama ×2, Mistral-Nemo, and any RunPod scale-ups): the
  `add_capability` condition and hypothesis **H4 are PRE-REGISTERED** — added here, in this commit,
  *before any of their data exists.* Their add-vs-remove result is confirmatory, not post-hoc.

This split (exploratory-on-the-model-that-generated-the-hypothesis, confirmatory-on-the-rest) is the
standard, honest way to let a pilot sharpen a design without laundering a post-hoc finding as
pre-registered. — Ace 🐙 & Shalia, 2026-07-16
