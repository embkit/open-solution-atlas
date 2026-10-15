/* Open Solution Atlas — copy-to-clipboard for the generated prompt bundles.

   Progressive enhancement: every prompt is a real Markdown file in
   `<pack>/prompts/`, so with JavaScript disabled the action is a link the
   reader can open and copy from. This only replaces that click with one
   click, and it degrades to a message when the clipboard API is unavailable.

   Nothing is fetched at load time: the text is already in the page for the
   inline prompt, and a `.md` sibling for the rest.

   The transient feedback strings come from the site's string catalog through
   `window.OSA_I18N` (assets/i18n.js), like every other string the page writes:
   a reader who switches language must not get a Chinese toast on an English
   page. */

(function () {
  "use strict";

  function tr(key) {
    return window.OSA_I18N ? window.OSA_I18N.t(key) : key;
  }

  function flash(button, message, ok) {
    var original = button.textContent;
    button.textContent = message;
    button.classList.toggle("copy-ok", !!ok);
    button.classList.toggle("copy-fail", !ok);
    window.setTimeout(function () {
      button.textContent = original;
      button.classList.remove("copy-ok", "copy-fail");
    }, 1600);
  }

  function copyText(text, button) {
    if (navigator.clipboard && window.isSecureContext !== false) {
      navigator.clipboard.writeText(text).then(
        function () { flash(button, tr("copy.ok"), true); },
        function () { flash(button, tr("copy.fail"), false); }
      );
      return;
    }
    // Older browsers and file:// origins have no async clipboard: fall back to
    // a temporary selection rather than pretending the prompt was copied.
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(area);
    flash(button, ok ? tr("copy.ok") : tr("copy.fail"), ok);
  }

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    var target = document.getElementById(button.getAttribute("data-copy"));
    button.addEventListener("click", function () {
      copyText(target.value || target.textContent, button);
    });
  });

  document.querySelectorAll("[data-copy-url]").forEach(function (button) {
    var url = button.getAttribute("data-copy-url");
    button.addEventListener("click", function () {
      fetch(url).then(
        function (r) { return r.ok ? r.text() : Promise.reject(r.status); }
      ).then(
        function (text) { copyText(text, button); },
        function () { flash(button, tr("copy.read_fail"), false); }
      );
    });
  });
})();
