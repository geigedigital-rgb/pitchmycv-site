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

  // Drag & Drop interactive zone (Rezi style)
  const uploadZone = document.getElementById("upload-zone");
  const fileInput = document.getElementById("file-input");

  // Hero gauge intro animation (run once after full page load)
  const gaugeFill = document.querySelector(".gauge-fill");
  const gaugeValue = document.querySelector(".gauge-value");
  const gaugeWrap = document.querySelector(".score-gauge-wrap");

  if (gaugeFill && gaugeValue && gaugeWrap) {
    const maxPercent = 100;
    const upDurationMs = 2200;
    const holdAtMaxMs = 2000;
    const downDurationMs = 1800;
    const totalLength = typeof gaugeFill.getTotalLength === "function"
      ? gaugeFill.getTotalLength()
      : 157;

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

      gaugeFill.style.strokeDasharray = `${totalLength}`;
      gaugeFill.style.strokeDashoffset = `${totalLength * (1 - progress)}`;
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
      // Disable CSS transition to avoid conflict with frame-by-frame animation.
      gaugeFill.style.transition = "none";
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

  if (uploadZone && fileInput) {
    // Prevent default drag behaviors
    ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
      uploadZone.addEventListener(eventName, preventDefaults, false);
      document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    // Highlight drop zone when item is dragged over it
    ["dragenter", "dragover"].forEach(eventName => {
      uploadZone.addEventListener(eventName, highlight, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
      uploadZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
      uploadZone.classList.add("dragover");
    }

    function unhighlight(e) {
      uploadZone.classList.remove("dragover");
    }

    // Handle dropped files
    uploadZone.addEventListener("drop", handleDrop, false);

    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      handleFiles(files);
    }

    // Handle selected files from input
    fileInput.addEventListener("change", function () {
      handleFiles(this.files);
    });

    function handleFiles(files) {
      if (files.length > 0) {
        const file = files[0];
        
        // Allowed formats: pdf, doc, docx
        const validTypes = [
          "application/pdf", 
          "application/msword", 
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ];
        
        if (validTypes.includes(file.type) || file.name.match(/\.(pdf|doc|docx)$/i)) {
          // Simulate a brief loading state, then redirect to the scan app
          const btn = uploadZone.querySelector('button');
          if(btn) {
            btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg> Analyzing...';
          }
          setTimeout(() => {
            window.location.href = '/scan';
          }, 1500);
        } else {
          alert("Please upload a PDF or DOCX file.");
        }
      }
    }
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
    let baseNumber = 1638;
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
