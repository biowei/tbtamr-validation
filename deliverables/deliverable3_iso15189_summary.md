# Method-Validation Summary — Genomic Drug-Susceptibility Prediction for *Mycobacterium tuberculosis* (tbtAMR)

**Document type:** Method-validation exercise summary, structured to ISO 15189:2022 §7.3.
**Status:** Reproduction / validation exercise only — **not** a clinical release or an accreditation record.
**Date:** 2026-07-23  ·  **Analyst:** Claude Science (automated)  ·  **Scope owner:** (user)

---

## 1. Purpose & scope (ISO 15189 §7.3.1)
To reproduce and validate, on independent public data, the genomic
drug-susceptibility (genomic DST) workflow of Horan et al., *Lancet Digital
Health* 2025;7(12):100939 — the NATA/ISO 15189-accredited MDU-PHL **tbtAMR**
pipeline — which predicts *M. tuberculosis* drug susceptibility from Illumina
whole-genome sequencing against the **WHO mutation catalogue v2**.

**Examination validated:** paired-end Illumina FASTQ → aligned/called variants →
WHO v2 catalogue interpretation → per-drug R/S genomic call.
**Analytes (this exercise):** first-line drugs **isoniazid, rifampicin,
ethambutol**. Pyrazinamide is in the tool's output but was **not** validated —
the CRyPTIC reference dataset carries no PZA phenotype (§8, limitation).
**Intended use statement:** demonstration of analytical validity of a genomic
DST method. This exercise does **not** establish clinical validity, fitness for
patient reporting, or local accreditation.

## 2. Materials (ISO 15189 §7.3.2 — specimens & reference materials)
- **Isolates:** 8 public *M. tuberculosis* WGS runs from the CRyPTIC consortium
  compendium (Illumina, paired-end), retrieved from ENA. Accessions:
  ERR4813225, ERR8975345, ERR8975009, ERR4831755, ERR3287635, ERR4811536,
  ERR3287775, ERR4809348.
- **Reference standard:** CRyPTIC HIGH-quality **binary phenotypic DST**
  (UKMYC broth microdilution), from `CRyPTIC_reuse_table_20221019.csv`
  (EBI public release). Panel spans pan-susceptible → MDR profiles; per-drug
  class balance INH 5R/3S, RIF 4R/4S, EMB 3R/5S.
- **Data integrity:** every FASTQ verified by MD5 against the ENA-reported
  checksum before analysis (16/16 files matched).
- **Reference genome / catalogue:** H37Rv (RefSeq NC_000962.3);
  WHO catalogue v2 (`who_v2_catalog.csv`, 48,151 rows) as shipped with tbtAMR.

## 3. Method & configuration (ISO 15189 §7.3.3 — procedure)
- **Software:** tbtamr 1.0.4 · mutamr 0.0.2 · bwa 0.7.18 · samtools/bcftools 1.20
  · freebayes 1.3.8 · delly 1.2.8 · snpEff 5.2 · OpenJDK 25 · Python 3.14.
  Full package manifest retained (`env_tbtamr.txt`, 80 packages).
- **Pipeline (per `mutamr.log`):** bwa-mem alignment → samclip/markdup →
  freebayes SNP/indel calling (parallel, `-q13 -m60 -F0.1`) with depth filter
  `FMT/DP<20` → delly deletion calling → bcftools merge/normalise → snpEff
  annotation → WHO v2 catalogue interpretation + classification.
- **Acceptance thresholds (tool defaults):** minimum depth 20×, minimum variant
  fraction 0.1.
- **Command (per sample):** `tbtamr full --seq_id <id> -1 R1 -2 R2 --threads 8`.
- **Environment note (traceability):** the accredited method runs on x86-64
  Linux. The validation host is Apple-Silicon macOS; bioconda ships no
  osx-arm64 builds for the pinned `delly`/`samtools` versions, so the
  environment was built as **emulated osx-64 under Rosetta 2**. All tool
  versions match the bioconda recipe; only the CPU architecture layer differs.
  This is documented as a deviation from the reference platform.

## 4. Analytical performance (ISO 15189 §7.3.4 — performance characteristics)
Reference-standard = phenotype; resistance = positive class. n=8 per drug.

| Drug | Sensitivity (95% CI) | Specificity (95% CI) | PPV | NPV | Concordance |
|---|---|---|---|---|---|
| Isoniazid | 100% (57–100) | 100% (44–100) | 100% | 100% | 8/8 |
| Rifampicin | 100% (51–100) | 75% (30–95) | 80% | 100% | 7/8 |
| Ethambutol | 100% (44–100) | 100% (57–100) | 100% | 100% | 8/8 |
| **Overall** | **100% (76–100)** | **92% (65–99)** | 92% | 100% | **23/24** |

- **Diagnostic sensitivity (very major error rate):** 100% / 0% — no
  phenotypically resistant isolate was called susceptible for any drug.
- **Diagnostic specificity (major errors):** one RIF major error (see §5).
- **Reproducibility:** the smoke-test isolate (ERR4813225) was run
  independently as the deliverable-1 end-to-end run and gave an identical
  pan-susceptible call; all runs exited status 0.
- **Analytical sensitivity / limit of detection:** governed by the 20× depth
  threshold; all isolates exceeded it comfortably (36–335× mean depth,
  ≥99% genome coverage), so LoD was not a limiting factor here.
- **CIs are Wilson intervals; they are wide by design at n=8** — point
  estimates are reported for demonstration, not certification.

## 5. Discordance analysis (ISO 15189 §7.3.4 / §7.4 — troubleshooting)
**1 discordant call of 24.** ERR4811536, rifampicin: genomic **R**, phenotypic
**S**. tbtAMR reported `rpoB p.His445Leu` (allele fraction 0.99; WHO v2 grading
"Associated with resistance"; called from 335× depth). The phenotype was
Susceptible at RIF MIC 0.5 mg/L (borderline, at/near ECOFF). rpoB codon-445
substitutions are archetypal **"disputed"/borderline** RIF mutations that confer
low-level MIC elevations frequently scored Susceptible by broth microdilution
yet are genuine, outcome-relevant resistance determinants. **Assessment:** a
false-susceptible *phenotype* near the breakpoint, not a tbtAMR error; the
genomic call is catalogue-correct and clinically cautious. No corrective action
against the method is indicated.

## 6. Traceability & records (ISO 15189 §7.3.5, §8.4)
Every result is reproducible from retained artifacts: sample manifest with
accessions + MD5s; installation/environment record with the platform deviation;
complete per-sample command logs (`mutamr.log`); annotated VCFs; raw 15-drug
tbtAMR output; tidy genomic-vs-phenotype matrix; performance table with CIs;
and this summary. Software and catalogue versions are pinned and captured.

## 7. Conclusion (within validation-exercise scope)
On an independent 8-isolate public panel, the tbtAMR genomic DST workflow
reproduced first-line susceptibility phenotypes with **100% sensitivity** for
resistance detection and **95.8% overall categorical agreement** (23/24). The
single discordance is an expected biological genotype–phenotype discrepancy at a
disputed rpoB locus, attributable to the phenotypic reference method rather than
the genomic method. Results are **consistent with** the published, accredited
tbtAMR performance, within the wide confidence limits of a small panel.

## 8. Limitations (mandatory scope statement)
1. **Demonstration scale (n=8):** confidence intervals are wide; this exercise
   is **not powered** to certify performance to a clinical/accreditation
   threshold.
2. **Pyrazinamide not validated:** no PZA phenotype in the CRyPTIC dataset.
   Second-line drugs were not validated (out of agreed scope).
3. **Reference-data overlap:** CRyPTIC isolates contributed to WHO v2 catalogue
   development; genomic calls are therefore not fully independent of the
   reference catalogue. An orthogonal, catalogue-naïve cohort would be needed
   for an unbiased estimate.
4. **Platform deviation:** validated under osx-64 Rosetta emulation, not the
   accredited x86-64 Linux platform (tool versions identical).
5. **Scope:** analytical/method-validation exercise only. **Not** a clinical
   release, not patient-reportable, and not a substitute for locally accredited
   verification. Any clinical use requires validation by a qualified laboratory
   under its own accredited quality system.
