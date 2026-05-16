/**
 * Global scroll-reveal animations (.reveal-up).
 */
(function () {
  'use strict';

  var STAGGER_PARENT_SELECTOR = '[data-reveal-stagger]';
  var REVEAL_SELECTOR = '.reveal-up:not(.is-visible)';
  var OBSERVER_OPTIONS = {
    root: null,
    rootMargin: '0px 0px -8% 0px',
    threshold: 0.12,
  };

  var observer = null;
  var staggerCounters = new WeakMap();

  function prefersReducedMotion() {
    try {
      return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (error) {
      return false;
    }
  }

  function revealImmediately(elements) {
    elements.forEach(function (element) {
      element.classList.add('is-visible');
      element.style.transitionDelay = '';
    });
  }

  function getStaggerDelay(element) {
    if (element.closest(STAGGER_PARENT_SELECTOR)) {
      return 0;
    }

    var count = staggerCounters.get(element.parentElement) || 0;
    staggerCounters.set(element.parentElement, count + 1);
    return count * 0.08;
  }

  function ensureObserver() {
    if (observer) {
      return observer;
    }

    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) {
          return;
        }

        var element = entry.target;
        var delay = getStaggerDelay(element);
        element.style.transitionDelay = delay > 0 ? delay + 's' : '';
        element.classList.add('is-visible');
        observer.unobserve(element);
      });
    }, OBSERVER_OPTIONS);

    return observer;
  }

  function initRevealUp(scope) {
    var root = scope && scope.querySelectorAll ? scope : document;
    var elements = [];

    if (root.matches && root.matches('.reveal-up') && !root.classList.contains('is-visible')) {
      elements.push(root);
    }

    root.querySelectorAll(REVEAL_SELECTOR).forEach(function (element) {
      elements.push(element);
    });

    if (!elements.length) {
      return;
    }

    if (prefersReducedMotion()) {
      revealImmediately(elements);
      return;
    }

    var revealObserver = ensureObserver();
    elements.forEach(function (element) {
      revealObserver.observe(element);
    });
  }

  function resetStaggerCounters(scope) {
    var root = scope && scope.querySelectorAll ? scope : document;
    root.querySelectorAll(STAGGER_PARENT_SELECTOR).forEach(function (parent) {
      staggerCounters.set(parent, 0);
    });
  }

  window.ThemeReveal = {
    init: initRevealUp,
    reset: resetStaggerCounters,
  };

  function onReady() {
    initRevealUp(document);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }

  document.addEventListener('shopify:section:load', function (event) {
    resetStaggerCounters(event.target);
    initRevealUp(event.target);
  });
})();
