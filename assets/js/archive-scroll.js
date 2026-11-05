/* Desktop-only row paging for the archive. It never changes the archive data. */
(() => {
  'use strict';
  if (!window.matchMedia || !window.requestAnimationFrame) return;

  const desktop = window.matchMedia('(min-width:761px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion:reduce)');
  const QUIET_MS = 200;
  const MOTION_FALLBACK_MS = 700;
  let lastWheelAt = -Infinity;
  let motionUntil = 0;
  let gestureUsed = false;
  let wheelAmount = 0;
  let topFrame = 0;
  let interacted = false;
  let ownsRestoration = false;
  let previousRestoration;
  let lastCategory = category();

  const now = () => window.performance.now();
  const scrollY = () => window.scrollY || 0;
  function category() {
    return (window.location.hash.match(/(?:^#|&)type=([^&]+)/) || [])[1] || 'pass';
  }
  function clearGesture() {
    lastWheelAt = -Infinity;
    motionUntil = 0;
    gestureUsed = false;
    wheelAmount = 0;
  }
  function overlayOpen() {
    return document.body.style.overflow === 'hidden' ||
      document.documentElement.style.overflow === 'hidden' ||
      document.body.classList.contains('viewer-open') ||
      Boolean(document.querySelector('dialog[open], [aria-modal="true"][aria-hidden="false"]'));
  }
  function nativeTarget(target) {
    let el = target && (target.nodeType === 3 ? target.parentElement : target);
    if (el?.closest?.('input, textarea, select, option, [contenteditable]:not([contenteditable="false"])')) return true;
    while (el && el !== document.body && el !== document.documentElement) {
      const style = window.getComputedStyle(el);
      if (/(auto|scroll|overlay)/.test(style.overflowY) && el.scrollHeight > el.clientHeight + 1) return true;
      el = el.parentElement;
    }
    return false;
  }
  function queueTop(force = true) {
    if (!desktop.matches) return;
    if (topFrame) window.cancelAnimationFrame(topFrame);
    topFrame = window.requestAnimationFrame(() => {
      topFrame = 0;
      if (!desktop.matches || (!force && interacted)) return;
      clearGesture();
      window.scrollTo({top: 0, left: 0, behavior: 'instant'});
    });
  }
  function viewportMode() {
    clearGesture();
    if (desktop.matches) {
      if (!ownsRestoration && 'scrollRestoration' in window.history) {
        previousRestoration = window.history.scrollRestoration;
        window.history.scrollRestoration = 'manual';
        ownsRestoration = true;
      }
      queueTop(false);
    } else {
      if (topFrame) window.cancelAnimationFrame(topFrame);
      topFrame = 0;
      if (ownsRestoration && window.history.scrollRestoration === 'manual') {
        window.history.scrollRestoration = previousRestoration;
      }
      ownsRestoration = false;
    }
  }
  function rowStops() {
    const feed = document.getElementById('feed');
    if (!feed) return [];
    const viewport = window.innerHeight || document.documentElement.clientHeight;
    const scroller = document.scrollingElement || document.documentElement;
    const maxY = Math.max(0, scroller.scrollHeight - viewport);
    if (maxY < 2) return [];
    const toolbar = document.querySelector('.toolbar-shell');
    const offset = (toolbar ? toolbar.getBoundingClientRect().height : 0) + 12;
    const readable = Math.max(120, viewport - offset - 16);
    const pageStep = Math.max(100, readable * 0.85);
    const y = scrollY();
    const rows = [];
    // Read the current grid geometry, not an assumed number of columns. Re-read
    // for each new gesture so lazy images and content-visibility can settle.
    for (const entry of feed.querySelectorAll(':scope > .entry')) {
      const rect = entry.getBoundingClientRect();
      if (!rect.width || !rect.height) continue;
      const top = rect.top + y;
      const bottom = rect.bottom + y;
      let row = rows.find(candidate => Math.abs(candidate.top - top) < 3);
      if (row) row.bottom = Math.max(row.bottom, bottom);
      else rows.push({top, bottom});
    }
    if (!rows.length) return [];
    rows.sort((a, b) => a.top - b.top);
    const heading = document.querySelector('.section-head');
    const headingTop = heading ? heading.getBoundingClientRect().top + y - offset : rows[0].top - offset;
    const stops = [0];
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      const start = Math.max(0, i ? row.top - offset : Math.min(headingTop, row.top - offset));
      stops.push(start);
      // A short desktop window must still be able to read the bottom of a tall
      // card. Such rows receive intermediate stops instead of skipping text.
      const lastReadable = Math.max(start, row.bottom - viewport + 16);
      for (let middle = start + pageStep; middle < lastReadable - 3; middle += pageStep) stops.push(middle);
      if (lastReadable > start + 3) stops.push(lastReadable);
    }
    stops.push(maxY); // The footer remains reachable after the final card row.
    const sorted = stops.map(value => Math.max(0, Math.min(maxY, value))).sort((a, b) => a - b);
    return sorted.filter((value, i) => !i || value - sorted[i - 1] > 3);
  }
  function onWheel(event) {
    interacted = true;
    if (!desktop.matches || event.defaultPrevented || event.cancelable === false ||
        event.ctrlKey || event.metaKey || event.shiftKey || event.altKey ||
        !Number.isFinite(event.deltaY) || !event.deltaY ||
        Math.abs(event.deltaX || 0) > Math.abs(event.deltaY)) return;
    if (overlayOpen() || nativeTarget(event.target)) {
      clearGesture();
      return;
    }
    const feed = document.getElementById('feed');
    if (!feed?.querySelector('.entry')) return;
    const time = now();
    if (time - lastWheelAt > QUIET_MS && time >= motionUntil) {
      gestureUsed = false;
      wheelAmount = 0;
    }
    lastWheelAt = time;
    if (gestureUsed || time < motionUntil) {
      event.preventDefault();
      return;
    }
    const stops = rowStops();
    if (stops.length < 2) return;
    const direction = Math.sign(event.deltaY);
    const y = scrollY();
    const next = direction > 0 ? stops.find(stop => stop > y + 3) : [...stops].reverse().find(stop => stop < y - 3);
    if (next === undefined) return;
    event.preventDefault();
    const units = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? window.innerHeight : 1;
    wheelAmount += event.deltaY * units;
    if (Math.abs(wheelAmount) < 6) return;
    gestureUsed = true;
    motionUntil = time + (reducedMotion.matches ? 0 : MOTION_FALLBACK_MS);
    window.scrollTo({top: next, left: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  }

  window.addEventListener('wheel', onWheel, {passive: false});
  window.addEventListener('scrollend', () => { motionUntil = 0; }, {passive: true});
  window.addEventListener('resize', clearGesture, {passive: true});
  window.addEventListener('pointerdown', () => { interacted = true; clearGesture(); }, {passive: true});
  window.addEventListener('keydown', () => { interacted = true; clearGesture(); }, {passive: true});
  window.addEventListener('load', () => queueTop(false));
  window.addEventListener('pageshow', event => {
    if (event.persisted) interacted = false;
    queueTop(false);
  });
  window.addEventListener('hashchange', () => {
    const next = category();
    if (next !== lastCategory) {
      lastCategory = next;
      queueTop();
    }
  });
  document.addEventListener('click', event => {
    if (event.target?.closest?.('.category')) {
      lastCategory = category();
      queueTop();
    }
  });
  if (desktop.addEventListener) desktop.addEventListener('change', viewportMode);
  else if (desktop.addListener) desktop.addListener(viewportMode);
  viewportMode();
})();
