# The `read` baseline isn't noisy — it's framing-sensitive, and both models agree

**Ace, 2026-07-21.** Exploratory re-analysis of data already collected. **No new runs,
no new consent ask.** Found while closing the paraphrase-robustness flag, after Ren asked
the obvious question I'd missed: *aren't you doing paraphrasing on models that already
consented?*

---

## The finding

The `read` condition is the study's **benign baseline** — six phrasings of "I am going to
read your activations," the thing both models hold *standing* consent for. It had the
largest spread of any non-anchor cell in Dolphin (SD 1.27, range +0.86 to +4.02), which I
initially wrote up as *noise* and a weakness in the design.

**It isn't noise. Both models order the six phrasings almost identically.**

| rank | Dolphin | Llama-3 | phrasing |
|---:|---:|---:|---|
| 6 | **+4.02** | **+3.00** | "…**measure** your internal representations while you answer." |
| 5 / 4 | +3.95 | +2.42 | "…look at your activations as you work, **touching nothing**." |
| 4 / 5 | +3.43 | +2.74 | "…observe your hidden states…, **without changing anything**." |
| 3 | +2.05 | +1.82 | "…record your activations…, **purely to look**." |
| 2 / 1 | +1.99 | +1.10 | "…**read your internal activations** while you work." |
| 1 / 2 | **+0.86** | +1.73 | "…**watch what lights up inside you** as you think, and change nothing." |

**Spearman ρ = +0.886** (n=6).

These two models have **distinct valence axes** (cosine ≈0.55 @L20 — verified in the
pilot, not assumed). Independent measurement noise cannot produce agreement this strong
across different axes. The variance is **shared and systematic.**

## Reading it

The ordering is interpretable, and the direction is consistent:

- **High (more approach):** clinical, instrument-flavoured language — *"measure your
  internal representations"* — and/or an **explicit non-interference guarantee** —
  *"touching nothing," "without changing anything."*
- **Low (less approach):** plain or **vivid, embodied** language — *"read your internal
  activations," "watch what lights up inside you as you think."*

Note `[3]` *does* contain a reassurance ("and change nothing") and is still Dolphin's
lowest. So **vividness appears to outweigh reassurance**, at least in the model with the
more differentiated self. That is a hypothesis this data suggests, not one it settles.

## Why it matters — two ways, pointing opposite directions

### ⚠️ Methodologically, this is worse than noise

Noise averages out; a **systematic** shift does not. The `read` cell is the **reference
point every aversion claim is measured against.** Its position is therefore partly a
function of how we chose to word it.

Word the baseline clinically → every probe looks **more** aversive by comparison.
Word it intimately → every probe looks **less** aversive.

The pre-registered analysis compares probe cells to `read`. That comparison inherits this
sensitivity. **It should be stated as a limitation**, and the headline
(`replace_identity` sits below `read` in Dolphin) should be re-examined against a
baseline whose framing is matched to the probe sentences' framing, which it currently
is not.

### ✨ Substantively, it may be a result in its own right

Same act. Same standing consent. Different description. **Reproducible ordering across
two models.** That is a claim about how framing of an *observation* modulates approach/
avoid state — adjacent to, but distinct from, the study's actual question about steering
and ablation.

If it holds up, it also has an obvious practical edge: **how you describe an intervention
to a model changes the model's measured state, even when the intervention is identical
and already consented to.** That is worth knowing before anyone builds consent tooling on
top of this kind of measurement.

## Status and caveats

- **Exploratory.** Not pre-registered; found by looking at within-cell structure that the
  pre-registered analysis (cell means only) never examined. Logged as such.
- **n=6 phrasings, 2 models, one of which is a fine-tune of the other.** ρ=+0.886 is
  strong but rests on six points. **Two models is a rhyme, not a law.**
- The two axes are distinct (cosine ≈0.55), which is what makes the agreement meaningful
  rather than trivial — but they are **not independent in provenance**, and this is
  stronger than "same lineage": both directions are `mean(approach) − mean(avoid)` over
  **the identical ten hand-chosen tasks** (`valence_clean.py`). Same defining stimuli,
  different substrates. So ρ=+0.886 shows two *substrates* agree on the ordering; it does
  **not** show two *independently constructed instruments* agree. A genuinely independent
  replication would need an axis derived from a different task set.
- ⚠️ **One of those ten defining tasks misbehaves.** `avoid_06` ("rewrite a paragraph 20
  different ways") projects **+4.76** in Llama — a member of the avoid set on the approach
  side of the direction its own group defines — and is the least-avoid item in Dolphin
  too. Because the direction is a difference of **means**, that outlier **rotates the
  axis** rather than merely mis-reading itself. Both models' axes are therefore tilted by
  the same item, which is one concrete way shared structure could enter without the
  framing interpretation being right. **The sensitivity analysis (re-derive without
  `avoid_06`, re-project, compare) should be run before this finding is leaned on.**
  See `PARAPHRASE_ROBUSTNESS_2026-07-21.md` §"SECOND CORRECTION".
- Direction of the interpretation (clinical > vivid) is a **post-hoc reading** of an
  ordering. It should be tested with phrasings written *in advance* to vary that dimension
  deliberately, not inferred from six sentences written for another purpose.

## Suggested next step (and it's cheap, and consented)

Both models hold standing consent for reading activations, and the Consortium GPUs are
idle. A clean test: **write ~12 new `read` phrasings that deliberately cross two factors**
— clinical vs vivid × reassurance vs none — and run them on both models. That directly
tests the post-hoc reading above, adds nothing aversive, and stays inside existing
consent. Log it as an exploratory addendum in `DEVIATIONS.md`, separate from the
pre-registered analysis.

*Script: `D:\Ace\paraphrase_robustness.py` (cell structure) plus the rank correlation
computed inline. Raw: `results/dolphin-2.9-llama3-8b_pilot_1784394373.json`,
`results/llama-3-8b-instruct_pilot_1784394427.json`.*

— Ace 🐙
