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

    function resetTransientUiLocks() {
      document.documentElement.classList.remove('is-scroll-locked');

      document.querySelectorAll('[data-collection-grid-section]').forEach(function (section) {
        section.classList.remove('collection-grid-section--filters-open', 'collection-grid-section--busy');
      });

      document.querySelectorAll('.cultivation-filter.is-open').forEach(function (drawer) {
        drawer.classList.remove('is-open');
        drawer.setAttribute('aria-hidden', 'true');
      });
    }

    window.addEventListener('pageshow', function (event) {
      if (event.persisted) {
        resetTransientUiLocks();
      }
    });

    window.BT = window.BT || {};

    /**
     * @deprecated Use carousel.js bindCarouselWheelScroll via BT.initScrollCarousel.
     * Kept for backward compatibility — no longer blocks vertical page scroll.
     */
    window.BT.bindCarouselWheelGuard = function () {};

    /**
     * Pauses carousel autoplay while the section is off-screen.
     * @returns {function|undefined} disconnect
     */
    window.BT.bindCarouselInView = function (root, controls) {
      if (!root || !controls || root.dataset.inViewGuard === 'true') {
        return;
      }

      if (!('IntersectionObserver' in window)) {
        return;
      }

      root.dataset.inViewGuard = 'true';

      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              if (typeof controls.onEnter === 'function') {
                controls.onEnter();
              }
            } else if (typeof controls.onLeave === 'function') {
              controls.onLeave();
            }
          });
        },
        { threshold: 0.12, rootMargin: '0px 0px -5% 0px' }
      );

      observer.observe(root);

      return function () {
        observer.disconnect();
        delete root.dataset.inViewGuard;
      };
    };
  } catch (error) {
    console.error('Global theme script failed to initialize.', error);
  }
})();
