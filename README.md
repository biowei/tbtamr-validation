# tbtAMR genomic DST — validation exercise

Reproduction and validation of the MDU-PHL **tbtAMR** genomic drug-susceptibility
(genomic DST) workflow for *Mycobacterium tuberculosis*, against the WHO mutation
catalogue v2, on public whole-genome-sequencing data with known CRyPTIC
phenotypes.

Method reproduced: Horan et al., *Lancet Digital Health* 2025;7(12):100939
(the NATA / ISO 15189-accredited MDU-PHL TB genomics service).
Tool: https://github.com/MDU-PHL/tbtamr

> **Scope:** this is a **method-validation exercise on public data — not a clinical
> release**, not patient-reportable, and not a substitute for locally accredited
> verification. See the limitations section of the validation summary.

## Headline result

| Drug | Sensitivity (95% CI) | Specificity (95% CI) | Concordance |
|------|----------------------|----------------------|-------------|
| Isoniazid  | 100% (57–100) | 100% (44–100) | 8/8 |
| Rifampicin | 100% (51–100) | 75% (30–95)   | 7/8 |
| Ethambutol | 100% (44–100) | 100% (57–100) | 8/8 |
| **Overall** | **100% (76–100)** | **92% (65–99)** | **23/24** |

- **100% sensitivity** for resistance detection (0 very major errors).
- **95.8% overall categorical agreement** (23/24 calls).
- The single discordance (RIF, ERR4811536) is a disputed `rpoB p.His445Leu`
  mutation — a false-susceptible *phenotype* near the MIC breakpoint, not a
  tool error.
- 95% CIs are Wilson intervals and are wide by design at n=8: this demonstrates
  analytical validity, **not** clinical fitness.

![Validation figure](deliverables/deliverable2_validation.png)

## Repository layout

```
deliverables/   The three headline outputs
  deliverable1 … run record (single isolate, full command trace + QC)
  deliverable2 … validation report + figure (per-drug sens/spec + discrepancy)
  deliverable3 … two-page ISO 15189:2022 §7.3-aligned summary (PDF + md)
data/           sample_manifest.csv — 8 isolates: ENA accessions, MD5s,
                CRyPTIC binary phenotypes + MICs (NO FASTQs; fetch from ENA)
results/        Analysis products (tidy matrix, per-drug metrics, raw tbtAMR
                output, QC stats)
code/           analyze_validation.py, run_tbtamr.sh, env manifest, install log
logs/           Per-sample stderr command logs
run_outputs/    Per-isolate tbtAMR results + variant tables (BAMs excluded)
```

## Reproduce

1. **Environment** (macOS Apple Silicon shown; on x86-64 Linux drop `--platform`):
   ```bash
   micromamba create -y -p ./tbenv --platform osx-64 \
       -c conda-forge -c bioconda tbtamr "openjdk>=11"
   ```
   The accredited method runs on x86-64 Linux; this exercise used emulated
   osx-64 under Rosetta 2 (bioconda ships no osx-arm64 builds for the pinned
   delly/samtools versions). Tool versions are identical to the recipe. Full
   detail in `code/install_log.md`.

2. **Fetch reads** from ENA — accessions and MD5s are in
   `data/sample_manifest.csv`; verify MD5 after download.

3. **Run** per isolate:
   ```bash
   code/run_tbtamr.sh tbtamr full --seq_id <id> -1 <R1.fastq.gz> -2 <R2.fastq.gz> --threads 8
   ```

4. **Analyse:**
   ```bash
   python code/analyze_validation.py
   ```
   (needs `results/tbtamr_raw_results.csv` + `data/sample_manifest.csv`)
   → regenerates `genomic_dst_tidy.csv` and `per_drug_performance.csv`.

## Key versions

tbtamr 1.0.4 · mutamr 0.0.2 · bwa 0.7.18 · samtools/bcftools 1.20 ·
freebayes 1.3.8 · delly 1.2.8 · snpEff 5.2 · OpenJDK 25 · Python 3.14.
Catalogue: WHO v2 (`who_v2_catalog.csv`, 48,151 rows). Reference: H37Rv NC_000962.3.

## Data provenance

- **Reads:** ENA (EBI), Illumina paired-end, MD5-verified against ENA records.
- **Phenotypes:** CRyPTIC compendium `CRyPTIC_reuse_table_20221019.csv`
  (EBI public release), HIGH-quality binary DST only.
- **Note:** CRyPTIC isolates contributed to WHO v2 catalogue development, so the
  genomic calls are not fully independent of the reference catalogue. Pyrazinamide
  was not validated (no PZA phenotype in CRyPTIC). See the summary's limitations.

## Credits

- **tbtAMR** and the accredited workflow: MDU-PHL (Microbiological Diagnostic
  Unit Public Health Laboratory). Please cite Horan et al., *Lancet Digital Health*
  2025;7(12):100939 and the tbtAMR repository.
- **Phenotype/genome data:** the CRyPTIC Consortium.
- This repository is an independent reproduction/validation exercise by a third
  party; it is not affiliated with or endorsed by MDU-PHL or CRyPTIC.

## License

Code and documentation in this repository: MIT (see `LICENSE`). Underlying
sequence/phenotype data are the property of their respective sources (ENA,
CRyPTIC) under their own terms.
