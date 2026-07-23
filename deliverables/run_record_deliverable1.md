# Deliverable 1 — tbtAMR end-to-end run record

**Purpose.** Demonstrate installation and a complete, reproducible single-sample
run of MDU-PHL tbtAMR (genomic drug-susceptibility prediction for
*M. tuberculosis*), with a full audit trail. Method-validation exercise — not a
clinical release.

## 1. Sample
| Field | Value |
|---|---|
| Sample (run accession) | **ERR4813225** |
| ENA sample | ERS5303385 |
| CRyPTIC UNIQUEID | site.05.subj.LS-0798.lab.MA-05826-18.iso.1 |
| Platform / layout | Illumina, paired-end |
| Read pairs | 1,409,740 |
| Phenotype (CRyPTIC, HIGH-quality binary) | INH-S, RIF-S, EMB-S (pan-susceptible, first-line) |
| Chosen because | smallest panel isolate; pan-S → clean positive control for a "no resistance" call |

### Input integrity (MD5, verified against ENA record)
```
ERR4813225_1.fastq.gz  9d5bfc102763507094f90884e0ad9be0
ERR4813225_2.fastq.gz  7ba547ff006ffda9b9fe6a4ce6b6a7e6
```

## 2. Command
```bash
# environment: emulated osx-64 conda env at /tmp/tbenv (see install_log.md);
# run_tbtamr.sh sets HOME, JAVA_HOME, PATH, MAMBA_ROOT_PREFIX.
run_tbtamr.sh tbtamr full \
    --seq_id ERR4813225 \
    -1 ERR4813225_1.fastq.gz -2 ERR4813225_2.fastq.gz \
    --threads 8 --ram 8 --keep
```
Defaults used: `min_depth=20`, `min_frac=0.1`. Catalogue: the bundled
`who_v2_catalog.csv` (WHO catalogue v2; the tool labels it `who_2024`).

## 3. Pipeline actually executed (from mutamr.log)
Reference: `Mtb_NC000962.3.fa` (H37Rv, RefSeq NC_000962.3).

1. **Align** — `bwa mem -T 50 -Y -M -R '@RG…'` → `samclip --max 10` →
   `samtools sort/fixmate/markdup -r` → sorted, dedup BAM.
2. **Coverage** — `samtools coverage` → `*_stats.txt`.
3. **SNPs/indels** — `freebayes-parallel` (15 chunks, `-q 13 -m 60 -F 0.1
   --haplotype-length -1`) → filter `bcftools view -c1 | norm | filter FMT/DP<20
   | filter INFO/SAR>0 && SAF>0`.
4. **Structural variants** — `delly call -t DEL` → `bcftools view -c2`,
   drop events ≥100 kb.
5. **Merge + normalise** — `bcftools concat -aD (delly, snps) | norm -m -both`.
6. **Annotate** — `snpEff ann … Mycobacterium_tuberculosis_h37rv`.
7. **Interpret** — extract variants, match against WHO v2 catalogue, apply
   `interpretation_criteria.csv` + `classification_criteria.csv`, generate linelist.

## 4. Result
- **Predicted first-line resistance: none — "No first-line drug resistance."**
- All 15 reported drugs → **Susceptible**. Isoniazid, rifampicin, ethambutol,
  pyrazinamide all "Susceptible" (no reportable mechanism).
- Uncertain-grade variants (e.g. `embB_p.Pro731Leu (Uncertain)`) are correctly
  relegated to "Susceptible (not reportable)" — i.e. not counted as resistance.
- **Concordant with the pan-susceptible CRyPTIC phenotype.**

### Sequencing QC (samtools coverage)
| Metric | Value |
|---|---|
| Genome coverage | 99.06 % |
| Mean depth | 39.1× |
| Mapped reads | 1,142,282 |
| Mean MAPQ | 59.2 |

Depth (39×) comfortably exceeds tbtAMR's `min_depth=20`.

## 5. Runtime & exit
- Wall time ≈ 60 s (8 threads); **exit code 0**.

## 6. Output files retained (in `smoke/ERR4813225/`)
`ERR4813225.bam(.bai)`, `ERR4813225.raw.snps.vcf`, `ERR4813225.snps.vcf.gz`,
`ERR4813225.delly.bcf/.vcf.gz`, `ERR4813225.concat.vcf.gz`,
`ERR4813225.annot.vcf.gz` (snpEff-annotated), `ERR4813225_variants.csv`,
`ERR4813225_stats.txt`, `tbtamr_results.csv` (all 15 drugs),
`tbtamr_linelist_report.csv`, plus `mutamr.log` / `tbtamr.log` (command traces).

## 7. Software versions
tbtamr 1.0.4 · mutamr 0.0.2 · bwa 0.7.18 · samtools/bcftools 1.20 ·
freebayes 1.3.8 · delly 1.2.8 · snpEff 5.2 · openjdk 25.0.2 · python 3.14.6.
Catalogue: WHO v2 (`who_2024`). See `env_tbtamr.txt` for the full 80-package list.
