# Resume Tailor — UX Design Doc

**Designer:** Staff Product Designer
**Status:** Draft v0.1
**Last updated:** 2026-10-17

---

## 1. The design bet

We are betting that the side-by-side comparison view carries the entire magical value proposition of the product. Rather than hiding original text or providing an undifferentiated wall of AI prose, presenting an unambiguous 1:1 diff between "What you had" and "How to present it" builds instant user confidence and triggers immediate copy actions.

## 2. The defining interaction

User clicks the prominent "Tailor Bullets" button. The button enters a subtle pulsing progress state while retaining input contents intact. Within 2.5 seconds, the input pane smoothly shifts or condenses, and the side-by-side comparison cards animate into view: on the left sits each original resume bullet in muted tones; on the right, the tailored bullet glides in with crisp high-contrast typography, an active verb highlight, and an "Impact Breakdown" tag. Clicking any tailored card's "Copy" button produces an immediate checkmark micro-animation and temporary "Copied!" pill. Total cycle feels like an effortless professional appraisal.

## 3. Screen inventory

- **Workspace Screen (Single Page)** — Hosts both the side-by-side input panes (Resume + Job Description) and transitions into the interactive side-by-side comparison results view.

## 4. Screen-by-screen specs

### Workspace Screen

**Purpose:** Provide a clean, frictionless interface to input resume text alongside target job specifications and review immediate side-by-side tailored bullets with one-click copy options.

**Layout (top to bottom, or left to right):**
1. **Header Bar** — Minimalist wordmark ("Resume Tailor"), brief subtitle ("Transform passive bullets into quantified impact"), and an optional "Clear" reset action.
2. **Input Zone (Split Two-Column Grid)**:
   - **Left Column:** "Your Current Resume" textarea with clear placeholder guidance ("Paste your resume summary or bullet points here...").
   - **Right Column:** "Target Job Description" textarea with clear placeholder guidance ("Paste key responsibilities and requirements here...").
3. **Action Bar** — Centered prominent CTA button ("Tailor Bullets") flanked by token/character counters and sample data helper links ("Load sample").
4. **Results Zone (Comparison Matrix)** — Appears directly below action bar upon generation:
   - **Header Sub-bar:** Summary banner ("N bullets upgraded") with a global "Copy All Tailored Bullets" button.
   - **Bullet Pair Cards (Vertical Stack of Side-by-Side Cards):**
     - Left Half: Original bullet text in neutral slate container.
     - Right Half: Tailored bullet text in elevated card container featuring highlighted action verbs, quantified metrics, an "Impact Breakdown" tag, and a dedicated "Copy" button.

**Key interactions:**
- Paste text into both inputs → CTA button illuminates and enables.
- Click "Load sample" → Auto-populates realistic engineer or marketer resume bullets and job posting to demonstrate value in 1 click.
- Click "Tailor Bullets" → Inputs disable gracefully, button displays loading spinner with progress microcopy ("Analyzing role requirements...", "Quantifying impact..."), results area renders smoothly.
- Click "Copy" on individual card → Copies specific bullet string to clipboard, swaps icon to checkmark with green badge for 1.5s.
- Click "Copy All" → Copies newline-delimited list of all tailored bullets to clipboard with confirmation toast.

**States:**
- **Default:** Clean dual textareas, disabled CTA button waiting for input in both fields.
- **Empty / first-time:** Both textareas show helpful placeholder prompts and a visible "Try a quick example" link above the action bar so users can preview the experience in zero keystrokes.
- **Loading:** Button shows spinner with phased status text; previous results (if any) dim slightly with a subtle skeleton shimmer overlay.
- **Error:** Inline non-modal error alert banner below the action bar explaining issues clearly (e.g., "Please provide at least one bullet point in the resume field" or "Could not connect to generator. Please check your connection and retry."). Inputs remain completely intact so no work is lost.
- **Edge / "too much":** If user pastes a 10-page document (over 4,000 words), gentle amber badge advises: "Large text detected — focusing on the top 10 most relevant bullets for optimal speed." Scrollbars remain internal to containers.

## 5. The user journey

A user lands on the page after encountering a promising job post on LinkedIn. The screen greets them with two generous, welcoming text boxes. Rather than typing from scratch, they paste 5 bullet points from their current resume into the left box, and paste the job requirements into the right box. The "Tailor Bullets" button immediately glows with high contrast.

They click "Tailor Bullets". For 2 seconds, a gentle status shimmer confirms the system is mapping their bullets against the job's core verbs and requirements. The comparison section snaps smoothly below: each row shows their original phrase alongside a rewritten, muscular alternative equipped with a bold verb, clear scope, and metric placeholder.

Surprised by how much stronger their own experience sounds, they click "Copy All", switch back to their document, and paste the upgraded bullets directly into their application.

## 6. Component & visual notes

- **Typography:** Crisp modern sans-serif (Inter or system UI sans font stack) with monospace accents for tags and metrics to convey technical precision.
- **Color:** Clean editorial palette — deep slate/charcoal text on clean warm white/light gray surfaces, with an energetic indigo/electric blue accent for primary action and emerald green for copy confirmations.
- **Motion:** Fast, purposeful transitions (150ms-250ms ease-out). No slow decorative animations; elements slide in with tight, crisp settling.
- **The signature visual:** The dual-pane comparison card with the tactile "Impact Breakdown" pill badge (e.g., `⚡ Action Verb Upgraded` or `📈 Metric Quantified`) anchored at the top-right of each tailored card.
- **Microcopy voice:** Direct, sharp, and encouraging. Examples: "Tailor Bullets", "Matching qualifications...", "Copied to clipboard!", "Try sample data".

## 7. Accessibility & inclusion

- **Screen readers:** Both textareas have explicit `aria-label` and `aria-describedby` attributes. Comparison results announce bullet counts and changes via `aria-live="polite"` regions.
- **Keyboard navigation:** Full keyboard tab flow from Left Input → Right Input → CTA → Comparison Cards → Copy Buttons. Enter/Space keys trigger copy actions.
- **Contrast & sizing:** All text meets WCAG AA standards (minimum 4.5:1 contrast). Tap targets on buttons are minimum 44x44px.
- **Network limits:** Total asset bundle is ultra-lean (vanilla CSS/JS, zero heavy framework overhead), ensuring fast load even on constrained 3G connections.

## 8. What we are NOT designing

- **No multi-step modal wizards** — All interaction remains on a single, continuous canvas.
- **No rich-text WYSIWYG editor or formatting toolbars** — Bolding and styling controls are excluded to avoid distraction from plain bullet writing.
- **No document preview canvas or faux-A4 sheet rendering** — We are not mimicking Word or Acrobat.
- **No user profile, history, or saved resumes sidebar** — Every session is fresh and focused.
- **No dark/light theme switchers** — Ships with an optimized, high-contrast, accessible light theme for v1.

## 9. Open design questions

- [ ] Should the comparison layout switch from side-by-side columns to stacked cards on narrow mobile viewports (<768px)?
- [ ] Should users be allowed to click into tailored bullets and inline-edit them before copying?

## 10. Handoff to engineering

The side-by-side comparison alignment and clipboard copy feedback are the critical UI interactions — ensure card heights align or flex gracefully between original and tailored variants without jumping. The entire frontend should be lightweight vanilla HTML/CSS/JS without heavyweight framework build steps.
