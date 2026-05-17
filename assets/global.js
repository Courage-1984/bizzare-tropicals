/**
 * Global theme bootstrap. Deferred to prioritize LCP.
 */
(function () {
  'use strict';

  try {
    var root = document.documentElement;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      root.classList.add('prefers-reduced-motion');
    }

    function syncPageVisibility() {
      root.classList.toggle('page-is-hidden', document.hidden);
    }

    syncPageVisibility();
    document.addEventListener('visibilitychange', syncPageVisibility);
  } catch (error) {
    console.error('Global theme script failed to initialize.', error);
  }
})();
