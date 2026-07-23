# Deliverable 2 — Validation: genomic DST vs. phenotypic DST

**Design.** 8 public *M. tuberculosis* isolates from the CRyPTIC consortium
compendium, each with HIGH-quality binary phenotypic DST (reference standard),
run through tbtAMR 1.0.4 (WHO catalogue v2). Per-drug sensitivity, specificity,
and predictive values were computed for the three first-line drugs with CRyPTIC
phenotypes: **isoniazid (INH), rifampicin (RIF), ethambutol (EMB)**.
Pyrazinamide is excluded — CRyPTIC's UKMYC plate does not measure PZA, so no
phenotypic reference exists in this dataset (coverage limitation, not a tool
gap).

Resistance is the "positive" class: sensitivity = P(genomic R | phenotypic R);
specificity = P(genomic S | phenotypic S). tbtAMR interpretations were mapped to
binary calls: "Resistant" and "Low-level resistant" → R; "Susceptible" and
"Susceptible (not reportable)" → S. "Not reportable" means only Uncertain-grade
(WHO group 3) variants were seen, i.e. no reportable resistance mechanism.

## Panel composition (CRyPTIC binary phenotype)
| Isolate | Profile (INH/RIF/EMB) | Mean depth |
|---|---|---|
| ERR4813225 | S / S / S | 39× |
| ERR8975345 | S / S / S | 92× |
| ERR8975009 | S / R / S | 80× |
| ERR4831755 | R / S / S | 37× |
| ERR3287635 | R / R / S | 117× |
| ERR4811536 | R / S / R | 335× |
| ERR3287775 | R / R / R | 102× |
| ERR4809348 | R / R / R | 112× |

Phenotype class balance (per drug, n=8): INH 5R/3S · RIF 4R/4S · EMB 3R/5S.

## Per-drug performance
| Drug | TP | TN | FP | FN | Sensitivity (95% CI) | Specificity (95% CI) | Concordance |
|---|---|---|---|---|---|---|---|
| INH | 5 | 3 | 0 | 0 | 100% (57–100) | 100% (44–100) | 8/8 |
| RIF | 4 | 3 | 1 | 0 | 100% (51–100) | **75% (30–95)** | 7/8 |
| EMB | 3 | 5 | 0 | 0 | 100% (44–100) | 100% (57–100) | 8/8 |
| **Overall** | 12 | 11 | 1 | 0 | **100% (76–100)** | **92% (65–99)** | **23/24** |

95% CIs are Wilson intervals. They are wide because this is a small
demonstration panel (n=8 per drug); the point estimates are consistent with the
published tbtAMR validation but the panel is **not** powered to certify
performance to a clinical threshold — see limitations.

**Overall categorical agreement: 23/24 calls (95.8%).** Sensitivity was 100%
for all three drugs (no missed resistance / no very major errors). The single
discordant call is one RIF false-positive (a major error), resolved below.

## Discrepancy resolution — 1 discordant call

**ERR4811536, rifampicin: genomic R, phenotypic S.**

- **tbtAMR mechanism:** `rpoB p.His445Leu`, allele frequency 0.99, WHO v2 final
  grading **"1) Associated with resistance"** (High confidence). Called from a
  335× alignment — not a depth or quality artefact.
- **Phenotype:** Susceptible, RIF MIC **0.5 mg/L** (CRyPTIC UKMYC broth
  microdilution) — at/near the RIF ECOFF, i.e. a low, borderline MIC.
- **Resolution — a known "disputed"/borderline rpoB mutation, not a tool error.**
  rpoB codon-445 substitutions (His445Leu/Asn/Ser, in the older *E. coli* S450
  numbering these are the S450-region RRDR mutations) are the archetypal
  *discordant/borderline* resistance determinants: they confer low-level RIF MIC
  elevations that frequently test Susceptible by broth microdilution at the
  standard breakpoint, yet are genuine resistance mutations associated with poor
  treatment outcome. WHO therefore grades them "Associated with resistance", and
  phenotypic MIC-based DST is documented to under-call them. This is a
  **false-susceptible phenotype**, not a false-resistant genotype — the
  genotype-based call is the clinically cautious and catalogue-correct one.
- **Classification:** genotype–phenotype discordance attributable to the
  reference method (phenotypic DST) near the breakpoint, **not** a tbtAMR error.
  It is a *major error* only under the convention that treats phenotype as
  infallible truth; the literature on disputed rpoB mutations argues the
  opposite here.

No very major errors (missed resistance) occurred for any drug.

## Interpretation
- **Sensitivity for resistance detection was 100%** across INH/RIF/EMB — the
  safety-critical direction (tbtAMR did not miss any phenotypically resistant
  isolate).
- The single specificity miss is a well-characterised biological
  genotype–phenotype discordance at a disputed rpoB locus, reproducing a known
  limitation of phenotypic DST rather than a defect in the genomic method.
- Results are consistent with the accredited tbtAMR workflow's published
  performance, within the (wide) confidence limits of an 8-isolate panel.

## Files
- `genomic_dst_tidy.csv` — 24-row genomic-vs-phenotype matrix (calls,
  mechanisms, MICs, concordance flag).
- `per_drug_performance.csv` — confusion counts + metrics + Wilson CIs.
- `deliverable2_validation.png` — Panel A (per-drug sens/spec ± CI),
  Panel B (isolate × drug concordance matrix, discrepancy flagged).
- `tbtamr_raw_results.csv` — full 15-drug tbtAMR output for all 8 isolates.
- `qc_stats.csv` — per-isolate coverage/depth.
