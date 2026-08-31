(function () {
  "use strict";

  var root = document.documentElement;
  var themeToggle = document.getElementById("theme-toggle");
  var navToggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("nav");
  var yearEl = document.getElementById("year");

  // Year in footer
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // Theme toggle (persisted per-browser)
  function applyTheme(theme) {
    if (theme === "light" || theme === "dark") {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
    if (themeToggle) {
      var isDark =
        theme === "dark" ||
        (!theme && window.matchMedia("(prefers-color-scheme: dark)").matches);
      themeToggle.textContent = isDark ? "☀️" : "🌙";
    }
  }

  var savedTheme = null;
  try {
    savedTheme = localStorage.getItem("theme");
  } catch (e) {
    /* storage unavailable, ignore */
  }
  applyTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var isDark =
        current === "dark" ||
        (!current && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = isDark ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        /* storage unavailable, ignore */
      }
    });
  }

  // Mobile nav toggle
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("open");
      });
    });
  }
})();
