# tbtAMR installation & environment record

## Platform pivot (documented)
- **Host:** macOS 15.4.1, Apple Silicon (arm64), 8 cores / 16 GiB.
- **Blocker on native arm64:** tbtAMR (via mutamr) pins `delly=1.2.8` and older
  builds pin `samtools=1.12`. Bioconda ships these pinned versions for
  `linux-64` / `osx-64` **only** — there is no `osx-arm64` build. A native
  `osx-arm64` solve therefore fails ("delly =1.2.8 does not exist").
- **Resolution:** built an emulated **osx-64** conda environment under Rosetta 2.
  This keeps the run local (user's decision) and is closer to the paper's
  x86-64 Linux environment than native arm64 would have been.

## Environment build
Tool: micromamba (conda-forge + bioconda channels), forced `--platform osx-64`.

```bash
export MAMBA_ROOT_PREFIX=/tmp/tbroot ; export HOME=/tmp/tbhome
micromamba create -y --no-rc --no-env -p /tmp/tbenv \
    --platform osx-64 -c conda-forge -c bioconda tbtamr
# snpEff needs a JRE; add one:
micromamba install -y --no-rc --no-env -p /tmp/tbenv \
    --platform osx-64 -c conda-forge -c bioconda "openjdk>=11"
```

The conda-forge `openjdk` places `java` at `$PREFIX/lib/jvm/bin/java` (not on
`bin`), so runs must set `JAVA_HOME=/tmp/tbenv/lib/jvm` and prepend
`$JAVA_HOME/bin` to PATH. This is encapsulated in `run_tbtamr.sh`.

## Runner wrapper (`run_tbtamr.sh`)
```bash
#!/bin/bash
export HOME=/tmp/tbhome
export JAVA_HOME=/tmp/tbenv/lib/jvm
export PATH=/tmp/tbenv/lib/jvm/bin:/tmp/tbenv/bin:$PATH
export MAMBA_ROOT_PREFIX=/tmp/tbroot
exec "$@"
```

## Verified versions
| Component | Version |
|---|---|
| tbtamr | 1.0.4 |
| mutamr | 0.0.2 |
| delly | 1.2.8 |
| freebayes | 1.3.8 |
| bwa | 0.7.18-r1243 |
| samtools | 1.20 |
| bcftools | 1.20 |
| snpEff | 5.2 |
| openjdk | 25.0.2 (Zulu, LTS) |
| python | 3.14.6 |

## Resistance catalogue (shipped with tbtAMR 1.0.4)
- File: `tbtamr/db/who_v2_catalog.csv` — **WHO mutation catalogue v2**.
- 48,151 rows; includes WHO v2 confidence-grading columns
  ("FINAL CONFIDENCE GRADING", etc.).
- Reference genome for calling: `tbtamr/db/tbtamr.fasta` (H37Rv).
- Default variant thresholds: `min_depth=20`, `min_frac=0.1`.

Full package list: `env_tbtamr.txt` (80 packages).
