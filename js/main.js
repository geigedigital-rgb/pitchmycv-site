document.addEventListener("DOMContentLoaded", () => {
  // Mobile burger nav
  const navToggle = document.querySelector(".nav-toggle");
  const headerNav = document.querySelector(".header-nav");
  if (navToggle && headerNav) {
    const closeMenu = () => {
      headerNav.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    };

    navToggle.addEventListener("click", () => {
      const isOpen = headerNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    headerNav.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        if (window.innerWidth <= 768) {
          closeMenu();
        }
      });
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 768) {
        closeMenu();
      }
    });
  }

  // One-time consent banner for first visit
  const consentStorageKey = "pmcv_cookie_consent_v1";
  const shouldShowConsent = (() => {
    try {
      return !window.localStorage.getItem(consentStorageKey);
    } catch (error) {
      return true;
    }
  })();

  if (shouldShowConsent) {
    const consentBanner = document.createElement("section");
    consentBanner.className = "cookie-consent";
    consentBanner.setAttribute("role", "dialog");
    consentBanner.setAttribute("aria-live", "polite");
    consentBanner.setAttribute("aria-label", "Cookie and data processing notice");
    consentBanner.innerHTML = `
      <div class="cookie-consent-card">
        <p class="cookie-consent-text">
          We use necessary cookies and site interaction data to provide the service and improve resume analytics.
          By continuing to use the site, you accept the
          <a href="/privacy">Privacy Policy</a>,
          <a href="/data-processing">Data Processing Policy</a>, and
          <a href="/terms">Terms of Service</a>.
        </p>
        <button type="button" class="cookie-consent-accept">Accept</button>
      </div>
    `;

    document.body.appendChild(consentBanner);
    requestAnimationFrame(() => {
      consentBanner.classList.add("is-visible");
    });

    const acceptButton = consentBanner.querySelector(".cookie-consent-accept");
    if (acceptButton) {
      acceptButton.addEventListener("click", () => {
        try {
          window.localStorage.setItem(consentStorageKey, "accepted");
        } catch (error) {
          // No-op if storage is unavailable.
        }
        consentBanner.classList.remove("is-visible");
        setTimeout(() => consentBanner.remove(), 220);
      });
    }
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Career page TOC: keep active section highlighted while scrolling.
  const careerToc = document.querySelector(".career-toc");
  if (careerToc) {
    const siteHeader = document.querySelector(".site-header");
    const careerLayout = careerToc.closest(".career-layout");
    const careerArticle = document.querySelector(".career-article");
    const fallbackMinWidth = 861;
    let tocPlaceholder = null;

    const ensureTocPlaceholder = () => {
      if (tocPlaceholder || !careerToc.parentNode) return;
      tocPlaceholder = document.createElement("div");
      tocPlaceholder.className = "career-toc-placeholder";
      tocPlaceholder.style.width = `${careerToc.offsetWidth}px`;
      tocPlaceholder.style.height = `${careerToc.offsetHeight}px`;
      careerToc.parentNode.insertBefore(tocPlaceholder, careerToc);
    };

    const removeTocPlaceholder = () => {
      if (!tocPlaceholder) return;
      tocPlaceholder.remove();
      tocPlaceholder = null;
    };

    const updateTocOffset = () => {
      const headerHeight = siteHeader ? Math.round(siteHeader.getBoundingClientRect().height) : 0;
      // Keep TOC close to its original start position.
      // Header is not fixed, so large offsets look visually detached.
      const topOffset = headerHeight > 72 ? 12 : 8;
      careerToc.style.setProperty("--toc-top-offset", `${topOffset}px`);
    };

    const resetTocFallbackState = () => {
      careerToc.classList.remove("toc-fixed", "toc-bottom");
      careerToc.style.removeProperty("--toc-left");
      careerToc.style.removeProperty("--toc-width");
      removeTocPlaceholder();
    };

    const updateTocStickyFallback = () => {
      if (!careerLayout || !careerArticle || window.innerWidth < fallbackMinWidth) {
        resetTocFallbackState();
        return;
      }

      const topOffset = parseInt(getComputedStyle(careerToc).getPropertyValue("--toc-top-offset"), 10) || 16;
      const layoutRect = careerLayout.getBoundingClientRect();
      const articleRect = careerArticle.getBoundingClientRect();
      const tocRect = careerToc.getBoundingClientRect();
      const scrollY = window.scrollY || window.pageYOffset;
      const layoutTopAbs = layoutRect.top + scrollY;
      const articleBottomAbs = articleRect.bottom + scrollY;

      const startY = layoutTopAbs - topOffset;
      const endY = articleBottomAbs - tocRect.height - topOffset - 24;

      if (scrollY > startY && scrollY < endY) {
        ensureTocPlaceholder();
        const placeholderRect = tocPlaceholder.getBoundingClientRect();
        careerToc.style.setProperty("--toc-left", `${Math.round(placeholderRect.left)}px`);
        careerToc.style.setProperty("--toc-width", `${Math.round(placeholderRect.width)}px`);
        careerToc.classList.add("toc-fixed");
        careerToc.classList.remove("toc-bottom");
      } else if (scrollY >= endY) {
        ensureTocPlaceholder();
        const placeholderRect = tocPlaceholder.getBoundingClientRect();
        careerToc.style.setProperty("--toc-width", `${Math.round(placeholderRect.width)}px`);
        careerToc.classList.remove("toc-fixed");
        careerToc.classList.add("toc-bottom");
      } else {
        resetTocFallbackState();
      }
    };

    updateTocOffset();
    updateTocStickyFallback();
    window.addEventListener("resize", () => {
      updateTocOffset();
      updateTocStickyFallback();
    });
    window.addEventListener("scroll", updateTocStickyFallback, { passive: true });

    const tocLinks = Array.from(careerToc.querySelectorAll('a[href^="#"]'));
    const linkSectionPairs = tocLinks
      .map(link => {
        const href = link.getAttribute("href");
        if (!href || href.length < 2) return null;
        const section = document.querySelector(href);
        if (!section) return null;
        return { link, section, id: href.slice(1) };
      })
      .filter(Boolean);

    if (linkSectionPairs.length > 0) {
      const setActiveLink = activeId => {
        linkSectionPairs.forEach(({ link, id }) => {
          const isActive = id === activeId;
          link.classList.toggle("is-active", isActive);
          if (isActive) {
            link.setAttribute("aria-current", "true");
          } else {
            link.removeAttribute("aria-current");
          }
        });
      };

      const resolveActiveId = () => {
        const activationOffset = 140;
        let activeId = linkSectionPairs[0].id;

        linkSectionPairs.forEach(({ section, id }) => {
          const rect = section.getBoundingClientRect();
          if (rect.top <= activationOffset) {
            activeId = id;
          }
        });

        return activeId;
      };

      let ticking = false;
      const updateActiveFromScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          setActiveLink(resolveActiveId());
          ticking = false;
        });
      };

      updateActiveFromScroll();
      window.addEventListener("scroll", updateActiveFromScroll, { passive: true });
      window.addEventListener("resize", updateActiveFromScroll);
    }
  }

  // Landing API: save → redirect to app login. See docs/LANDIND_API.md (§2, §10–11).
  // For local backend use: "http://localhost:8000"
  const LANDING_API_BASE = "https://my.pitchcv.app";

  // Drag & Drop interactive zone (Rezi style) — hero + optional footer CTA duplicate
  function qid(suffix, base) {
    return document.getElementById(`${base}${suffix}`);
  }

  const LANDING_UPLOAD_ZONES = [
    { suffix: "", zoneId: "upload-zone" },
    { suffix: "-cta", zoneId: "upload-zone-cta" },
  ];
  const uploadInstances = LANDING_UPLOAD_ZONES.map(({ suffix, zoneId }) => {
    const zone = document.getElementById(zoneId);
    const fileInput = qid(suffix, "file-input");
    if (!zone || !fileInput) {
      return null;
    }
    return { suffix, zoneId, zone, fileInput };
  }).filter(Boolean);

  // Hero gauge: full gradient arc static; slider thumb moves along the arc
  const gaugeArcPath = document.querySelector(".gauge-svg-thumb .gauge-gradient-arc");
  const gaugeThumbGroup = document.querySelector(".gauge-svg-thumb .gauge-thumb-group");
  const gaugeValue = document.querySelector(".gauge-value");
  const gaugeWrap = document.querySelector(".score-gauge-wrap");

  if (gaugeArcPath && gaugeThumbGroup && gaugeValue && gaugeWrap) {
    const maxPercent = 100;
    const upDurationMs = 2200;
    const holdAtMaxMs = 2000;
    const downDurationMs = 1800;
    const arcLength = typeof gaugeArcPath.getTotalLength === "function"
      ? gaugeArcPath.getTotalLength()
      : 157;
    const arcEps = 1.5;

    const easeInOutCubic = t => (
      t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2
    );

    const setGaugeState = percent => {
      const safePercent = Math.max(0, Math.min(maxPercent, percent));
      const progress = safePercent / maxPercent;
      const startColor = [239, 68, 68];
      const endColor = [34, 197, 94];
      const r = Math.round(startColor[0] + (endColor[0] - startColor[0]) * progress);
      const g = Math.round(startColor[1] + (endColor[1] - startColor[1]) * progress);
      const b = Math.round(startColor[2] + (endColor[2] - startColor[2]) * progress);
      const glowAlphaBase = Math.pow(progress, 1.45) * 0.26;
      const nearMaxBoost = progress > 0.9 ? ((progress - 0.9) / 0.1) * 0.08 : 0;
      const glowAlpha = Math.min(0.34, glowAlphaBase + nearMaxBoost);
      const glowScale = 0.9 + progress * 0.12;

      const L = arcLength;
      const d = arcEps + (L - 2 * arcEps) * progress;
      const p = gaugeArcPath.getPointAtLength(d);
      const dA = Math.min(L - arcEps, d + 2.5);
      const dB = Math.max(arcEps, d - 2.5);
      const pA = gaugeArcPath.getPointAtLength(dA);
      const pB = gaugeArcPath.getPointAtLength(dB);
      const angleDeg = Math.atan2(pA.y - pB.y, pA.x - pB.x) * (180 / Math.PI);

      gaugeThumbGroup.setAttribute(
        "transform",
        `translate(${p.x.toFixed(2)},${p.y.toFixed(2)}) rotate(${angleDeg.toFixed(2)})`
      );
      gaugeValue.textContent = `${Math.round(safePercent)}%`;

      gaugeWrap.style.setProperty("--gauge-glow-rgb", `${r}, ${g}, ${b}`);
      gaugeWrap.style.setProperty("--gauge-glow-alpha", glowAlpha.toFixed(3));
      gaugeWrap.style.setProperty("--gauge-glow-scale", glowScale.toFixed(3));

      if (progress >= 0.96) {
        gaugeWrap.classList.add("gauge-near-max");
      } else {
        gaugeWrap.classList.remove("gauge-near-max");
      }
    };

    const animateRange = (from, to, durationMs, onDone) => {
      const start = performance.now();

      const tick = now => {
        const elapsed = now - start;
        const t = Math.min(1, elapsed / durationMs);
        const eased = easeInOutCubic(t);
        setGaugeState(from + (to - from) * eased);

        if (t < 1) {
          requestAnimationFrame(tick);
          return;
        }

        if (typeof onDone === "function") {
          onDone();
        }
      };

      requestAnimationFrame(tick);
    };

    const runGaugeIntroAnimation = () => {
      setGaugeState(0);

      animateRange(0, maxPercent, upDurationMs, () => {
        setTimeout(() => {
          animateRange(maxPercent, 0, downDurationMs);
        }, holdAtMaxMs);
      });
    };

    if (document.readyState === "complete") {
      runGaugeIntroAnimation();
    } else {
      window.addEventListener("load", runGaugeIntroAnimation, { once: true });
    }
  }

  function ensureResumeDropzoneLayout(dropzoneEl) {
    const dz = dropzoneEl || document.getElementById("upload-dropzone");
    if (!dz) {
      return;
    }
    const textWrap = dz.querySelector(".compact-dropzone-text");
    if (textWrap && !textWrap.querySelector(".compact-dropzone-text-body")) {
      const body = document.createElement("div");
      body.className = "compact-dropzone-text-body";
      while (textWrap.firstChild) {
        body.appendChild(textWrap.firstChild);
      }
      textWrap.appendChild(body);
    }
    const iconWrap = dz.querySelector(".upload-dropzone-icon");
    if (!iconWrap || iconWrap.querySelector(".icon-resume-replace")) {
      return;
    }
    const uploadIcon = iconWrap.querySelector(".ph-file-arrow-up, .icon-resume-upload");
    if (uploadIcon && !uploadIcon.classList.contains("icon-resume-upload")) {
      uploadIcon.classList.add("icon-resume-upload");
    }
    if (!iconWrap.querySelector(".icon-resume-upload")) {
      const up = document.createElement("i");
      up.className = "ph ph-file-arrow-up icon-resume-upload";
      up.setAttribute("aria-hidden", "true");
      iconWrap.insertBefore(up, iconWrap.firstChild);
    }
    const rep = document.createElement("i");
    rep.className = "ph ph-arrows-clockwise icon-resume-replace";
    rep.setAttribute("aria-hidden", "true");
    iconWrap.appendChild(rep);
  }

  function setupCompactUploadLayoutEnhancements(zone, suffix) {
    const fileInputEl = qid(suffix, "file-input");
    if (!zone || !fileInputEl) {
      return;
    }

    const fileCardRoot = zone.querySelector(".compact-file-card");
    if (fileCardRoot) {
      fileCardRoot.classList.add("compact-file-card-unified");
    }

    const stack = zone.querySelector(".compact-upload-row, .compact-upload-stack");
    if (stack && !stack.classList.contains("compact-upload-stack")) {
      stack.classList.add("compact-upload-stack");
    }

    const jobWrapperId = `compact-job-wrapper${suffix}`;
    let jobLinkStepEl = qid(suffix, "job-link-step");
    if (jobLinkStepEl && !document.getElementById(jobWrapperId)) {
      const overlay = jobLinkStepEl.querySelector(".compact-link-overlay");
      if (overlay) {
        overlay.remove();
      }
      jobLinkStepEl.classList.remove("is-disabled");
      jobLinkStepEl.removeAttribute("aria-disabled");

      const wrapper = document.createElement("div");
      wrapper.id = jobWrapperId;
      wrapper.className = "compact-job-wrapper";
      wrapper.hidden = true;

      jobLinkStepEl.parentNode.insertBefore(wrapper, jobLinkStepEl);
      wrapper.appendChild(jobLinkStepEl);
    }

    ensureResumeDropzoneLayout(qid(suffix, "upload-dropzone"));

    const dropzoneEl = qid(suffix, "upload-dropzone");
    const fileCard = zone.querySelector(".compact-file-card");
    const rowId = `resume-drop-row${suffix}`;
    if (dropzoneEl && fileCard && !fileCard.querySelector(".compact-resume-row")) {
      const row = document.createElement("div");
      row.className = "compact-resume-row";
      row.id = rowId;
      dropzoneEl.parentNode.insertBefore(row, dropzoneEl);
      row.appendChild(dropzoneEl);
      dropzoneEl.classList.add("compact-dropzone-compact");
    } else {
      const existingRow = zone.querySelector(".compact-resume-row");
      if (existingRow && !existingRow.id) {
        existingRow.id = rowId;
      }
    }
  }

  if (uploadInstances.length > 0) {
    uploadInstances.forEach(({ zone, suffix }) => setupCompactUploadLayoutEnhancements(zone, suffix));

    const primary = uploadInstances[0];
    const isTwoStepUploadFlow = Boolean(
      qid(primary.suffix, "upload-dropzone")
        && qid(primary.suffix, "job-link-step")
        && qid(primary.suffix, "job-text-input")
        && qid(primary.suffix, "analyze-resume-btn")
    );

    const getEls = suffix => ({
      uploadDropzone: qid(suffix, "upload-dropzone"),
      dropzoneTitle: qid(suffix, "dropzone-title"),
      fileStepStatus: qid(suffix, "file-step-status"),
      jobLinkStep: qid(suffix, "job-link-step"),
      jobTextInput: qid(suffix, "job-text-input"),
      jobLinkNote: qid(suffix, "job-link-note"),
      analyzeResumeBtn: qid(suffix, "analyze-resume-btn"),
      resumeDropRow: qid(suffix, "resume-drop-row"),
      fileInput: qid(suffix, "file-input"),
      zone: document.getElementById(suffix ? `upload-zone${suffix}` : "upload-zone"),
    });

    const dropzoneTitlePrimary = qid(primary.suffix, "dropzone-title");
    const dragTargets = uploadInstances.map(inst => {
      const e = getEls(inst.suffix);
      return e.resumeDropRow || e.uploadDropzone || e.zone;
    }).filter(Boolean);
    let selectedResumeFile = null;

    const dropzoneEmptyLabel = (() => {
      if (!dropzoneTitlePrimary) {
        return "Drop your resume here or click to upload";
      }
      const fromData = dropzoneTitlePrimary.getAttribute("data-empty-label")?.trim();
      if (fromData) {
        return fromData;
      }
      const fromSpan = dropzoneTitlePrimary.querySelector(".dropzone-title-desktop-only")?.textContent?.trim();
      if (fromSpan) {
        return fromSpan;
      }
      const plain = dropzoneTitlePrimary.textContent.trim();
      return plain || "Drop your resume here or click to upload";
    })();

    const validTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    const updateAnalyzeResumeButtonState = () => {
      if (!isTwoStepUploadFlow) {
        return;
      }
      const hasFile = Boolean(selectedResumeFile);
      const primaryJobInput = qid(primary.suffix, "job-text-input");
      const hasJobText = Boolean(primaryJobInput?.value.trim());
      const enabled = hasFile && hasJobText;
      uploadInstances.forEach(inst => {
        const btn = qid(inst.suffix, "analyze-resume-btn");
        if (!btn) {
          return;
        }
        btn.disabled = !enabled;
        btn.setAttribute("aria-disabled", enabled ? "false" : "true");
      });
    };

    const setTwoStepState = file => {
      if (!isTwoStepUploadFlow) {
        return;
      }
      selectedResumeFile = file;
      const hasFile = Boolean(file);

      uploadInstances.forEach(inst => {
        const e = getEls(inst.suffix);
        const jobWrapperEl = document.getElementById(`compact-job-wrapper${inst.suffix}`);

        if (e.dropzoneTitle) {
          if (hasFile) {
            e.dropzoneTitle.textContent = file.name;
            e.dropzoneTitle.classList.add("has-selected-file");
          } else {
            e.dropzoneTitle.classList.remove("has-selected-file");
            const span = document.createElement("span");
            span.className = "dropzone-title-desktop-only";
            span.textContent = dropzoneEmptyLabel;
            e.dropzoneTitle.replaceChildren(span);
          }
        }
        if (e.fileStepStatus) {
          e.fileStepStatus.textContent = "";
        }
        if (e.jobTextInput) {
          e.jobTextInput.disabled = !hasFile;
        }
        if (e.jobLinkNote) {
          e.jobLinkNote.textContent = hasFile ? "Paste job description to continue" : "";
        }
        if (jobWrapperEl) {
          jobWrapperEl.hidden = !hasFile;
        }
        if (e.jobLinkStep) {
          if (jobWrapperEl) {
            e.jobLinkStep.classList.remove("is-disabled");
            e.jobLinkStep.setAttribute("aria-disabled", "false");
          } else {
            e.jobLinkStep.classList.toggle("is-disabled", !hasFile);
            e.jobLinkStep.setAttribute("aria-disabled", hasFile ? "false" : "true");
          }
        }
        if (e.zone) {
          e.zone.classList.toggle("has-resume-file", hasFile);
        }
      });
      updateAnalyzeResumeButtonState();
    };

    const syncJobTextFrom = sourceInput => {
      if (!sourceInput) {
        return;
      }
      const value = sourceInput.value;
      uploadInstances.forEach(inst => {
        const jt = qid(inst.suffix, "job-text-input");
        if (jt && jt !== sourceInput) {
          jt.value = value;
        }
      });
    };

    if (isTwoStepUploadFlow) {
      uploadInstances.forEach(inst => {
        const e = getEls(inst.suffix);
        if (!e.jobTextInput || !e.jobLinkNote) {
          return;
        }
        e.jobTextInput.addEventListener("input", () => {
          syncJobTextFrom(e.jobTextInput);
          uploadInstances.forEach(i => {
            const n = qid(i.suffix, "job-link-note");
            if (n) {
              n.textContent = "";
              n.classList.add("sr-only");
              n.classList.remove("upload-link-note");
            }
          });
          updateAnalyzeResumeButtonState();
        });
      });
    }

    if (isTwoStepUploadFlow) {
      uploadInstances.forEach(inst => {
        const e = getEls(inst.suffix);
        if (!e.uploadDropzone || !e.fileInput) {
          return;
        }
        e.uploadDropzone.addEventListener("click", () => {
          e.fileInput.click();
        });
        e.uploadDropzone.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            e.fileInput.click();
          }
        });
      });
      setTwoStepState(null);
    }

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
      document.body.addEventListener(eventName, preventDefaults, false);
    });

    uploadInstances.forEach((inst, idx) => {
      const target = dragTargets[idx];
      if (!target) {
        return;
      }
      const e = getEls(inst.suffix);

      ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
        target.addEventListener(eventName, preventDefaults, false);
      });

      const highlightInst = () => {
        if (e.resumeDropRow) {
          e.resumeDropRow.classList.add("is-dragover");
        } else if (e.uploadDropzone) {
          e.uploadDropzone.classList.add("is-dragover");
        } else if (e.zone) {
          e.zone.classList.add("dragover");
        }
      };

      const unhighlightInst = () => {
        if (e.resumeDropRow) {
          e.resumeDropRow.classList.remove("is-dragover");
        } else if (e.uploadDropzone) {
          e.uploadDropzone.classList.remove("is-dragover");
        } else if (e.zone) {
          e.zone.classList.remove("dragover");
        }
      };

      ["dragenter", "dragover"].forEach(eventName => {
        target.addEventListener(eventName, highlightInst, false);
      });

      ["dragleave", "drop"].forEach(eventName => {
        target.addEventListener(eventName, unhighlightInst, false);
      });

      target.addEventListener("drop", evt => {
        const dt = evt.dataTransfer;
        if (dt.files?.length) {
          handleFiles(dt.files);
        }
      }, false);
    });

    uploadInstances.forEach(inst => {
      if (!inst.fileInput) {
        return;
      }
      inst.fileInput.addEventListener("change", function () {
        handleFiles(this.files);
      });
    });

    function handleFiles(files) {
      if (files.length > 0) {
        const file = files[0];

        if (validTypes.includes(file.type) || file.name.match(/\.(pdf|doc|docx)$/i)) {
          if (isTwoStepUploadFlow) {
            setTwoStepState(file);
            return;
          }

          const z = uploadInstances[0]?.zone;
          const btn = z?.querySelector("button");
          if (btn) {
            btn.textContent = "Analyzing...";
          }
          setTimeout(() => {
            window.location.href = "/scan";
          }, 1500);
        } else {
          if (isTwoStepUploadFlow) {
            uploadInstances.forEach(inst => {
              const fs = qid(inst.suffix, "file-step-status");
              if (fs) {
                fs.textContent = "Unsupported format. Use PDF, DOC, or DOCX";
              }
            });
          }
          alert("Please upload a PDF or DOCX file.");
        }
      }
    }

    if (isTwoStepUploadFlow) {
      const loadingSteps = [
        "Uploading resume…",
        "Checking job description…",
        "Preparing your analysis…",
        "Almost there…",
      ];

      const attachAnalyze = inst => {
        const btn = qid(inst.suffix, "analyze-resume-btn");
        const zoneRoot = inst.zone;
        if (!btn || !zoneRoot) {
          return;
        }

        btn.addEventListener("click", async () => {
          if (!selectedResumeFile) {
            return;
          }

          const jobText = qid(primary.suffix, "job-text-input")?.value.trim() || "";
          if (!jobText) {
            uploadInstances.forEach(i => {
              const note = qid(i.suffix, "job-link-note");
              if (note) {
                note.textContent = "Please paste the job vacancy text to continue.";
                note.classList.remove("sr-only");
                note.classList.add("upload-link-note");
              }
            });
            return;
          }

          uploadInstances.forEach(i => {
            const b = qid(i.suffix, "analyze-resume-btn");
            if (b) {
              b.disabled = true;
              b.textContent = "Saving…";
            }
          });

          const overlay = document.createElement("div");
          overlay.className = "upload-card-loading";
          overlay.setAttribute("aria-live", "polite");
          overlay.setAttribute("aria-busy", "true");
          overlay.innerHTML = `
          <div class="upload-card-loading-spinner" aria-hidden="true"></div>
          <div class="upload-card-loading-text">${loadingSteps[0]}</div>
        `;
          const loadingTextEl = overlay.querySelector(".upload-card-loading-text");
          zoneRoot.appendChild(overlay);

          let stepIndex = 0;
          const stepInterval = setInterval(() => {
            stepIndex = Math.min(stepIndex + 1, loadingSteps.length - 1);
            if (loadingTextEl) {
              loadingTextEl.textContent = loadingSteps[stepIndex];
            }
            if (stepIndex >= loadingSteps.length - 1) {
              clearInterval(stepInterval);
            }
          }, 600);

          const hideOverlay = () => {
            clearInterval(stepInterval);
            overlay.remove();
            uploadInstances.forEach(i => {
              const b = qid(i.suffix, "analyze-resume-btn");
              if (b) {
                b.textContent = "Check your resume free";
              }
            });
            updateAnalyzeResumeButtonState();
          };

          try {
            const formData = new FormData();
            formData.append("resume", selectedResumeFile);
            formData.append("job_text", jobText);

            const response = await fetch(`${LANDING_API_BASE}/api/landing/save`, {
              method: "POST",
              body: formData,
              credentials: "omit",
            });

            if (!response.ok) {
              const err = await response.json().catch(() => ({}));
              let message = "Something went wrong. Please try again.";
              if (typeof err.detail === "string") {
                message = err.detail;
              } else if (Array.isArray(err.detail) && err.detail[0]) {
                message = err.detail[0].msg || "Invalid input.";
              } else if (err.detail) {
                message = String(err.detail);
              } else if (response.statusText) {
                message = response.statusText;
              }
              throw new Error(message);
            }

            const data = await response.json();
            const token = data.token;
            if (!token) {
              throw new Error("No token received.");
            }
            clearInterval(stepInterval);
            if (loadingTextEl) {
              loadingTextEl.textContent = "Redirecting to your dashboard…";
            }
            window.location.href = `${LANDING_API_BASE}/login?pending=${encodeURIComponent(token)}`;
          } catch (err) {
            hideOverlay();
            alert(err.message || "Could not save. Please try again.");
          }
        });
      };

      uploadInstances.forEach(attachAnalyze);
    }
  }

  // Review timestamps: разница между сегодня и датой публикации (фиксированные даты в data-review-date)
  const reviewAgoEls = document.querySelectorAll(".review-ago[data-review-date]");
  const formatReviewAgo = (date) => {
    const now = new Date();
    const diffMs = now - date;
    const diffM = Math.floor(Math.abs(diffMs) / 60000);
    const diffH = Math.floor(Math.abs(diffMs) / 3600000);
    const diffD = Math.floor(Math.abs(diffMs) / 86400000);
    const diffW = Math.floor(diffD / 7);
    const past = diffMs >= 0;
    const suffix = past ? " ago" : " from now";
    const prefix = past ? "" : "in ";
    if (diffMs >= 0) {
      if (diffM < 1) return "just now";
      if (diffM < 60) return diffM === 1 ? "1 minute ago" : `${diffM} minutes ago`;
      if (diffH < 24) return diffH === 1 ? "about 1 hour ago" : `about ${diffH} hours ago`;
      if (diffD === 1) return "1 day ago";
      if (diffD < 7) return `${diffD} days ago`;
      if (diffW === 1) return "1 week ago";
      if (diffW < 4) return `${diffW} weeks ago`;
      return date.toLocaleDateString();
    }
    if (diffD < 1) return diffH <= 1 ? "in about 1 hour" : `in about ${diffH} hours`;
    if (diffD === 1) return "in 1 day";
    if (diffD < 7) return `in ${diffD} days`;
    if (diffW === 1) return "in 1 week";
    if (diffW < 4) return `in ${diffW} weeks`;
    return date.toLocaleDateString();
  };
  reviewAgoEls.forEach((el) => {
    const iso = el.getAttribute("data-review-date");
    if (!iso) return;
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return;
    el.textContent = formatReviewAgo(date);
  });

  // CTA typewriter: 10 job titles, type then erase with blinking cursor
  const ctaJobEl = document.getElementById("cta-typewriter-job");
  const ctaJobs = [
    "Software Engineer",
    "Product Manager",
    "Data Scientist",
    "Marketing Manager",
    "Sales Manager",
    "Project Manager",
    "UX Designer",
    "Content Writer",
    "Digital Marketing Specialist",
    "Event Planner",
  ];
  if (ctaJobEl) {
    let jobIndex = 0;
    let isTyping = true;
    let charIndex = 0;
    const typeSpeed = 90;
    const eraseSpeed = 50;
    const pauseAfterType = 2200;
    const pauseAfterErase = 600;

    const tick = () => {
      const job = ctaJobs[jobIndex];
      if (isTyping) {
        if (charIndex <= job.length) {
          ctaJobEl.textContent = job.slice(0, charIndex);
          charIndex++;
          setTimeout(tick, typeSpeed);
        } else {
          isTyping = false;
          setTimeout(tick, pauseAfterType);
        }
      } else {
        if (charIndex > 0) {
          charIndex--;
          ctaJobEl.textContent = job.slice(0, charIndex);
          setTimeout(tick, eraseSpeed);
        } else {
          isTyping = true;
          jobIndex = (jobIndex + 1) % ctaJobs.length;
          setTimeout(tick, pauseAfterErase);
        }
      }
    };
    setTimeout(tick, 400);
  }

  // Reviews horizontal slider
  const reviewsTrack = document.getElementById("reviews-track");
  const reviewsPrevBtn = document.querySelector('[data-reviews-nav="prev"]');
  const reviewsNextBtn = document.querySelector('[data-reviews-nav="next"]');
  const reviewsProgressFill = document.querySelector(".reviews-progress-fill");
  const reviewsControls = document.querySelector(".reviews-controls");

  if (reviewsTrack && reviewsPrevBtn && reviewsNextBtn && reviewsProgressFill && reviewsControls) {
    let isScrollable = false;

    const getScrollStep = () => {
      const card = reviewsTrack.querySelector(".review-card");
      if (!card) return 280;
      const styles = window.getComputedStyle(reviewsTrack);
      const gap = parseFloat(styles.columnGap || styles.gap || "16");
      return card.getBoundingClientRect().width + gap;
    };

    const updateReviewsProgress = () => {
      const maxScroll = reviewsTrack.scrollWidth - reviewsTrack.clientWidth;
      isScrollable = maxScroll > 4;
      reviewsControls.style.display = isScrollable ? "flex" : "none";
      const ratio = maxScroll > 0 ? reviewsTrack.scrollLeft / maxScroll : 0;
      const fillPercent = 20 + ratio * 80;
      reviewsProgressFill.style.width = `${fillPercent}%`;
    };

    reviewsPrevBtn.addEventListener("click", () => {
      if (!isScrollable) return;
      reviewsTrack.scrollBy({ left: -getScrollStep(), behavior: "smooth" });
    });

    reviewsNextBtn.addEventListener("click", () => {
      if (!isScrollable) return;
      reviewsTrack.scrollBy({ left: getScrollStep(), behavior: "smooth" });
    });

    reviewsTrack.addEventListener("scroll", updateReviewsProgress);
    window.addEventListener("resize", updateReviewsProgress);
    updateReviewsProgress();
  }

  // FAQ Accordion
  const faqQuestions = document.querySelectorAll('.faq-question');
  
  faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
      const isExpanded = question.getAttribute('aria-expanded') === 'true';
      const answer = question.nextElementSibling;
      
      // Close all other FAQs
      faqQuestions.forEach(q => {
        q.setAttribute('aria-expanded', 'false');
        q.nextElementSibling.style.maxHeight = null;
      });
      
      // Toggle current FAQ
      if (!isExpanded) {
        question.setAttribute('aria-expanded', 'true');
        answer.style.maxHeight = answer.scrollHeight + "px";
      }
    });
  });

  // Resumes Created Counter Animation
  const resumesCounter = document.getElementById("resumes-counter");
  if (resumesCounter) {
    let baseNumber = 203;
    const formatCounter = value => value.toLocaleString("en-US");
    let displayedCounter = baseNumber;
    let finalizeCounterTimer = null;

    const createDigitNode = digit => {
      const slot = document.createElement("span");
      slot.className = "counter-digit counter-digit-static";
      const valueNode = document.createElement("span");
      valueNode.className = "counter-digit-value";
      valueNode.textContent = digit;
      slot.appendChild(valueNode);
      return slot;
    };

    const createSeparatorNode = char => {
      const separator = document.createElement("span");
      separator.className = "counter-separator";
      separator.textContent = char;
      return separator;
    };

    const renderStaticCounter = value => {
      resumesCounter.innerHTML = "";
      const chars = formatCounter(value).split("");

      chars.forEach(char => {
        if (/\d/.test(char)) {
          resumesCounter.appendChild(createDigitNode(char));
        } else {
          resumesCounter.appendChild(createSeparatorNode(char));
        }
      });
    };

    const rollCounterTo = nextValue => {
      if (finalizeCounterTimer) {
        clearTimeout(finalizeCounterTimer);
        finalizeCounterTimer = null;
      }

      const prevRaw = String(displayedCounter);
      const nextRaw = String(nextValue);
      const maxLen = Math.max(prevRaw.length, nextRaw.length);
      const prevDigits = prevRaw.padStart(maxLen, " ");
      const nextDigits = nextRaw.padStart(maxLen, " ");
      const changedMask = Array.from({ length: maxLen }, (_, idx) => prevDigits[idx] !== nextDigits[idx]);
      const nextChars = formatCounter(nextValue).split("");

      resumesCounter.innerHTML = "";

      const tracks = [];
      let digitIndex = 0;

      nextChars.forEach(char => {
        if (!/\d/.test(char)) {
          resumesCounter.appendChild(createSeparatorNode(char));
          return;
        }

        const newDigit = nextDigits[digitIndex];
        const oldDigitRaw = prevDigits[digitIndex];
        const shouldAnimate = changedMask[digitIndex];

        if (!shouldAnimate) {
          resumesCounter.appendChild(createDigitNode(newDigit));
          digitIndex += 1;
          return;
        }

        const oldDigit = /\d/.test(oldDigitRaw) ? oldDigitRaw : "0";
        const slot = document.createElement("span");
        slot.className = "counter-digit counter-digit-rolling";

        const track = document.createElement("span");
        track.className = "counter-digit-track";

        const oldValue = document.createElement("span");
        oldValue.className = "counter-digit-value";
        oldValue.textContent = oldDigit;

        const newValue = document.createElement("span");
        newValue.className = "counter-digit-value";
        newValue.textContent = newDigit;

        track.append(oldValue, newValue);
        slot.appendChild(track);
        resumesCounter.appendChild(slot);
        tracks.push({ track, index: digitIndex });

        digitIndex += 1;
      });

      const baseDuration = 560;
      let maxDelay = 0;

      tracks.forEach(({ track, index }) => {
        const delay = Math.max(0, (maxLen - 1 - index) * 28);
        maxDelay = Math.max(maxDelay, delay);
        track.animate(
          [
            { transform: "translateY(0%)" },
            { transform: "translateY(-100%)" }
          ],
          {
            duration: baseDuration,
            easing: "cubic-bezier(0.22, 1, 0.36, 1)",
            fill: "forwards",
            delay
          }
        );
      });

      finalizeCounterTimer = setTimeout(() => {
        displayedCounter = nextValue;
        renderStaticCounter(nextValue);
      }, baseDuration + maxDelay + 40);
    };

    resumesCounter.classList.add("counter-roll");
    renderStaticCounter(baseNumber);

    // Function to generate random interval between 5 and 15 seconds
    const getRandomInterval = () => Math.floor(Math.random() * (15000 - 5000 + 1)) + 5000;
    
    const updateCounter = () => {
      baseNumber += 1;
      rollCounterTo(baseNumber);

      // Set next timeout
      setTimeout(updateCounter, getRandomInterval());
    };

    // Start the counter
    setTimeout(updateCounter, getRandomInterval());
  }
});
