/* Open Solution Atlas — copy-to-clipboard for the generated prompt bundles.

   Progressive enhancement: every prompt is a real Markdown file in
   `<pack>/prompts/`, so with JavaScript disabled the action is a link the
   reader can open and copy from. This only replaces that click with one
   click, and it degrades to a message when the clipboard API is unavailable.

   Nothing is fetched at load time: the text is already in the page for the
   inline prompt, and a `.md` sibling for the rest. */

(function () {
  "use strict";

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
        function () { flash(button, "已复制", true); },
        function () { flash(button, "复制失败，请手动选择", false); }
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
    flash(button, ok ? "已复制" : "复制失败，请手动选择", ok);
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
        function () { flash(button, "读取失败，请打开文件手动复制", false); }
      );
    });
  });
})();
