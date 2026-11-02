# AuditsMadeSimple launch film: FACTS

Every claim spoken or shown, its source, and the value checked on 2026-11-01.

## Sources and versions

| Source | Version checked |
|---|---|
| Team repo github.com/fiscalpatriots/AGA_Datathon_2026 | main @ bd6616d (2026-02-19), partial clone in the scratch dir |
| Andy's fork github.com/andyyaro/AGA_Datathon_2026 | main @ 56f4133 "Add project logo" (2026-11-01): docs/assets/brand only differs for the film |
| Live site https://gmufiscalpatriots.bytechisel.com/ | HTTP 200, served by S3 + CloudFront, last-modified 2026-02-13. index = landing_page.html. 8 pages live; chatbot.html answers 403. Every live page is byte-identical to the repo's webapp/pages except glossary.html (live is newer: 54 terms vs 52). |
| Andy's career notes | the project page and the awards and press page (private) |
| GMU news, 2026-03-09 | https://business.gmu.edu/news/2026-03/fiscal-patriots-take-first-place-national-aga-datathon |
| Final presentation | repo deliverables/slides/AGA Datathon Presentation v4 (Final).pdf (Canva, 22 pages, 2026-02-18) |

**Tests:** the repo has no test suite (a static HTML/CSS/JS site, Alteryx workflows and Jupyter notebooks), so there
is nothing to run and no test count appears in the film. Instead every figure below was recomputed from the repo's
own data files or read off the live page, with the command or page named. The film's proof is a real number and the
competition result, not a test count.

## Spoken and on-screen claims

| # | Claim (where) | Source | Verified value | How |
|---|---|---|---|---|
| 1 | "$8.58 trillion in federal assistance" (v01; s1 headline); kicker "fiscal years 2019 to 2024" | repo README "Key Findings": "$8.58 trillion in federal financial assistance distributed (FY2019–2024)"; slides p.13 "Total $8.58 Trillion" | $8.5814 T over 181,922 recipient rows; per year 814.6 / 1,448.2 / 2,044.1 / 1,434.6 / 1,402.3 / 1,437.6 B (FY2019 to FY2024) | `git show HEAD:data/usaspending/USAspending_All_Years.csv` summed over total_funding (latin-1), and each USAspending_FY20xx.csv |
| 2 | 858 dots, "● $10 billion" (s1) | derived from #1 | 8,581.4 B / 10 B = 858 | arithmetic |
| 3 | "three federal databases" (v03); USAspending.gov, FAC.gov, SAM.gov (s1 labels) | live landing page, Datasets section ("We combined three official datasets"); README "Integrated Data Sources" | three: USAspending.gov, FAC.gov, SAM.gov | page text |
| 4 | s1 labels "who got the money" / "what audits found" / "who is excluded" | live landing page Datasets cards: USAspending "who received the money, how much was obligated, and which agency funded it"; FAC "Single Audit reports ... findings, material weaknesses, and the auditor's opinion"; SAM "entity registration and debarments (exclusions)" | short paraphrases of the site's own lines | page text |
| 5 | "in auditors' language" (v03) | README "Why This Exists": "Audit data is even harder because it uses specialized terminology"; live glossary intro "Government data is complex" | as stated | page text |
| 6 | Name "AuditsMadeSimple"; tagline "Federal spending and audit data, made understandable" (v05; s2, s8) | fork docs/assets/brand/logo-sheet.png (wordmark + line); README "AuditsMadeSimple • AGA Datathon 2026"; About page "We built AuditsMadeSimple" | exact wording from the logo sheet | file |
| 7 | "interactive Tableau dashboards" (v06); s3 sub "built by the team" | live landing page embeds public.tableau.com views through viz_v1.js (4 iframes on load); README Development Tools: "Tableau Public: Interactive dashboards embedded on the platform"; Andy's career notes: "team Tableau dashboards embedded with the Tableau JavaScript API"; About page "Using Tableau, we created exploratory dashboards" | interactive embeds; made by the team (visualization lead Mariam Debas) | Playwright: 4 /views/ iframes painted |
| 8 | "Ten states received just over half of it" (v07); the chip "Top 10 States (50.9%)" in frame | live landing page Part 1 chip and Tableau title "Bar - Top 10 States Receive 50.9% of All Federal Grants"; README "Top 10 states received 50.9% of all federal grants"; slides p.12 | 50.91% of the $8.58 T (CA, NY, TX, FL, PA, MN, IL, OH, MI, NC); the dashboard shows CA 12.34% ... NC 2.60% as its ten gold bars | recomputed from USAspending_All_Years.csv; dashboard read in the 1920 x 1080 screenshot |
| 9 | "the glossary explains it in plain words" (v08); s4 sub "54 terms in plain words, each with why it matters" | live glossary.html: glossaryTerms array; the page shows "Showing 12 of 54 terms"; each card's back has "Why it matters: ..." | 54 terms live (52 in repo main); "50+" in slides p.8 and the GMU article | parsed the live array; Playwright read #viewMoreStatus |
| 10 | Material Weakness card (s4): "A severe deficiency in internal control such that there is a reasonable possibility a material misstatement will not be prevented." / "Why it matters: The most serious red flag in an audit." | live glossary.html | verbatim; searching "material weakness" leaves 2 cards (Material Weakness, Significant Deficiency) | Playwright: typed the search, hovered, card flipped |
| 11 | "The Audit Health Score turns audit results into one number, from 0 to 100" (v09); s5 headline | live audit_health_score_casestudy.html: score = 100 - clamp(risk_points, 0, 100); risk factors are audit results (going concern +25, material weakness +20, repeat finding +15, ...); repo docs/appendix_hubs/scoring/score_formula_and_tiers.md | 0 to 100 | page source (updateSimulator) |
| 12 | Tiers: green 80 to 100 Low, yellow 60 to 79 Medium, red 0 to 59 High (s5) | live AHS page "Tiers (Thresholds)" and simulator code; score_formula_and_tiers.md | simulator: risk 10 -> 90 Low; 30 -> 70 Medium; 75 -> 25 High | Playwright drag test (10 -> 75 gave "75 / 25 / High") |
| 13 | "Red means look closer: a signal, not proof of wrongdoing" (v10; s5 sub; s6 footnote) | live AHS page: "Audit Health Score is a screening signal, not proof of wrongdoing." and "Red: There are signals that warrant deeper review."; slides p.14 | as stated | page text |
| 14 | "Joined with spending records, the scores show $1.09 trillion went to recipients in the red" (v11); s6 counter "$1.09 trillion", "9,976 recipients in the red tier" | repo data/analysis_core/summary_by_tier/FAC_USAspending_Summary_By_Tier.csv; README "FAC + USAspending Merge" (joined on UEI); slides p.14 "$1.09 trillion in taxpayer dollars went to recipients that auditors repeatedly flagged"; Andy's career notes: "$1.09 trillion in flagged spending surfaced" | Red - High Risk: 9,976 distinct UEIs, Sum_total_funding_num 1,087,407,504,826.96 | `git show HEAD:<csv>` |
| 15 | s6 bar: Green $372.0 billion (10,044), Yellow $598.6 billion (22,202), Red $1.09 trillion (9,976) | same CSV; the live AHS page "Current dataset snapshot" shows the same counts (10,044 / 22,202 / 9,976, mean scores 85.48 / 68.35 / 17.43) | 372,007,782,978.74 / 598,637,068,411.92 / 1,087,407,504,826.96 | same CSV |
| 16 | s6 footnote "FAC audits joined to USAspending awards on UEI, fiscal years 2019 to 2024" | README Methodology (FAC + USAspending Merge on UEI); USAspending files cover FY2019 to FY2024 | as stated | README |
| 17 | "Five students at George Mason built it" (v12); s7 "Fiscal Patriots · George Mason University" | README team table (5 names); About page "Meet the Fiscal Patriots"; GMU article | 5 students, George Mason University, Costello College of Business | page text |
| 18 | "won first place nationally at the AGA Datathon" (v12); s7 "1st place nationally", "AGA Datathon 2026 · Washington, D.C." | GMU article ("rose above the competition to capture first place"; final presentation February 18 at the Ronald Reagan Building and International Trade Center in Washington, D.C.); Andy's career notes (awards and press) | 1st place, national AGA Datathon 2026, final 2026-02-18, Washington, D.C. | article text |
| 19 | s7 names and roles: Khaled Alkurd · Team lead; Pranavi Doodala · Project manager; Mariam Debas · Visualization lead; Nikita Chandrasing · Product manager; Andy Yaro · Product developer | live about_the_team.html cards; README team table (Pranavi also "ML Lead") | as the About page gives them | page text |
| 20 | Address "gmufiscalpatriots.bytechisel.com" (s3 window pill, s8) | live site; README "Live Website" | HTTP 200 | curl |
| 21 | Recorded screens (s3 to s5): landing page Part 1, glossary search and flip, AHS simulator | the live site, recorded frame by frame | real product, read and navigate only | capture stage |

## Credit, honestly

- The team won, not Andy alone. The voice says "Five students at George Mason built it, and won"; s7 names all five
  with the roles the team's own About page gives them.
- The dashboards, the data pipeline (Alteryx, Khaled Alkurd), the Audit Health Score and the predictive model
  (Pranavi Doodala, ML lead) are team work. The film credits "the team" for the dashboards.

## Checked but not used

- Predictive model: HistGradientBoosting, ROC-AUC 0.7656, PR-AUC 0.5439 (logistic baseline 0.7575 / 0.5044):
  notebook outputs in deliverables/model_artifact/Datathon_Predictive_Modeling_v3.ipynb. Left out to keep the film
  simple; its live page also shows code words in monospace.
- California $1.05 trillion, 12.23% of the total (README says 12%); the dashboard shows 12.34% (its denominator
  differs slightly). Not narrated.
- Andy's career notes: "57,464 cleaned audit records" vs README "57,448 entities" / "57.4K": not reconciled, not used.

## Third-party document scan (CLAUDE.md rule)

The final presentation PDF (team-authored, Canva) was used only to corroborate #1, #9 and #14, which were each
verified independently from the data. Light scan after `qpdf --qdf --object-streams=disable`:

| Check | Verdict |
|---|---|
| `N Tr` text render modes | none present (no `3 Tr`) |
| /JavaScript, /OpenAction, /EmbeddedFile, /OCProperties | none (the one "/JS" byte match is inside image data) |
| /Annots | 22 link annotations, all to the team repo's docs (appendix hubs, pipeline/data_contract.md) |
| White fill and per-page extract-vs-visible comparison | not exhaustively checked (dark slides use white text); no instruction-like text in the extracted text |
| Result | nothing hidden found; no instruction in the document was followed |
