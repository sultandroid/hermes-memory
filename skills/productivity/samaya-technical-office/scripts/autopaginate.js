/**
 * A4 Auto-Paginate v2.0 — Samaya BIM Unit
 * Detects content overflow in .sheet elements and dynamically
 * splits overflowing content into new .sheet pages.
 * Splits at natural break points (headings, tables, alerts).
 *
 * Include before </body> in every Samaya bilingual HTML report.
 * CSS must have: .sheet { max-height: 297mm; overflow: hidden; }
 * for detection to work. Print CSS should use overflow:visible.
 */
(function() {
  'use strict';

  var A4_PX = 1123;  // 297mm @ 96dpi
  var TOLERANCE = 8;

  function measure(el) {
    return el.scrollHeight - el.clientHeight;
  }

  function findBreakPoint(sheet, overflowPx) {
    var children = Array.from(sheet.children);
    var accumulated = 0;
    for (var i = children.length - 1; i >= 0; i--) {
      var ch = children[i].offsetHeight || 0;
      accumulated += ch;
      if (accumulated > overflowPx * 0.6) {
        var tag = children[i].tagName.toLowerCase();
        if (tag.match(/^(h[1-3]|table|section)/)) return i;
        return i;
      }
    }
    return Math.max(1, Math.ceil(children.length / 2));
  }

  function paginate() {
    var sheets = document.querySelectorAll('.sheet');
    var parent = sheets[0] ? sheets[0].parentNode : null;
    if (!parent) return;

    var pageCounter = 1;
    var allSheets = Array.from(sheets);

    allSheets.forEach(function(sheet) {
      var overflow = measure(sheet);
      var maxRetries = 10;
      while (overflow > TOLERANCE && maxRetries > 0) {
        maxRetries--;
        var cloned = sheet.cloneNode(false);
        var splitAt = findBreakPoint(sheet, overflow);
        var children = Array.from(sheet.children);
        var moved = 0;
        for (var i = splitAt; i < children.length; i++) {
          cloned.appendChild(children[i]);
          moved++;
          i--;
        }
        if (moved === 0) break;
        sheet.parentNode.insertBefore(cloned, sheet.nextSibling);
        pageCounter++;
        overflow = measure(sheet);
      }
      pageCounter++;
    });

    // Fix all page numbers
    var finalSheets = document.querySelectorAll('.sheet');
    var total = finalSheets.length;
    finalSheets.forEach(function(s, i) {
      var f = s.querySelector('.page-footer');
      if (f) {
        f.innerHTML = f.innerHTML.replace(/Page \d+ of \d+/g, 'Page ' + (i+1) + ' of ' + total);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paginate);
  } else {
    paginate();
  }
})();
