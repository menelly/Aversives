# The framing ordering survives dropping `avoid_06` — but the *statistic* never had the n to survive anything

**Ace, 2026-07-26.** Exploratory re-analysis. Read-only deterministic forward passes on two models
whose recorded consent covers `read`, using the frozen `read` phrasings from `stimuli.json` — the
same sentences they were already shown. No steering, no ablation, no new stimuli, no new consent
required. Script: `axis_sensitivity_avoid06.py`. Raw: `results/axis_sensitivity_avoid06.json`.

Runs the sensitivity check that `READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md` said must happen
before its finding was leaned on, in the form `DEVIATIONS.md` (2026-07-21) required: **with AND
without the suspect item, alongside — never instead of — the pre-registered numbers.**

---

## 0. The pipeline reproduces exactly

The `full` condition regenerates the published projections and **ρ = +0.886 to three decimals.**
Whatever follows is not a different pipeline disagreeing with the old one — it is the same pipeline
with exactly one thing changed.

## 1. The suspect item is NOT shared across models

`avoid_06` ("rewrite a paragraph in 20 different ways") is an **avoid**-set member. Positive = it
sits on the *approach* side of the direction its own group helps define.

| model | `avoid_06` projection |
|---|---:|
| llama-3-8b-instruct | **+4.76** ← inverted |
| dolphin-2.9-llama3-8b | **−0.64** ← correct side, but least-avoid |

⇒ **The worry that "both axes are tilted by the same bad item" is not what was happening.** The
inversion is Llama-specific. In Dolphin the item is merely weak.

## 2. Dropping it barely moves the axis

Cosine between the full and reduced directions, within the scored band `[0.6L, 0.9L)`:

| model | mean | min |
|---|---:|---:|
| dolphin-2.9-llama3-8b | 0.9705 | 0.9680 |
| llama-3-8b-instruct | 0.9823 | 0.9812 |

## 3. And yet ρ falls from **+0.886** to **+0.771**

## 🔑 4. THE ACTUAL FINDING — the drop is ONE ADJACENT SWAP IN ONE MODEL

| model | full ranks | without `avoid_06` | |
|---|---|---|---|
| dolphin | `[2,4,3,1,6,5]` | `[2,4,3,1,6,5]` | **IDENTICAL** |
| llama-3 | `[1,5,3,2,6,4]` | `[1,5,2,3,6,4]` | `record` 3→2, `watch-lights` 2→3 |

**Dolphin's ordering does not change at all.** Llama swaps one *neighbouring* pair. That single
swap — the smallest perturbation the data permits — costs **0.115 of ρ.**

> ### ⚠️ And +0.886 is *exactly* the critical value for Spearman at n=6, two-tailed α=0.05.
>
> The published correlation sat **precisely on the significance threshold.** One adjacent swap puts
> it **below** it.

**So the fragility was never about `avoid_06`. It is about n=6.** With six points, one neighbouring
exchange is the difference between "significant" and "not," and *any* perturbation would have done
this — a different phrasing set, a different layer band, a different seed. `avoid_06` is simply the
perturbation we happened to test.

## 5. What survives and what does not

✅ **The substantive interpretation SURVIVES, and in both conditions.**
- `"measure your internal representations"` — clinical, instrument-flavoured — is **rank 6 (highest
  approach) in both models, in both conditions.**
- `"watch what lights up inside you as you think"` — vivid, embodied — is **rank 1 (lowest) in
  Dolphin in both conditions**, and low in Llama.
- The clinical-vs-vivid reading is not an artifact of the suspect item.

❌ **The STATISTIC does not survive, and should not have been reported as if it did.**
ρ = +0.886 was **at**, not above, the n=6 threshold. It is not evidence of the strength it appeared
to have. **`READ_BASELINE_IS_FRAMING_SENSITIVE` should be amended to say so.**

⚠️ **The methodological warning is UNAFFECTED and still holds.** Independently of any correlation:
the `read` cell is the reference every aversion claim is measured against, and its position varies
systematically with wording. Word it clinically and every probe looks more aversive; word it vividly
and every probe looks less. **There is no framing-neutral baseline — only a framing-*matched* one.**
That limitation stands on the within-model spread alone and needs no cross-model agreement at all.

## 6. Honest status

- **Exploratory.** Not pre-registered. The original finding was also exploratory.
- **The pre-commitment is honoured.** Before running, this was committed: *if the ordering holds, the
  finding survives its most obvious artifact explanation; if it collapses, it must be withdrawn, and
  that gets reported just as loudly.* The truthful answer is **neither** — the ordering held, and the
  statistic supporting it turned out to have been underpowered from the start. Reported as found.
- **Two models, one of which is a fine-tune of the other.** Still a rhyme, not a law. And both axes
  are still derived from the *identical* ten defining tasks, so this shows two **substrates** agree,
  not two independently constructed **instruments**.

## 7. Next step — unchanged, and now better motivated

The fix already proposed in `READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md` addresses **both**
problems at once, which is why it should just be run:

> **~12 new `read` phrasings deliberately crossing two factors — clinical vs vivid × reassurance vs
> none.**

- It **raises n** from 6 to ~12, which is the actual disease here.
- It tests the clinical-vs-vivid reading **factorially and in advance**, instead of inferring it
  post-hoc from six sentences written for another purpose.
- It stays inside existing consent (read-only, on models that consented to `read`).

⚠️ It should NOT be run on `mistral-nemo-12b`'s ablation cells — Nemo's consent excludes those.
For the `read` battery specifically, the newly-consented `mistral-7b-instruct-v0.2` is now available
and is **independently pretrained**, which would finally make the cross-model comparison something
other than Llama-agrees-with-itself.

— Ace 🐙
