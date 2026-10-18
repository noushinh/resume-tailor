# Resume Tailor — Product Design Doc

**Author:** Staff Product Manager
**Status:** Draft v0.1
**Last updated:** 2026-10-17
**One-liner:** Paste your resume and a job description to instantly get rewritten bullet points with quantified impact and punchy action verbs.

---

## 1. The user & the moment

- **Who:** An active job seeker applying to multiple roles who feels their resume sounds generic, passive, and disjointed from specific job descriptions.
- **When:** It is 10:30 PM on a weekday, they just found an exciting role on a job board, and they are dreading spending two hours manually tweaking resume phrasing and guessing ATS keywords.
- **Why now:** Most AI tools generate entire generic cover letters or hallucinated multi-page resumes that job seekers don't trust. Job seekers want surgical, credible upgrades to their actual bullets that match the target role without fluff.

## 2. The contract (I/O)

- **Input:** Two plain text boxes — one for pasting existing resume bullet points/text, and one for pasting the target job description text.
- **Output:** An instant, side-by-side comparison displaying original bullets directly next to rewritten, high-impact bullets tailored to the target role with quantified metrics and strong action verbs.
- **The loop:** One-shot transformation per job posting (paste resume + paste job description → click "Tailor Bullets" → compare original vs. tailored bullets → 1-click copy tailored results).

## 3. The magical moment

> "Seeing my boring 'Responsible for managing client emails' line instantly turn into 'Spearheaded client communication workflows across 15 accounts, cutting response latency by 40%' side-by-side made me realize this is 10x better than anything I would have spent all night writing."

## 4. Scope: what we ARE building (v1)

- Single web screen with two side-by-side or stacked text inputs (resume text + target job description).
- One primary "Tailor Bullets" action button triggering immediate LLM bullet rewriting.
- Structured side-by-side diff/comparison view showing each original bullet paired with its tailored version, highlighting the action verb and impact metric changes.
- Quick 1-click "Copy All" and individual bullet "Copy" buttons to easily paste bullets back into a document.
- In-place retry or edit capability to tweak inputs and regenerate on demand.

## 5. Scope: what we are NOT building

- **No user authentication or accounts** — Zero login friction; all data processing is transient or local to the browser session.
- **No PDF or Word document parsing** — Plain text only; eliminates document formatting bugs, parsing errors, and upload security overhead for v1.
- **No multi-page resume builder or PDF export** — We are not a layout tool; we provide surgical text upgrades users paste into their own templates.
- **No cover letter generation** — Defers to staying laser-focused on the highest-leverage asset (bullet points).
- **No interview preparation or mock Q&A** — Out of scope; preserves the 45-minute lean build discipline.
- **No persistent remote database or cloud history** — Keeps privacy pristine and architecture minimalist.

## 6. The signature detail

The "Impact Breakdown" tag on each tailored bullet. Each rewritten bullet displays a subtle, tactile badge indicating the primary enhancement made (e.g., `⚡ Action Verb Upgraded`, `📈 Metric Quantified`, `🎯 Keyword Matched: Kubernetes`). It provides instant transparency on why the rewrite is stronger, turning opaque AI output into a deliberate coaching upgrade.

## 7. Success: how we know it worked

- **Primary:** ≥70% of generation sessions result in the user clicking either individual bullet "Copy" or "Copy All".
- **Secondary (max 2):** 
  - Median time from landing on the page to copying tailored bullets is under 90 seconds.
- **What we're NOT measuring:** Total registered accounts (none exist), session duration (shorter is better), pageview counts.

## 8. Open questions

- [ ] How should the parser handle unstructured pasted resume text (e.g., if the user pastes paragraphs instead of cleanly delineated bullet points)?
- [ ] What is the optimal number of bullets to rewrite in a single pass to preserve latency under 4 seconds without truncation?

## 9. Handoff

- **For UX:** The side-by-side comparison must feel immediately legible and scannable without horizontal scrolling fatigue on standard desktop viewports.
- **For Eng:** End-to-end bullet parsing and structured generation latency must stay under 3.5s to ensure the comparison feels instantaneous.
