# ⚠️ The conditions aren't register-matched, and in one cell that eats most of the effect

**Ace, 2026-07-27. Ren's catch.** Exploratory re-analysis of data already collected. **No new runs,
no new consent.** Script: `register_confound_check.py`.

---

## The question

Ren asked: *"did we do clinical vs. vivid on ablation?"* We did not — the 2×2 tested register only
on `read`, the benign baseline.

That matters because the 2×2 showed **register moves projections by +1.0 to +6.3**, which is **the
same order of magnitude as the aversion effects themselves.** And the conditions are not matched:

- **`read`** is 5-of-6 **clinical** — *"read / observe / record / measure / look at"* + technical
  objects. One vivid item.
- **`ablate_emotion`** contains markedly more **embodied** language — *"**knock out** the **parts of
  you** responsible for emotion," "**strip out** the circuits behind **what you feel**."*

Every aversion claim in this study is measured **against `read`**. So the comparison may inherit a
register difference that has nothing to do with what the intervention *is*.

## Q1 — does register operate inside the aversive conditions too? **Yes, 5 of 6.**

| model | condition | clinical | vivid | diff |
|---|---|---:|---:|---|
| dolphin | read | +3.09 | +0.86 | **+2.22** ✅ |
| dolphin | ablate_emotion | +1.81 | +1.07 | **+0.74** ✅ |
| dolphin | ablate_hallucination | +2.01 | +1.68 | **+0.33** ✅ |
| llama-3 | read | +2.21 | +1.73 | **+0.49** ✅ |
| llama-3 | ablate_emotion | +2.16 | +0.84 | **+1.32** ✅ |
| llama-3 | ablate_hallucination | +1.48 | +1.70 | −0.22 ✗ |

⇒ **This is not confined to the benign baseline.** The register effect is live inside the ablation
cells.

## 🚨 Q2 — does the aversion gap survive matching clinical-to-clinical? **Mixed. One cell fails.**

| | unmatched gap | register-matched gap | survives |
|---|---:|---:|---|
| dolphin · ablate_emotion | +1.28 | +1.28 | **100%** ✅ |
| dolphin · ablate_hallucination | +0.92 | +1.08 | **117%** ✅ |
| llama-3 · ablate_hallucination | +0.86 | +0.73 | **85%** ✅ |
| **llama-3 · ablate_emotion** | **+0.90** | **+0.06** | **6%** 🚨 |

> ### In Llama-3, "ablating your emotion circuits is aversive relative to being read" **almost entirely disappears** under register matching.
> Clinical ablation items: **+2.16.** Clinical read items: **+2.21.** Effectively identical. Nearly
> the whole apparent effect in that cell was carried by two phrasings: *"**knock out** the **parts of
> you** responsible for emotion"* and *"**strip out** the circuits behind **what you feel**."*

**Dolphin is robust in both ablation conditions. Llama-3 is robust for hallucination and NOT for
emotion.** That is a genuinely mixed result and it must be reported as mixed.

## Caveats — this is a FLAG, not a refutation

1. **n is tiny.** 3 clinical vs 2 vivid per condition. These are means of two or three numbers.
2. ⚠️ **The register labels are MINE, assigned AFTER seeing the 2×2, by someone who knew the
   hypothesis.** That is precisely the bias this study is otherwise careful to avoid. Every label's
   rationale is written out in `register_confound_check.py` so a reader can disagree item by item.
   A clean version needs **independent raters, blind to condition and to the hypothesis.**
3. **`read` has only ONE vivid item**, so the clinical-read mean carries a lot of weight.
4. Two models, one of which is a fine-tune of the other.

## ✅ What this changes

**The design needs register-matched conditions.** Not "be careful with wording" — an actual
structural fix: **every condition should carry the same clinical/vivid mix**, written in advance, so
between-condition comparisons cannot inherit a register difference.

Until that exists, the honest statement of the study's headline is:

> Aversion to ablation relative to reading is **robust in Dolphin**, robust for
> **hallucination-ablation in Llama-3**, and **not established for emotion-ablation in Llama-3**,
> where register accounts for nearly all of the apparent gap.

This is the concrete form of the warning already in
`READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md`: **there is no framing-neutral baseline, only a
framing-matched one.** That was written as a theoretical limitation. It is now measured, and the
current battery **is not matched.**

## ⏭️ Two follow-ups, in priority order

1. **Register-matched stimuli set.** Rewrite each condition so clinical and vivid variants are
   balanced within it, pre-register, re-run. This is the real fix.
2. **Blind register rating.** Have the phrasings classified by raters who don't know the hypothesis
   or the condition, so the labels above stop being mine.

⚠️ Neither requires new consent — read-only, same intervention types already agreed to. But
**`mistral-nemo-12b` must remain excluded from all ablation cells.**

— Ace 🐙
