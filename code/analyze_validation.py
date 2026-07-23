#!/usr/bin/env python3
"""
Reproduce Deliverable 2 analysis: parse tbtAMR genomic DST calls, join to
CRyPTIC binary phenotypes, compute per-drug sensitivity/specificity with
Wilson 95% CIs, and flag discordances.

Inputs (same directory):
  - tbtamr_raw_results.csv   (collated 15-drug tbtAMR output, 8 isolates)
  - sample_manifest.csv      (accessions, MD5s, CRyPTIC binary phenotypes)
Outputs:
  - genomic_dst_tidy.csv
  - per_drug_performance.csv
"""
import numpy as np, pandas as pd

raw = pd.read_csv("tbtamr_raw_results.csv")
man = pd.read_csv("sample_manifest.csv")

def to_binary(interp):
    s = str(interp).strip().lower()
    if "resistant" in s: return "R"      # "resistant" + "low-level resistant"
    if "susceptible" in s: return "S"    # "susceptible" + "susceptible (not reportable)"
    return "NA"

drug_map = {"INH":"isoniazid","RIF":"rifampicin","EMB":"ethambutol"}  # PZA: no CRyPTIC phenotype
rows = []
for _, r in raw.iterrows():
    sid = r["seq_id"]; mrow = man[man.sample_id==sid].iloc[0]
    for short, full in drug_map.items():
        rows.append(dict(
            seq_id=sid, UNIQUEID=mrow["UNIQUEID"], drug=short,
            genomic_interpretation=r[f"{full} - interpretation"],
            genomic_call=to_binary(r[f"{full} - interpretation"]),
            genomic_mechanism=r[f"{full} - mechanisms"],
            phenotype_call=mrow[f"{short}_BINARY_PHENOTYPE"],
            phenotype_MIC=mrow[f"{short}_MIC"]))
tidy = pd.DataFrame(rows)
tidy["concordant"] = tidy.genomic_call==tidy.phenotype_call
tidy.to_csv("genomic_dst_tidy.csv", index=False)

def wilson(k, n, z=1.96):
    if n==0: return (np.nan, np.nan)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (max(0,c-h), min(1,c+h))

def metrics(sub):
    tp=((sub.genomic_call=="R")&(sub.phenotype_call=="R")).sum()
    tn=((sub.genomic_call=="S")&(sub.phenotype_call=="S")).sum()
    fp=((sub.genomic_call=="R")&(sub.phenotype_call=="S")).sum()
    fn=((sub.genomic_call=="S")&(sub.phenotype_call=="R")).sum()
    n=tp+tn+fp+fn
    sl,sh=wilson(tp,tp+fn); pl,ph=wilson(tn,tn+fp)
    return dict(N=n,TP=tp,TN=tn,FP=fp,FN=fn,
        sensitivity=tp/(tp+fn) if tp+fn else np.nan, sens_lo=sl, sens_hi=sh,
        specificity=tn/(tn+fp) if tn+fp else np.nan, spec_lo=pl, spec_hi=ph,
        PPV=tp/(tp+fp) if tp+fp else np.nan, NPV=tn/(tn+fn) if tn+fn else np.nan,
        concordance=(tp+tn)/n if n else np.nan)

perf=[]
for d in ["INH","RIF","EMB"]:
    m=metrics(tidy[tidy.drug==d]); m["drug"]=d; perf.append(m)
m=metrics(tidy); m["drug"]="OVERALL"; perf.append(m)
pd.DataFrame(perf).to_csv("per_drug_performance.csv", index=False)

print(f"Concordant: {tidy.concordant.sum()}/{len(tidy)}")
print("Discordances:")
print(tidy[~tidy.concordant][["seq_id","drug","genomic_call","phenotype_call","genomic_mechanism"]].to_string(index=False))
