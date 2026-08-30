/* ==========================================================================
   OPFOR app.js — interaction layer
   --------------------------------------------------------------------------
   Zero dependencies. Progressive enhancement: the site is fully usable
   without JS (server-rendered markdown, Material's own search); this layer
   adds the tactile experience — HUD counters, filter matrix, command
   palette bridge, terminal code chrome, scroll reveal.
   ========================================================================== */
(function () {
  "use strict";

  var REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ============================================================ mesh ===== */
  /* Material has no container for a fixed layer; ensure it exists on every
     page (template injects it, but older cached pages may lack it). */
  function ensureMesh() {
    if (document.querySelector(".opfor-mesh")) return;
    var mesh = document.createElement("div");
    mesh.className = "opfor-mesh";
    mesh.setAttribute("aria-hidden", "true");
    document.body.insertBefore(mesh, document.body.firstChild);
  }

  /* ======================================================== reveal ====== */
  /* Cards/sections fade+rise as they enter the viewport. */
  function initReveal() {
    var els = document.querySelectorAll(".opfor-reveal");
    if (!els.length || REDUCED || !("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("is-visible");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    els.forEach(function (el, i) {
      el.style.transitionDelay = ((i % 3) * 70) + "ms";
      io.observe(el);
    });
  }

  /* ====================================================== counters ====== */
  /* HUD stat values count up from 0 when they scroll into view.
     data-count may be bare (value = textContent) or ="N" (explicit). */
  function initCounters() {
    var vals = document.querySelectorAll(".opfor-stat__value[data-count]");
    if (!vals.length) return;
    function endValue(el) {
      var attr = el.getAttribute("data-count");
      if (attr && attr.trim() && !isNaN(parseInt(attr, 10))) return parseInt(attr, 10);
      return parseInt(el.textContent, 10) || 0;
    }
    function animate(el) {
      var end = endValue(el);
      if (REDUCED) { render(el, end); return; }
      var start = performance.now(), dur = 900;
      function step(now) {
        var p = Math.min(1, (now - start) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        render(el, Math.round(end * eased));
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    function render(el, n) {
      var unit = el.querySelector(".unit");
      var unitTxt = unit ? unit.outerHTML : "";
      el.innerHTML = n + unitTxt;
    }
    if (!("IntersectionObserver" in window)) { vals.forEach(animate); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animate(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    vals.forEach(function (el) { io.observe(el); });
  }

  /* ==================================================== filter matrix === */
  /* Multi-axis: platform / difficulty / vector. A card matches when it hits
     >=1 active chip on EVERY axis that has active chips. Runs against cards
     inside the ops grid only (#opfor-grid), never decorative cards. */
  function initFilters() {
    var grid = document.getElementById("opfor-grid");
    var wrap = document.getElementById("opfor-filters");
    if (!grid || !wrap) return;

    var chips = Array.prototype.slice.call(wrap.querySelectorAll(".opfor-chip[data-filter]"));
    var clearBtn = document.getElementById("opfor-clear");
    var state = { platform: {}, difficulty: {}, vector: {} };
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".opfor-card"));

    function apply() {
      var any = false;
      cards.forEach(function (card) {
        var match = true;
        ["platform", "difficulty", "vector"].forEach(function (ax) {
          var active = Object.keys(state[ax]).filter(function (k) { return state[ax][k]; });
          if (active.length) {
            any = true;
            var cardVal = card.getAttribute("data-" + ax) || "";
            if (active.indexOf(cardVal) === -1) match = false;
          }
        });
        card.style.display = match ? "" : "none";
      });
      if (clearBtn) clearBtn.style.visibility = any ? "visible" : "hidden";
    }

    function toggle(chip) {
      var ax = chip.getAttribute("data-filter");
      var val = chip.getAttribute("data-value");
      state[ax][val] = !state[ax][val];
      chip.setAttribute("aria-pressed", state[ax][val] ? "true" : "false");
      apply();
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () { toggle(chip); });
      chip.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(chip); }
      });
    });
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        chips.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
        state = { platform: {}, difficulty: {}, vector: {} };
        apply();
      });
    }
    apply();
  }

  /* ==================================================== HUD numbers ===== */
  /* Fill chip count badges from the actual card data so they never lie. */
  function initChipCounts() {
    var grid = document.getElementById("opfor-grid");
    if (!grid) return;
    var cards = grid.querySelectorAll(".opfor-card");
    ["platform", "difficulty", "vector"].forEach(function (ax) {
      var counts = {};
      cards.forEach(function (c) {
        var v = c.getAttribute("data-" + ax);
        if (v) counts[v] = (counts[v] || 0) + 1;
      });
      Object.keys(counts).forEach(function (v) {
        var badge = document.querySelector('[data-hud="' + ax + "-" + v + '"]');
        if (badge) badge.textContent = counts[v];
      });
    });
  }

  /* ===================================================== palette ====== */
  /* '/' or Ctrl-K focuses Material's built-in search — keep the muscle
     memory of a command palette without rebuilding it. */
  function initPalette() {
    document.addEventListener("keydown", function (e) {
      var target = e.target || {};
      var typing = target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable;
      if (typing) return;
      if (e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k")) {
        e.preventDefault();
        var btn = document.querySelector('.md-header .md-search-icon[for="search"], .md-header button.md-search-icon');
        if (btn) btn.click();
        var input = document.querySelector(".md-search__input");
        if (input) input.focus();
      }
    });
  }

  /* ============================================== terminal chrome ====== */
  /* Wrap shell-looking code blocks in a terminal window bar: traffic dots,
     kalifox prompt label, per-block copy with feedback. Material emits
     <div class="highlight"><pre><code> without language classes, so we
     detect shells from block classes + first-line heuristics. */
  var SHELL_HINTS = /^\s*(\$|>|#(?!#)|sudo |nmap |ffuf |gobuster |hydra |curl |nc |ncat |python[23]? |ssh |cd |ls |cat |find |export |echo |mkdir |cp |mv |chmod |chown |wget |git |crackmapexec |netexec |impacket|bash |sh |\.\/|sqlmap |searchsploit |msfconsole|hashcat |john |scp |ftp )/;

  function looksLikeShell(block, code) {
    var pre = block.querySelector("pre");
    var blockClass = (block.className || "") + " " + ((pre && pre.className) || "");
    if (/language-(bash|sh|shell|console|terminal|powershell|ps1|zsh)/i.test(blockClass)) return true;
    if (/language-(php|python|js|javascript|json|yaml|html|css|http|sql|c|cpp|java|go|rb|text|md)/i.test(blockClass)) return false;
    // heuristic: prompt-shaped first non-empty line
    var lines = (code || "").split("\n");
    for (var i = 0; i < Math.min(lines.length, 3); i++) {
      var l = lines[i];
      if (!l.trim()) continue;
      return SHELL_HINTS.test(l);
    }
    return false;
  }

  function initTerminalChrome() {
    var blocks = document.querySelectorAll(".md-typeset .highlight");
    blocks.forEach(function (block) {
      var pre = block.querySelector("pre");
      if (!pre || block.classList.contains("opfor-wrapped")) return;
      var code = pre.querySelector("code") || pre;
      var text = code.textContent || "";
      if (!looksLikeShell(block, text)) return;
      block.classList.add("opfor-wrapped");

      var bar = document.createElement("div");
      bar.className = "opfor-termbar";
      bar.setAttribute("role", "presentation");
      bar.innerHTML =
        '<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>' +
        '<span class="t-label">daniel@kali</span>' +
        '<span class="t-cmdline"></span>';

      var copy = document.createElement("button");
      copy.className = "t-copy";
      copy.type = "button";
      copy.setAttribute("aria-label", "Copy command to clipboard");
      copy.textContent = "COPY";
      copy.addEventListener("click", function () {
        copyText(text).then(function () {
          copy.textContent = "COPIED ✓";
          copy.classList.add("is-copied");
          setTimeout(function () {
            copy.textContent = "COPY";
            copy.classList.remove("is-copied");
          }, 1600);
        });
      });
      bar.appendChild(copy);

      block.insertBefore(bar, block.firstChild);
      var first = text.split("\n")[0] || "";
      var cmdEl = bar.querySelector(".t-cmdline");
      if (cmdEl) cmdEl.textContent = first.slice(0, 48) + (first.length > 48 ? "…" : "");
    });
  }

  function copyText(text) {
    /* Best-effort copy with a hard 400ms ceiling so the UI feedback never
       hangs: async clipboard first, legacy execCommand fallback, and a race
       timeout for environments where the clipboard promise pends
       (unfocused document, hardened browsers, embedded views). */
    var timeout = new Promise(function (resolve) { setTimeout(resolve, 400); });
    var attempt;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      attempt = navigator.clipboard.writeText(text).catch(function () {
        return legacyCopy(text);
      });
    } else {
      attempt = Promise.resolve(legacyCopy(text));
    }
    return Promise.race([attempt, timeout]);
  }

  function legacyCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-1000px";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* best effort */ }
    document.body.removeChild(ta);
  }

  /* ================================================== boot sequence ===== */
  function boot() {
    ensureMesh();
    initReveal();
    initCounters();
    initChipCounts();
    initFilters();
    initPalette();
    initTerminalChrome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
