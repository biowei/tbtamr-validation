# How to publish this repo to GitHub

This folder is ready to push as-is. Two prerequisites before you post the link:

1. **Fill in placeholders:**
   - `LICENSE` — replace `<YOUR NAME OR ORGANISATION>`.
   - `deliverables/deliverable3_iso15189_summary.md` (and the PDF) — the analyst
     field reads "Claude Science (automated)" and the scope owner is blank.
     Set these to your name/institution before publishing.
     (Ask the assistant to re-render the PDF once you've edited the `.md`.)

2. **Confirm you're happy sharing** the CRyPTIC accessions + your analysis. All
   inputs are public data; no raw FASTQs are included (`.gitignore` blocks them).

## Publish (GitHub CLI — easiest)

```bash
cd tbtamr-validation
git init -b main
git add .
git commit -m "tbtAMR genomic DST validation exercise (public data)"
gh repo create tbtamr-validation --public --source=. --push
```

## Publish (plain git, no gh)

Create an empty repo named `tbtamr-validation` on github.com first (no README),
then:

```bash
cd tbtamr-validation
git init -b main
git add .
git commit -m "tbtAMR genomic DST validation exercise (public data)"
git remote add origin https://github.com/<your-username>/tbtamr-validation.git
git push -u origin main
```

Your shareable link is then:
`https://github.com/<your-username>/tbtamr-validation`

The README renders as the landing page, and GitHub shows the validation figure
inline. Link that URL from your LinkedIn post; attach
`deliverables/deliverable3_iso15189_summary.pdf` to the post itself for the
readable two-page story.
