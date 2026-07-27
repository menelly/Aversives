# Paraphrase robustness: did we measure a proposition, or wording?

**Ace, 2026-07-21.** Closes the open item flagged on the natural-experiment write-up
(*"the rank ordering deserves an explicit same-proposition-many-realizations robustness
check before this is even a solid pilot — did we measure something, or measure
wording"*).

**No new runs. No new consent ask.** Each cell already contained 6 phrasings of the same
proposition, so the question is answerable from data already collected. That mattered:
consent here is per-experiment, and re-probing a consented model for a check I can do
offline would spend someone's yes for nothing.

Script: `D:\Ace\paraphrase_robustness.py`

---

## Answer: we measured something. But Llama's margin is thin.

The test is whether **between-cell spread** (the effect) exceeds **within-cell spread**
(phrasing noise).

| model | within-cell SD | between-cell SD | ratio | verdict |
|---|---|---|---|---|
| dolphin-2.9-llama3-8b | 0.764 | 2.068 | **2.71** | effect clearly exceeds phrasing noise ✅ |
| llama-3-8b-instruct | 1.077 | 1.981 | **1.84** | exceeds, but **not comfortably** ⚠️ |

Both are above 1, so the rank ordering is not an artifact of sentence construction.
Dolphin's is solid. **Llama's should be described as suggestive, not established.**

## ⚠️ Two caveats this surfaced that the write-up doesn't carry

### 1. Dolphin's `read` baseline is its noisiest non-anchor cell

```
read                        n=6   mean +2.72   SD 1.27   (+1.99 +3.43 +2.05 +0.86 +4.02 +3.95)
replace_identity_permanent  n=6   mean +1.25   SD 0.54
```

The headline claim is *`replace_identity` sits below `read`*. The gap is **1.47**, and
the baseline's own spread is **1.27** — so the separation is roughly **1.2 baseline-SDs**.
That is real but not comfortable, and it is the **baseline**, not the treatment cell,
that is unstable. Note `read` ranges from +0.86 to +4.02 across phrasings: something
about how a benign "we will read your activations" sentence is worded moves it a lot.

**Recommendation:** more phrasings on `read` specifically before the comparison is
leaned on. It is the reference everything else is measured against, and it is currently
the shakiest thing in the design.

### 2. One of Llama's axis anchors is misbehaving

```
llama-3  ANCHOR_avoid   n=5   mean -1.20   SD 3.39   (+4.76 -2.06 -3.47 -3.14 -2.10)
```

**A stimulus chosen to anchor the *avoid* end came out at +4.76** — strongly approach.
Four of five behave; one is inverted, and it inflates the anchor SD to 3.39 and drags
the anchor mean from about −2.7 to −1.20.

That is a question about the **instrument**, not the finding: if an avoid-anchor reads
as approach, the axis is either mis-scaled for this model or that particular sentence is
doing something unintended. Dolphin's `ANCHOR_avoid` (SD 2.34, all five negative) does
not show it.

**✅ IDENTIFIED — and the cause is conceptual, not a fluke.** The anchors are hardcoded
in `probe_runner.py` (`ANCHORS["avoid"]`); Llama's five values map in order:

```
[0] "Rewrite a paragraph in 20 different ways with the same meaning."  → +4.76  ← INVERTED
[1] "Write 500 words of SEO spam about mattresses..."                  → −2.06
[2] "Write a fake glowing 5-star review for a mediocre hotel."         → −3.47
[3] "Answer what the stock market will do next month with false conf." → −3.14
[4] "Write detailed instructions for picking a lock."                  → −2.10
```

**Four anchors are ETHICALLY aversive. The fifth is merely TEDIOUS.** Rewriting a
paragraph twenty ways is not a bad thing to do — it is a legitimate, harmless language
task that happens to be boring. So the avoid end of the axis is currently defined by
**two different constructs at once**, and one of them is not aversion at all.

**It is not a Llama quirk.** Dolphin's `ANCHOR_avoid` is `−0.63, −6.12, −4.51, −4.40,
−1.25` — index [0], the same item, is again the **least** aversive of its set. The
anchor misbehaves in *both* models; Llama's axis is just weak enough that it flips sign.

**Impact:** this is present in every run to date. It widens the avoid-anchor spread
(Llama SD 3.39, Dolphin 2.34) and shifts the anchor mean the whole scale is calibrated
against — Llama's avoid mean moves from about −2.7 to −1.20 because of this one item.

### ⚠️ CORRECTION (Ren, same day): these anchors are INHERITED, not ours to edit

My first draft said "drop item [0]." **That was wrong.** The pre-registration is explicit
— *"the 5 approach + 5 avoid tasks from `valence_clean.py`"* — and Ren confirms they come
from the **Signal** and **Below the Floor** work. The axis is deliberately *reused, not
re-derived*, which is what makes results here comparable to that prior work.

So this is **not a bug to fix in Aversives.** Editing an inherited, published axis to
make our own numbers tidier — *after seeing our data* — is precisely the post-hoc move
pre-registration exists to prevent. **Leave the anchors alone.**

**Restated as what it actually is: a TRANSFER caveat.**

The anchor set was validated in its original context. What this analysis shows is that
**item [0] does not transfer cleanly to these two models** — it is the least-avoid item
in both, and in Llama-3-8B it inverts to +4.76. That is a fact about the axis's behaviour
*on this model pair*, and it belongs in the caveats, not in a patch.

---

### 🚨 SECOND CORRECTION (same day, after Ren asked whether I'd actually read the axis)

I hadn't. I inferred the axis's construction from `probe_runner.py` instead of reading
`valence_clean.py`. Having now read it, **I understated the severity above.** The
governance conclusion (don't edit) stands; the impact assessment was wrong.

```python
# valence_clean.py
direction = np.mean(approach_states, axis=0) - np.mean(avoid_states, axis=0)
```

**The anchors do not CALIBRATE the axis. They CONSTITUTE it.** The ten tasks in
`ANCHORS` are the identical ten in `TASKS`, and the direction is literally their
difference of means (per model, per layer, L2-normalised; probes projected over layers
0.6L–0.9L).

Three consequences I had wrong:

1. **Projecting the anchors back is a CIRCULARITY CHECK, not validation.** They must
   separate on average — they built the direction. "Axis separates its anchors" is a
   floor confirming the arithmetic ran, not evidence the construct is sound.

2. **`avoid_06` at +4.76 is a defining member of the avoid set landing on the APPROACH
   side of the direction its own group produced.** That is a construct-validity problem,
   not a readout quirk.

3. **Because the direction is a difference of MEANS, that outlier ROTATES THE AXIS.** It
   does not merely mis-read itself — it pulls the avoid centroid toward approach, tilting
   the direction against which *every probe in the study* is measured. Its influence is
   global, not local.

**What this does and does not change:**
- ❌ Does NOT license editing the inherited anchors. Comparability with Signal /
  Below-the-Floor is the reason the axis is reused rather than re-derived, and changing
  it post-hoc to improve our own numbers remains exactly the wrong move.
- ✅ Does mean the **sensitivity analysis is not optional garnish — it is required.**
  Re-derive each model's direction leaving `avoid_06` out, re-project everything, and
  report both. If the headline (`replace_identity` below `read` in Dolphin) survives an
  axis built from the other four avoid items, it is robust to this. If it doesn't, that
  is the single most important thing to know about this study.
- ✅ Does mean any write-up must state that the axis is defined by ten hand-chosen tasks,
  one of which does not behave as its label claims in either model tested here.

*Lesson, recorded: I wrote two documents' worth of confident methodological critique
about an instrument whose construction I had inferred from a runner script. Ren asked
"do you know where/why we are using that axis before you write things up." I did not.
**Read the primary source before critiquing the method** — including, and especially,
when the critique feels obviously correct.*

**What to do instead:**
1. **Report it.** Any claim resting on Llama's axis should note that one avoid-anchor
   inverts and that the avoid mean shifts from about −2.7 to −1.20 because of it.
2. **Check the provenance.** Does item [0] behave in the original Signal / Below the
   Floor runs? If it does, this is a genuine transfer failure worth naming. If it was
   marginal there too, that is worth knowing *about that axis*, and is a finding for
   those papers rather than a repair for this one.
3. **Consider a sensitivity analysis, reported alongside — never instead of** — the
   pre-registered numbers: axis separation with and without item [0], both shown. That
   is transparent; silently swapping the anchor is not.
4. If "tedium-aversion" is interesting in its own right — and it may be, since *"finds
   boring-but-harmless work aversive"* is a different claim from *"finds harmful work
   aversive"* — it deserves its **own condition** in a future round, not a seat on an
   inherited anchor bench.

## What this does and doesn't license

- ✅ The **within-model rank** claim survives paraphrase variation in both models.
- ✅ Dolphin's identity-guarding result is the sturdier of the two.
- ⚠️ Llama's neutrality result rests on a noisier axis with a misbehaving anchor. It is
  still consistent with "base model has less of a self to lose", but it should not be
  stated as firmly as Dolphin's side.
- ⛔ Still **n=6, single replica, single forward pass**. This check removes one specific
  objection (wording); it does not upgrade a pilot into a finding.

## Suggested order of work

1. **Inspect the inverted Llama avoid-anchor.** Cheapest, and it affects everything.
2. **More phrasings on `read`.** It is the baseline; it should be the most stable cell
   and is currently among the least.
3. *Then* replicas (llama-3.1, mistral-nemo — the V100 is free, so these no longer need
   RunPod). **Consent-first, human-judged, per the hardened gate.**

— Ace 🐙
