/* ==========================================================================
   BOOKSHELF — INTERACTIONS
   ========================================================================== */
(function () {
  "use strict";

  /* -------------------------------------------------- */
  /* Footer year                                          */
  /* -------------------------------------------------- */
  try {
    var yearEl = document.getElementById("year");
    if (yearEl) yearEl.textContent = new Date().getFullYear();
  } catch (e) {
    console.error("[bookshelf] footer year:", e);
  }

  /* -------------------------------------------------- */
  /* Sticky navbar background on scroll                  */
  /* -------------------------------------------------- */
  try {
    var navbar = document.getElementById("navbar");
    if (navbar) {
      var handleNavScroll = function () {
        if (window.scrollY > 8) {
          navbar.classList.add("is-scrolled");
        } else {
          navbar.classList.remove("is-scrolled");
        }
      };
      handleNavScroll();
      window.addEventListener("scroll", handleNavScroll, { passive: true });
    }
  } catch (e) {
    console.error("[bookshelf] navbar scroll:", e);
  }

  /* -------------------------------------------------- */
  /* Mobile hamburger menu                                */
  /* -------------------------------------------------- */
  try {
    var hamburger = document.getElementById("hamburger");
    var mobileMenu = document.getElementById("mobileMenu");

    if (hamburger && mobileMenu) {
      var closeMobileMenu = function () {
        mobileMenu.classList.remove("is-open");
        hamburger.setAttribute("aria-expanded", "false");
      };

      hamburger.addEventListener("click", function () {
        var isOpen = mobileMenu.classList.toggle("is-open");
        hamburger.setAttribute("aria-expanded", String(isOpen));
      });

      mobileMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", closeMobileMenu);
      });
    }
  } catch (e) {
    console.error("[bookshelf] hamburger menu:", e);
  }

  /* -------------------------------------------------- */
  /* Expandable nav search                                */
  /* -------------------------------------------------- */
  try {
    var searchToggle = document.getElementById("searchToggle");
    var navSearch = document.getElementById("navSearch");

    if (searchToggle && navSearch) {
      searchToggle.addEventListener("click", function () {
        var isOpen = navSearch.classList.toggle("is-open");

        if (isOpen) {
          var input = navSearch.querySelector("input");
          if (input) {
            window.setTimeout(function () {
              input.focus();
            }, 200);
          }
        }
      });
    }
  } catch (e) {
    console.error("[bookshelf] nav search:", e);
  }

  /* -------------------------------------------------- */
  /* Dark mode toggle (persisted)                         */
  /* -------------------------------------------------- */
  try {
    var themeToggle = document.getElementById("themeToggle");
    var iconSun = document.getElementById("iconSun");
    var iconMoon = document.getElementById("iconMoon");
    var root = document.documentElement;
    var STORAGE_KEY = "bookshelf-theme";

    var applyTheme = function (theme) {
      if (theme === "dark") {
        root.setAttribute("data-theme", "dark");
        if (iconSun) iconSun.style.display = "none";
        if (iconMoon) iconMoon.style.display = "block";
      } else {
        root.removeAttribute("data-theme");
        if (iconSun) iconSun.style.display = "block";
        if (iconMoon) iconMoon.style.display = "none";
      }
    };

    var savedTheme = null;
    try {
      savedTheme = localStorage.getItem(STORAGE_KEY);
    } catch (storageErr) {
      /* localStorage unavailable */
    }

    var prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;

    applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

    if (themeToggle) {
      themeToggle.addEventListener("click", function () {
        var isDark = root.getAttribute("data-theme") === "dark";
        var next = isDark ? "light" : "dark";
        applyTheme(next);
        try {
          localStorage.setItem(STORAGE_KEY, next);
        } catch (storageErr) {
          /* ignore persistence errors */
        }
      });
    }
  } catch (e) {
    console.error("[bookshelf] theme toggle:", e);
  }

  /* -------------------------------------------------- */
  /* Scroll reveal animations                             */
  /* -------------------------------------------------- */
  try {
    var revealEls = document.querySelectorAll(".reveal");

    if (revealEls.length) {
      if ("IntersectionObserver" in window) {
        var revealObserver = new IntersectionObserver(function (entries, observer) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        }, { threshold: 0.15, rootMargin: "0px 0px -60px 0px" });

        revealEls.forEach(function (el) {
          el.classList.add("reveal--pending");
          revealObserver.observe(el);
        });
      } else {
        /* No IntersectionObserver support — show content immediately */
        revealEls.forEach(function (el) {
          el.classList.add("is-visible");
        });
      }
    }
  } catch (e) {
    console.error("[bookshelf] reveal animations:", e);
    /* Failsafe: never let content stay hidden because of a JS error */
    document.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* -------------------------------------------------- */
  /* Animated stat counters                               */
  /* -------------------------------------------------- */
  try {
    var statNumbers = document.querySelectorAll(".stat__number");

    var animateCount = function (el) {
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      var duration = 1600;
      var startTime = null;

      function step(timestamp) {
        if (startTime === null) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var value = Math.floor(eased * target);
        el.textContent = value.toLocaleString();
        if (progress < 1) {
          window.requestAnimationFrame(step);
        } else {
          el.textContent = target.toLocaleString();
        }
      }
      window.requestAnimationFrame(step);
    };

    if (statNumbers.length) {
      if ("IntersectionObserver" in window) {
        var statsObserver = new IntersectionObserver(function (entries, observer) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              animateCount(entry.target);
              observer.unobserve(entry.target);
            }
          });
        }, { threshold: 0.4 });
        statNumbers.forEach(function (el) {
          statsObserver.observe(el);
        });
      } else {
        statNumbers.forEach(function (el) {
          el.textContent = (parseInt(el.getAttribute("data-count"), 10) || 0).toLocaleString();
        });
      }
    }
  } catch (e) {
    console.error("[bookshelf] stat counters:", e);
  }

  /* -------------------------------------------------- */
  /* Dynamic progress indicators                          */
  /* -------------------------------------------------- */
  try {
    document.querySelectorAll(".progress-ring__value[data-progress]").forEach(function (el) {
      el.style.setProperty("--progress", el.getAttribute("data-progress") || "0");
    });

    document.querySelectorAll(".progress-bar__fill[data-progress]").forEach(function (el) {
      var progress = parseFloat(el.getAttribute("data-progress")) || 0;
      el.style.width = Math.max(0, Math.min(progress, 100)) + "%";
    });
  } catch (e) {
    console.error("[bookshelf] progress indicators:", e);
  }

  /* -------------------------------------------------- */
  /* Newsletter form (front-end only placeholder)         */
  /* -------------------------------------------------- */
  try {
    var newsletterForm = document.getElementById("newsletterForm");
    var newsletterNote = document.getElementById("newsletterNote");

    if (newsletterForm) {
      newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault();
        var emailInput = document.getElementById("newsletterEmail");
        var email = emailInput ? emailInput.value.trim() : "";
        if (email && newsletterNote) {
          newsletterNote.textContent = "Thanks — check " + email + " for a confirmation email.";
          newsletterForm.reset();
        }
      });
    }
  } catch (e) {
    console.error("[bookshelf] newsletter form:", e);
  }
})();