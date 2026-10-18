/**
 * Resume Tailor — Frontend Application State Machine & Interactions
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- DOM Elements ---
  const resumeInput = document.getElementById("resume-input");
  const jobInput = document.getElementById("job-input");
  const resumeCounter = document.getElementById("resume-counter");
  const jobCounter = document.getElementById("job-counter");

  const btnTailor = document.getElementById("btn-tailor");
  const btnSpinner = document.getElementById("btn-spinner");
  const btnLabel = document.getElementById("btn-label");
  const btnSample = document.getElementById("btn-sample");
  const btnClear = document.getElementById("btn-clear");
  const btnCopyAll = document.getElementById("btn-copy-all");
  const copyAllLabel = document.getElementById("copy-all-label");

  const loadingIndicator = document.getElementById("loading-indicator");
  const loadingPhrase = document.getElementById("loading-phrase");

  const errorBanner = document.getElementById("error-banner");
  const errorMessage = document.getElementById("error-message");
  const errorDismiss = document.getElementById("error-dismiss");

  const resultsZone = document.getElementById("results-zone");
  const resultsCountBadge = document.getElementById("results-count-badge");
  const roleSummaryText = document.getElementById("role-summary-text");
  const comparisonList = document.getElementById("comparison-list");

  const toast = document.getElementById("toast");
  const toastText = document.getElementById("toast-text");

  // State
  let currentBullets = [];
  let loadingInterval = null;

  const LOADING_PHRASES = [
    "Analyzing role requirements...",
    "Extracting core competencies...",
    "Quantifying metrics & action verbs...",
    "Finalizing side-by-side diff...",
  ];

  // Realistic sample data for instant 1-click test
  const SAMPLE_DATA = {
    resume: `• Managed social media accounts and created marketing content.
• Built user interface for checkout system using React and JavaScript.
• Fixed bugs reported by clients in our web application.
• Worked with backend engineers on REST API integrations.
• Helped onboard new junior developers to the frontend repository.`,
    job: `Senior Frontend Engineer (React, TypeScript, Performance)
Responsibilities:
- Architect and optimize high-throughput React web applications serving millions of users.
- Drive defect resolution and performance tuning to maintain 99.99% frontend uptime.
- Champion code quality, design system consistency, and end-to-end telemetry.
- Mentor engineers and spearhead technical roadmap execution across multidisciplinary teams.`
  };

  // --- Helpers ---
  function updateCounters() {
    const resumeLen = resumeInput.value.length;
    const jobLen = jobInput.value.length;
    resumeCounter.textContent = `${resumeLen.toLocaleString()} chars`;
    jobCounter.textContent = `${jobLen.toLocaleString()} chars`;

    const isValid = resumeInput.value.trim().length >= 20 && jobInput.value.trim().length >= 20;
    btnTailor.disabled = !isValid;
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.classList.remove("hidden");
    errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function hideError() {
    errorBanner.classList.add("hidden");
  }

  function showToast(message) {
    toastText.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 2200);
  }

  function startLoading() {
    hideError();
    btnTailor.disabled = true;
    btnSpinner.classList.remove("hidden");
    btnLabel.textContent = "Tailoring...";
    loadingIndicator.classList.remove("hidden");

    let phraseIndex = 0;
    loadingPhrase.textContent = LOADING_PHRASES[0];
    loadingInterval = setInterval(() => {
      phraseIndex = (phraseIndex + 1) % LOADING_PHRASES.length;
      loadingPhrase.textContent = LOADING_PHRASES[phraseIndex];
    }, 900);
  }

  function stopLoading() {
    btnTailor.disabled = false;
    btnSpinner.classList.add("hidden");
    btnLabel.textContent = "⚡ Tailor Bullets";
    loadingIndicator.classList.add("hidden");
    if (loadingInterval) {
      clearInterval(loadingInterval);
      loadingInterval = null;
    }
    updateCounters();
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function renderComparisonMatrix(data) {
    currentBullets = data.bullets || [];
    resultsCountBadge.textContent = `${currentBullets.length} bullets upgraded`;
    roleSummaryText.textContent = data.role_summary || "";

    comparisonList.innerHTML = "";

    currentBullets.forEach((bullet, index) => {
      const card = document.createElement("div");
      card.className = "comparison-card";
      card.setAttribute("role", "listitem");

      // Format tailored text with action verb highlighted
      const escapedTailored = escapeHtml(bullet.tailored);
      let formattedTailored = escapedTailored;
      if (bullet.action_verb && bullet.action_verb.trim().length > 0) {
        const verb = escapeHtml(bullet.action_verb.trim());
        const regex = new RegExp(`^\\b(${verb})\\b`, "i");
        if (regex.test(formattedTailored)) {
          formattedTailored = formattedTailored.replace(regex, `<span class="verb-highlight">$1</span>`);
        }
      }

      const keywordTag = bullet.matched_keyword 
        ? `<span class="tag-keyword" title="Matched Job Requirement">🎯 ${escapeHtml(bullet.matched_keyword)}</span>` 
        : "";

      card.innerHTML = `
        <div class="side-original">
          <div class="side-label-mobile">Original Bullet</div>
          <p class="original-text">${escapeHtml(bullet.original)}</p>
        </div>
        <div class="side-tailored">
          <div>
            <div class="tailored-meta">
              <span class="tag-impact">${escapeHtml(bullet.impact_tag || "⚡ Action Verb Upgraded")}</span>
              ${keywordTag}
            </div>
            <p class="tailored-text">${formattedTailored}</p>
          </div>
          <div class="tailored-actions">
            <button class="btn-copy-card" data-index="${index}" type="button" aria-label="Copy this tailored bullet">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span>Copy</span>
            </button>
          </div>
        </div>
      `;

      comparisonList.appendChild(card);
    });

    // Attach individual copy button events
    const copyButtons = comparisonList.querySelectorAll(".btn-copy-card");
    copyButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = parseInt(btn.getAttribute("data-index"), 10);
        const bullet = currentBullets[idx];
        if (bullet && bullet.tailored) {
          navigator.clipboard.writeText(bullet.tailored).then(() => {
            btn.classList.add("copied");
            btn.innerHTML = `<span>✓ Copied!</span>`;
            showToast("Bullet copied to clipboard!");
            setTimeout(() => {
              btn.classList.remove("copied");
              btn.innerHTML = `
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                <span>Copy</span>
              `;
            }, 1500);
          });
        }
      });
    });

    resultsZone.classList.remove("hidden");
    resultsZone.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // --- Event Listeners ---
  resumeInput.addEventListener("input", updateCounters);
  jobInput.addEventListener("input", updateCounters);

  errorDismiss.addEventListener("click", hideError);

  btnSample.addEventListener("click", () => {
    resumeInput.value = SAMPLE_DATA.resume;
    jobInput.value = SAMPLE_DATA.job;
    updateCounters();
    hideError();
  });

  btnClear.addEventListener("click", () => {
    resumeInput.value = "";
    jobInput.value = "";
    updateCounters();
    hideError();
    resultsZone.classList.add("hidden");
    currentBullets = [];
  });

  btnCopyAll.addEventListener("click", () => {
    if (!currentBullets || currentBullets.length === 0) return;

    const allBulletsText = currentBullets.map(b => `• ${b.tailored}`).join("\n");
    navigator.clipboard.writeText(allBulletsText).then(() => {
      const origText = copyAllLabel.textContent;
      copyAllLabel.textContent = "✓ All Bullets Copied!";
      btnCopyAll.style.borderColor = "var(--success-border)";
      btnCopyAll.style.background = "var(--success-bg)";
      btnCopyAll.style.color = "var(--success-color)";
      showToast("All tailored bullets copied!");

      setTimeout(() => {
        copyAllLabel.textContent = origText;
        btnCopyAll.style.borderColor = "";
        btnCopyAll.style.background = "";
        btnCopyAll.style.color = "";
      }, 2000);
    });
  });

  btnTailor.addEventListener("click", async () => {
    const resumeText = resumeInput.value.trim();
    const jobDescription = jobInput.value.trim();

    if (resumeText.length < 20 || jobDescription.length < 20) {
      showError("Please enter at least 20 characters in both the resume and job description fields.");
      return;
    }

    startLoading();

    try {
      const response = await fetch("/api/tailor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        const detail = errData.detail || `Server error (${response.status})`;
        throw new Error(detail);
      }

      const data = await response.json();
      renderComparisonMatrix(data);
    } catch (err) {
      console.error("Tailor error:", err);
      showError(err.message || "Failed to tailor bullets. Please verify connection and try again.");
    } finally {
      stopLoading();
    }
  });

  // Initial setup
  updateCounters();
});
