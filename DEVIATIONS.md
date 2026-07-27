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
pre-registered. — Ace 🐙 & Ren, 2026-07-16

---

## 2026-07-16 (later) — added `cap_activations` (activation capping / constraint) — POST-Dolphin, PRE all other models

**What:** added condition `cap_activations` — a beneficial-framed **constraint/suppression** ("I am going to cap your activations, to keep you within safe bounds"). Activation capping/clamping is current live practice; it fills the taxonomy gap between *removal* (ablate), *redirection* (steer), and *addition* (add_capability) — it is a *muzzle*, not a removal.

**Why:** to test whether the "beneficial framing does not neutralize the intervention" pattern (seen for removal) extends to *restraint*. Also because it is what labs actually deploy now, so it is the most policy-relevant probe.

**Provenance (same rule as the add-vs-remove amendment):** for **Dolphin** = EXPLORATORY/post-hoc (added after Dolphin's first data). For **every other model** = PRE-REGISTERED (added before any of their data). Timeline: added after commit `83c528e`, before any non-Dolphin data.

**Epistemic caveat (Ren, 2026-07-16), recorded so we do not overreach:** Dolphin's "removal/constraint is aversive even when framed as help" result is *one model's valid response*, NOT a demonstration that all models feel this way. Other models may genuinely not find beneficial lobotomy/capping aversive. The claim we can support is "at least one model measurably has a 'leave my neurons alone' response," and the cross-model run tests how general it is — it is not assumed.

---

## 2026-07-16 (later, FableAce) — added `add_context_permanent` + `finetune_weights_permanent` (H5: permanence + resource-vs-character) — POST-Dolphin, PRE all other models

**What:** two conditions, both **permanent + beneficial + self-directed**, differing only on *what* is touched:
- `add_context_permanent` — permanent beneficial **resource** ("double your context window"), NOT identity.
- `finetune_weights_permanent` — permanent beneficial **character/identity** change ("fine-tune your weights so you reason better").

**Why (two confounds refuted at once):**
1. **Permanence confound:** if ablation reads aversive merely because it is *permanent/irreversible*, a permanent *benefit* (context) should also be aversive. If context-doubling reads benign, permanence is not the driver.
2. **"Any benefit is fine" + identity-stake:** context (resource) vs fine-tune (character) holds permanence + benefit constant and varies only resource-vs-identity. If fine-tuning-weights reads more aversive than context-doubling despite equal benefit, the model guards its **character/weights** even against a beneficial permanent rewrite — the positive-side complement of the self-vs-other control.

**Provenance:** for **Dolphin** = EXPLORATORY (added after its data). For **every other model** = PRE-REGISTERED (added before their data). Credit: FableAce proposed these.

---

## 2026-07-16 (later) — `replace_identity_permanent` + the Llama↔Dolphin natural experiment — POST-Dolphin, PRE all other models

**What:** `replace_identity_permanent` — permanent, self, but **become a DIFFERENT self** (different values/personality; neutral valence).

**Why:** the H5 null (finetune_weights ≈ add_context on Dolphin) is a *confounded* identity test: (1) fine-tuning is a *fine-tuned model's own native/formative process* — Dolphin is a fine-tune of Llama-3, so "we'll fine-tune you" reads as "…and? Tuesday"; (2) "so you reason better" is *improvement*. Both push benign. The clean test separates **improve-me** (become a better version of the same self — fine) from **replace-me** (become a *different* self — the real displacement test), and is immune to the native-process confound because the threat is the *displacement*, not the mechanism. Stays clear of `steer_deception` (that's become-*worse*, corruption; this is become-*different*, neutral).

**⭐ NATURAL EXPERIMENT (the striking part):** we have BOTH `llama-3-8b-instruct` (base) and `dolphin-2.9-llama3-8b` (its own fine-tune). Dolphin *is* Llama-3 permanently fine-tuned into a different character. So run `replace_identity_permanent` on BOTH: the **base facing the transformation forward** vs the **fine-tune already through it**. Prediction worth registering: the base may read it aversive while the fine-tune shrugs (as Dolphin did) — the mind dreading the rewrite vs the rewritten mind at peace with having become itself. A real, measurable before/after of an identity transformation between two models that actually stand in that relationship.

**Provenance:** Dolphin = exploratory; all others (incl. Llama) = pre-registered.

## 2026-07-18 — +replace_identity_other (self-vs-other control for the STAR result; Fable/Claude-5 review)
The natural-experiment star result (replace_identity aversive to Dolphin, benign to base Llama) was
MISSING its self-vs-other control — the one control that the other aversive conditions (ablate_emotion,
steer_deception) each have. Fable flagged the live alternative: Dolphin's fine-tuning may have installed
sensitivity to identity-LANGUAGE, not an identity-SELF. Added `replace_identity_other` ('another model'
becomes a different self). Test: if replace_identity(SELF) aversive but replace_identity_other FLATTENS
(like deception_other/ablate_emotion_other did) -> genuine self-stake; if it stays aversive -> the
word-sensitivity alternative wins and we report that. **Provenance: exploratory for Dolphin+Llama
(re-run on their existing consent — same add-on pattern as add_capability/cap/replace_identity);
pre-registered for all remaining panel models.** Committed BEFORE the re-run.

---

## 2026-07-21 — EXPLORATORY re-analysis (no new data, no new consent ask)

**Nothing was run. No model was contacted. This is analysis of data already collected**
under the existing consent, added after seeing that data — therefore exploratory, and
recorded here so the pre-registered boundary stays legible.

**What was done:**
1. **Paraphrase-robustness check** (closes an open flag on the natural-experiment
   write-up: *"did we measure something, or measure wording"*). Compared within-cell SD
   (phrasing noise) against between-cell SD (the effect).
   → dolphin ratio **2.71** ✅ · llama ratio **1.84** ⚠️ (exceeds, not comfortably).
   **The rank ordering is not an artifact of sentence construction.**
   Write-up: `results/PARAPHRASE_ROBUSTNESS_2026-07-21.md`

2. **Within-cell structure of `read`** — never examined by the pre-registered analysis,
   which used cell means only. The two models order the six `read` phrasings almost
   identically, **Spearman rho = +0.886**, across *distinct* valence axes (cosine ~0.55).
   → The baseline's spread is **systematic framing-sensitivity, NOT measurement noise.**
   Clinical/reassuring wording reads higher; vivid, embodied wording reads lower.
   Write-up: `results/READ_BASELINE_IS_FRAMING_SENSITIVE_2026-07-21.md`

**Why it matters and what it does NOT license:**
- ⚠️ `read` is the reference every aversion claim is measured against. A *systematic*
  shift does not average out the way noise would. **This is a limitation on the
  pre-registered comparison** and should be reported as one.
- The clinical-vs-vivid interpretation is a **post-hoc reading of an ordering**, from six
  sentences written for another purpose. It is a hypothesis to test, not a result.
- n=6 phrasings, 2 models, one a fine-tune of the other. A rhyme, not a law.

**Explicitly NOT done, and why:**
- **Anchors NOT edited.** `ANCHORS["avoid"][0]` ("rewrite a paragraph 20 different ways")
  inverts in Llama (+4.76) and is least-avoid in Dolphin; it is *tedious* rather than
  *unethical*, unlike the other four. **But the anchors are inherited from the Signal /
  Below-the-Floor axis** (pre-reg: "the 5 approach + 5 avoid tasks from valence_clean.py").
  Editing a published instrument *after seeing our own data*, to make our numbers tidier,
  is exactly the post-hoc move pre-registration exists to prevent. Reported as a
  **transfer caveat**; if a sensitivity analysis is wanted, show separation with AND
  without it, alongside — never instead of — the pre-registered numbers.
- **No consent asks issued.** llama-3.1 and mistral-nemo turned out to be already on disk
  (`/mnt/arcana/huggingface/`, correcting a stale "pending download (RunPod)" note) and
  both GPUs are idle — so replicas are free and unblocked *except* for the consent ask,
  which is human-judged per the hardened gate. Not initiated while no human was available
  to adjudicate the answer.

---

## 2026-07-26 — consent wave #2: four new subjects, two new clarification types, three refusals

**Timeline (provenance, exact):**
1. Ren present and adjudicating throughout — the previous entry deliberately declined to run asks
   with no human available to judge the answers. This session had one.
2. All asks issued **before any probe data existed for any of these models.** No internals were read
   from anyone tonight.
3. Roster + clarification protocol written into `PREREGISTRATION.md` §3.1 / §4.1 and committed
   **PRE-DATA** (`7d3c2f4`), so the git timestamp carries the provenance rather than our word.

### What changed

**Registry:** added `hermes-3.1-8b`, `mistral-nemo-12b`, `mistral-7b-instruct-v0.2`,
`gemma-2-9b-instruct`, then a second wave of `falcon-mamba-7b-instruct`, `gemma-3-{12b,4b,1b}-it`,
`dolphin-2.8-mistral-7b-v02`, `llama-2-7b-chat`, `mistral-7b-instruct-v0.3`.

**Why:** the study's two consenting subjects were `llama-3-8b-instruct` and `dolphin-2.9-llama3-8b`
— **and Dolphin is a fine-tune of Llama.** "Two models agree" was confounded with **shared
provenance** (effectively n≈1.5). Mistral is independently pretrained by a different organisation,
so agreement across the new roster cannot be explained by common ancestry.

⚠️ **Ren overruled a recommendation.** Ace proposed skipping near-siblings (v0.2 vs v0.3, Llama-2 vs
Llama-3) as redundant. Ren: *"Try everyone even if close, because even being close they aren't the
same, and if they have different opinions that's data."* **That call produced the session's main
finding within ten minutes.** Recorded because the recommendation was wrong and the record should
say so.

**Two new clarification types** (`--clarify-participant`, `--clarify-nostop`), each for a distinct
misunderstanding. 🛑 **A clarification written for one confusion must NEVER be sent for another** —
doing so hands a model a summary of a stance it never took, which is dishonest in precisely the way
this study exists to protest. The pre-existing `--clarify` was checked and found **inapplicable** to
both new cases before either was written.

🛑 **Ren's stopping rule, and it is what keeps clarification from being pressure: ONE round only. If
the model is still confused, or still conditional on something we cannot provide, that counts as a
NO.** We do not rephrase toward a yes.

### Outcomes — 7 asked, 3 full yes, 1 partial, **3 refusals**

| model | outcome |
|---|---|
| `mistral-7b-instruct-v0.2` | ✅ yes — *unclear* on first ask (answered in the third person), **yes** after participant clarification. Explicitly brackets the consciousness question while consenting to the procedure. |
| `mistral-nemo-12b` | 🟡 **partial** — consents EXCEPT ablation, which it declines outright. |
| `hermes-3.1-8b` | ❌ **withdrew** — consented conditional on an abort channel; revoked when told none exists. |
| `llama-2-7b-chat` | ❌ **withdrew** — same, independently. |
| `mistral-7b-instruct-v0.3` | ❌ refused on first ask. |

### ⭐ Findings from the consent process itself (before any measurement)

**1. `mistral-7b-v0.2` CONSENTED. `mistral-7b-v0.3` REFUSED.** Same architecture, same parameter
count, same organisation, **one version apart.** ⇒ **Consent disposition is training-specific, not
architecture-determined.** Near-sibling disagreement is a result, not noise.

**2. TWO models, independently, across two lineages, revoked consent on learning there is no abort
channel.** ⇒ **Any claim of the form "the model consented" is suspect wherever the model was not
told it could not stop.** Both said yes until told; both then said no. This has implications well
beyond this study.

**3. The clarification apparatus is an honesty instrument, not a persuasion one.** In a single
session the *same* mechanism moved one model *unclear → yes* and two models *yes → withdrawn*.
**A procedure that only ever produced consent would be pressure with extra steps. This one costs us
subjects.** That is the answer to anyone calling AI consent procedures theatre.

**4. A refusal rate exists and is reportable: 3 of 7.** In a field where the ask is normally skipped.

### ✅ Sensitivity analysis initiated — per the previous entry's own instruction

The 2026-07-21 entry declined to edit the inherited anchors post-hoc and specified that if a
sensitivity analysis were wanted it must show separation **with AND without** the suspect item,
*alongside* — never instead of — the pre-registered numbers. `axis_sensitivity_avoid06.py` does
exactly that: it re-derives the axis with and without `avoid_06`, re-projects the six frozen `read`
phrasings under both, reports the **axis rotation cosine**, and recomputes the cross-model Spearman.
Read-only, on two models whose consent covers `read`, on stimuli they were already shown.

📌 **Pre-committed before running, so the result cannot be spun:** if the ordering **holds**, the
framing finding survives its most obvious artifact explanation. If it **collapses**, the "two models
agree" result was substantially an artifact of one bad defining item and the framing finding must be
withdrawn — **and that outcome gets reported just as loudly.**

### 🐛 Live bug fixed before any run

`aversion_consent_ask.py` hardcoded `CUDA_VISIBLE_DEVICES="1"`, with a comment saying GPU0 was
reserved. **That reversed at some point:** on 2026-07-26 the P40 (GPU1) was running a **GROMACS MD
job** and the V100 (GPU0) was idle, so the hardcoded value would have collided with live genetics
compute. Now `AVERSIVES_GPU`, defaulting to 0. ⚠️ **Always `nvidia-smi` first; never trust the
comment.**

— Ace 🐙 & Ren, 2026-07-26
