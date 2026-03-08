document.addEventListener("DOMContentLoaded", () => {
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
            window.location.href = 'scan.html';
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

  if (reviewsTrack && reviewsPrevBtn && reviewsNextBtn && reviewsProgressFill) {
    const getScrollStep = () => {
      const card = reviewsTrack.querySelector(".review-card");
      if (!card) return 280;
      const styles = window.getComputedStyle(reviewsTrack);
      const gap = parseFloat(styles.columnGap || styles.gap || "16");
      return card.getBoundingClientRect().width + gap;
    };

    const updateReviewsProgress = () => {
      const maxScroll = reviewsTrack.scrollWidth - reviewsTrack.clientWidth;
      const ratio = maxScroll > 0 ? reviewsTrack.scrollLeft / maxScroll : 0;
      const fillPercent = 20 + ratio * 80;
      reviewsProgressFill.style.width = `${fillPercent}%`;
    };

    reviewsPrevBtn.addEventListener("click", () => {
      reviewsTrack.scrollBy({ left: -getScrollStep(), behavior: "smooth" });
    });

    reviewsNextBtn.addEventListener("click", () => {
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
    
    // Function to generate random interval between 5 and 15 seconds
    const getRandomInterval = () => Math.floor(Math.random() * (15000 - 5000 + 1)) + 5000;
    
    const updateCounter = () => {
      baseNumber += 1;
      // Format number with commas
      resumesCounter.textContent = baseNumber.toLocaleString('en-US');
      
      // Add a slight animation class
      resumesCounter.style.transition = "color 0.3s ease";
      resumesCounter.style.color = "var(--primary)";
      
      setTimeout(() => {
        resumesCounter.style.color = "inherit";
      }, 300);
      
      // Set next timeout
      setTimeout(updateCounter, getRandomInterval());
    };

    // Start the counter
    setTimeout(updateCounter, getRandomInterval());
  }
});
