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
  } catch (error) {
    console.error('Global theme script failed to initialize.', error);
  }
})();
