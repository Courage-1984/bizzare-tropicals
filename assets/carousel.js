/**
 * Shared horizontal scroll carousel — touch-friendly, no page-scroll hijacking.
 */
(function () {
  'use strict';

  window.BT = window.BT || {};

  var DEFAULT_AUTOPLAY_MS = 6000;
  var DEFAULT_RESUME_MS = 8000;

  function prefersReducedMotion() {
    try {
      return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (error) {
      return false;
    }
  }

  function matchesMinWidth(px) {
    try {
      return window.matchMedia('(min-width: ' + px + 'px)').matches;
    } catch (error) {
      return false;
    }
  }

  function getScrollStep(track, itemSelector) {
    var firstItem = track.querySelector(itemSelector || '[data-carousel-item], [data-carousel-slide]');
    if (!firstItem) {
      firstItem = track.firstElementChild;
    }

    if (!firstItem) {
      return track.clientWidth * 0.85;
    }

    var flexRow = firstItem.parentElement || track;
    var rowStyles = window.getComputedStyle(flexRow);
    var gap = parseFloat(rowStyles.columnGap || rowStyles.gap || '0') || 0;

    if (gap === 0 && flexRow !== track) {
      var trackStyles = window.getComputedStyle(track);
      gap = parseFloat(trackStyles.columnGap || trackStyles.gap || '0') || 0;
    }

    return firstItem.offsetWidth + gap;
  }

  function bindCarouselWheelScroll(scrollable) {
    if (!scrollable || scrollable.dataset.wheelScroll === 'true') {
      return;
    }

    scrollable.dataset.wheelScroll = 'true';

    scrollable.addEventListener(
      'wheel',
      function (event) {
        var absX = Math.abs(event.deltaX);
        var absY = Math.abs(event.deltaY);

        if (absX <= absY) {
          return;
        }

        if (scrollable.scrollWidth <= scrollable.clientWidth + 2) {
          return;
        }

        var maxScroll = scrollable.scrollWidth - scrollable.clientWidth;
        var atStart = scrollable.scrollLeft <= 1;
        var atEnd = scrollable.scrollLeft >= maxScroll - 1;

        if ((event.deltaX < 0 && atStart) || (event.deltaX > 0 && atEnd)) {
          return;
        }

        event.preventDefault();
        scrollable.scrollLeft += event.deltaX;
      },
      { passive: false }
    );
  }

  function destroyScrollCarousel(root) {
    if (!root || !root._btCarouselState) {
      return;
    }

    try {
      var state = root._btCarouselState;

      if (state.autoplayTimer) {
        clearInterval(state.autoplayTimer);
      }

      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
      }

      state.listeners.forEach(function (entry) {
        entry.target.removeEventListener(entry.type, entry.handler, entry.options);
      });

      if (typeof state.inViewDisconnect === 'function') {
        state.inViewDisconnect();
      }

      if (state.mediaQuery && typeof state.onMediaChange === 'function') {
        if (typeof state.mediaQuery.removeEventListener === 'function') {
          state.mediaQuery.removeEventListener('change', state.onMediaChange);
        } else if (typeof state.mediaQuery.removeListener === 'function') {
          state.mediaQuery.removeListener(state.onMediaChange);
        }
      }
    } catch (error) {
      console.error('Carousel: teardown failed.', error);
    }

    delete root._btCarouselState;
    root.dataset.btCarouselInit = 'false';
  }

  /**
   * @param {HTMLElement} root
   * @param {object} options
   * @param {string} [options.track] - track selector
   * @param {string} [options.prev] - prev button selector
   * @param {string} [options.next] - next button selector
   * @param {string} [options.nav] - nav wrapper selector
   * @param {string} [options.item] - slide/item selector for step sizing
   * @param {number} [options.navMinWidth] - show arrow nav from this width (px)
   * @param {number} [options.autoplayDisableMinWidth] - disable autoplay from this width (px)
   * @param {number} [options.autoplayMs]
   * @param {number} [options.resumeMs]
   * @param {function} [options.onScroll] - called on scroll/resize
   */
  window.BT.initScrollCarousel = function (root, options) {
    if (!root) {
      return;
    }

    options = options || {};
    destroyScrollCarousel(root);

    var track = root.querySelector(options.track || '[data-carousel-track]');
    if (!track) {
      return;
    }

    var prevButton = options.prev ? root.querySelector(options.prev) : root.querySelector('[data-carousel-prev]');
    var nextButton = options.next ? root.querySelector(options.next) : root.querySelector('[data-carousel-next]');
    var nav = options.nav ? root.querySelector(options.nav) : root.querySelector('[data-carousel-nav]');
    var itemSelector = options.item || '[data-carousel-item], [data-carousel-slide]';
    var navMinWidth = typeof options.navMinWidth === 'number' ? options.navMinWidth : 750;
    var autoplayDisableMinWidth =
      typeof options.autoplayDisableMinWidth === 'number' ? options.autoplayDisableMinWidth : navMinWidth;
    var autoplayMs = options.autoplayMs || DEFAULT_AUTOPLAY_MS;
    var resumeMs = options.resumeMs || DEFAULT_RESUME_MS;
    var autoplayPaused = false;
    var inView = true;

    var state = {
      listeners: [],
      autoplayTimer: null,
      resumeTimer: null,
      inViewDisconnect: null,
      mediaQuery: null,
      onMediaChange: null
    };

    function trackListener(target, type, handler, opts) {
      target.addEventListener(type, handler, opts);
      state.listeners.push({ target: target, type: type, handler: handler, options: opts });
    }

    function scrollBehavior() {
      return prefersReducedMotion() ? 'auto' : 'smooth';
    }

    function scrollByStep(direction) {
      var step = getScrollStep(track, itemSelector) * direction;
      track.scrollBy({ left: step, behavior: scrollBehavior() });
    }

    function scrollNextWithLoop() {
      var maxScroll = track.scrollWidth - track.clientWidth;
      var atEnd = track.scrollLeft >= maxScroll - 2;

      if (atEnd) {
        track.scrollTo({ left: 0, behavior: scrollBehavior() });
        return;
      }

      scrollByStep(1);
    }

    function scrollPrevWithLoop() {
      var atStart = track.scrollLeft <= 2;
      var maxScroll = track.scrollWidth - track.clientWidth;

      if (atStart) {
        track.scrollTo({ left: maxScroll, behavior: scrollBehavior() });
        return;
      }

      scrollByStep(-1);
    }

    function stopAutoplay() {
      if (state.autoplayTimer) {
        clearInterval(state.autoplayTimer);
        state.autoplayTimer = null;
      }
    }

    function startAutoplay() {
      stopAutoplay();

      var overflow = track.scrollWidth > track.clientWidth + 2;
      if (
        !overflow ||
        !inView ||
        autoplayPaused ||
        prefersReducedMotion() ||
        document.hidden ||
        matchesMinWidth(autoplayDisableMinWidth)
      ) {
        return;
      }

      state.autoplayTimer = setInterval(function () {
        if (document.hidden) {
          return;
        }

        try {
          scrollNextWithLoop();
        } catch (error) {
          console.error('Carousel: autoplay tick failed.', error);
        }
      }, autoplayMs);
    }

    function pauseAutoplay() {
      autoplayPaused = true;
      stopAutoplay();

      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
        state.resumeTimer = null;
      }
    }

    function scheduleAutoplayResume() {
      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
      }

      state.resumeTimer = setTimeout(function () {
        try {
          autoplayPaused = false;
          startAutoplay();
        } catch (error) {
          console.error('Carousel: autoplay resume failed.', error);
        }
      }, resumeMs);
    }

    function updateNavState() {
      var overflow = track.scrollWidth > track.clientWidth + 2;

      if (prevButton) {
        prevButton.disabled = !overflow;
      }

      if (nextButton) {
        nextButton.disabled = !overflow;
      }
    }

    function syncNavVisibility() {
      var showNav = matchesMinWidth(navMinWidth);
      var overflow = track.scrollWidth > track.clientWidth + 2;

      if (nav) {
        nav.hidden = !showNav;
        nav.classList.toggle('is-visible', showNav && overflow);
      }

      updateNavState();
    }

    function onScroll() {
      updateNavState();

      if (typeof options.onScroll === 'function') {
        options.onScroll(track, root);
      }
    }

    if (prevButton) {
      trackListener(prevButton, 'click', function () {
        pauseAutoplay();
        scrollPrevWithLoop();
        scheduleAutoplayResume();
      });
    }

    if (nextButton) {
      trackListener(nextButton, 'click', function () {
        pauseAutoplay();
        scrollNextWithLoop();
        scheduleAutoplayResume();
      });
    }

    trackListener(track, 'scroll', onScroll, { passive: true });
    trackListener(window, 'resize', function () {
      syncNavVisibility();
      onScroll();
      startAutoplay();
    });

    trackListener(track, 'pointerdown', pauseAutoplay);
    trackListener(track, 'pointerenter', pauseAutoplay);
    trackListener(track, 'focusin', pauseAutoplay);
    trackListener(track, 'pointerup', scheduleAutoplayResume);
    trackListener(track, 'pointerleave', scheduleAutoplayResume);
    trackListener(track, 'focusout', scheduleAutoplayResume);

    bindCarouselWheelScroll(track);

    if (window.BT.bindCarouselInView) {
      state.inViewDisconnect = window.BT.bindCarouselInView(root, {
        onLeave: function () {
          inView = false;
          stopAutoplay();
        },
        onEnter: function () {
          inView = true;
          if (!autoplayPaused) {
            startAutoplay();
          }
        }
      });
    }

    if (nav) {
      try {
        state.mediaQuery = window.matchMedia('(min-width: ' + navMinWidth + 'px)');
        state.onMediaChange = function () {
          syncNavVisibility();
          startAutoplay();
        };

        if (typeof state.mediaQuery.addEventListener === 'function') {
          trackListener(state.mediaQuery, 'change', state.onMediaChange);
        } else if (typeof state.mediaQuery.addListener === 'function') {
          state.mediaQuery.addListener(state.onMediaChange);
        }
      } catch (error) {
        /* ignore */
      }
    }

    root._btCarouselState = state;
    root.dataset.btCarouselInit = 'true';
    syncNavVisibility();
    onScroll();
    startAutoplay();

    return {
      destroy: function () {
        destroyScrollCarousel(root);
      },
      scrollNext: scrollNextWithLoop,
      scrollPrev: scrollPrevWithLoop
    };
  };

  window.BT.destroyScrollCarousel = destroyScrollCarousel;

  /**
   * Crossfade hero slideshow with touch swipe.
   */
  window.BT.initCrossfadeSlider = function (root, options) {
    if (!root) {
      return;
    }

    options = options || {};
    destroyCrossfadeSlider(root);

    var slideSelector = options.slide || '[data-home-slide]';
    var slides = Array.prototype.slice.call(root.querySelectorAll(slideSelector));

    if (slides.length === 0) {
      return;
    }

    var autoplayEnabled = root.getAttribute('data-autoplay-enabled') !== 'false';
    var autoplayMs = parseInt(root.getAttribute('data-autoplay-ms'), 10);

    if (isNaN(autoplayMs) || autoplayMs < 3000) {
      autoplayMs = 7000;
    }

    var prevButton = root.querySelector(options.prev || '[data-home-prev]');
    var nextButton = root.querySelector(options.next || '[data-home-next]');
    var controls = root.querySelector(options.controls || '[data-home-controls]');
    var dots = Array.prototype.slice.call(root.querySelectorAll(options.dot || '[data-home-dot]'));
    var resumeMs = options.resumeMs || DEFAULT_RESUME_MS;
    var swipeThreshold = options.swipeThreshold || 48;
    var currentIndex = 0;
    var slidesLength = slides.length;
    var autoplayPaused = false;
    var pointerStartX = 0;
    var pointerStartY = 0;
    var pointerTracking = false;
    var swipePointerId = null;

    var state = {
      autoplayTimer: null,
      resumeTimer: null,
      listeners: []
    };

    function trackListener(target, type, handler, opts) {
      target.addEventListener(type, handler, opts);
      state.listeners.push({ target: target, type: type, handler: handler, options: opts });
    }

    slides.forEach(function (slide, index) {
      if (slide.classList.contains('is-active')) {
        currentIndex = index;
      }
    });

    function stopAutoplay() {
      if (state.autoplayTimer) {
        clearInterval(state.autoplayTimer);
        state.autoplayTimer = null;
      }
    }

    function startAutoplay() {
      stopAutoplay();

      if (!autoplayEnabled || slidesLength <= 1 || autoplayPaused || prefersReducedMotion() || document.hidden) {
        return;
      }

      state.autoplayTimer = setInterval(function () {
        if (document.hidden) {
          return;
        }

        try {
          setActiveSlide(currentIndex + 1, { fromAutoplay: true });
        } catch (error) {
          console.error('Crossfade slider: autoplay tick failed.', error);
        }
      }, autoplayMs);
    }

    function pauseAutoplay() {
      autoplayPaused = true;
      stopAutoplay();

      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
        state.resumeTimer = null;
      }
    }

    function scheduleAutoplayResume() {
      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
      }

      state.resumeTimer = setTimeout(function () {
        try {
          autoplayPaused = false;
          startAutoplay();
        } catch (error) {
          console.error('Crossfade slider: autoplay resume failed.', error);
        }
      }, resumeMs);
    }

    function setActiveSlide(index, opts) {
      var slideOpts = opts || {};
      var nextIndex = index;

      if (nextIndex < 0) {
        nextIndex = slidesLength - 1;
      }

      if (nextIndex >= slidesLength) {
        nextIndex = 0;
      }

      if (nextIndex === currentIndex && !slideOpts.force) {
        return;
      }

      if (!slideOpts.fromAutoplay) {
        pauseAutoplay();
        scheduleAutoplayResume();
      }

      slides.forEach(function (slide, slideIndex) {
        var isActive = slideIndex === nextIndex;
        slide.classList.toggle('is-active', isActive);
        slide.setAttribute('aria-hidden', isActive ? 'false' : 'true');
      });

      dots.forEach(function (dot, dotIndex) {
        var isActive = dotIndex === nextIndex;
        dot.classList.toggle('is-active', isActive);
        dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      currentIndex = nextIndex;
    }

    function bindControl(element, handler) {
      if (!element) {
        return;
      }

      trackListener(element, 'click', function (event) {
        event.preventDefault();
        handler();
      });
    }

    bindControl(prevButton, function () {
      setActiveSlide(currentIndex - 1, { force: true });
    });

    bindControl(nextButton, function () {
      setActiveSlide(currentIndex + 1, { force: true });
    });

    dots.forEach(function (dot) {
      trackListener(dot, 'click', function (event) {
        event.preventDefault();
        var index = parseInt(dot.getAttribute('data-slide-index'), 10);

        if (!isNaN(index)) {
          setActiveSlide(index, { force: true });
        }
      });
    });

    if (controls) {
      trackListener(controls, 'pointerdown', pauseAutoplay);
      trackListener(controls, 'pointerenter', pauseAutoplay);
      trackListener(controls, 'focusin', pauseAutoplay);
      trackListener(controls, 'pointerup', scheduleAutoplayResume);
      trackListener(controls, 'pointerleave', scheduleAutoplayResume);
      trackListener(controls, 'focusout', scheduleAutoplayResume);
    }

    function beginSwipeTracking(clientX, clientY, pointerId) {
      pointerStartX = clientX;
      pointerStartY = clientY;
      pointerTracking = true;
      swipePointerId = pointerId;
      pauseAutoplay();
    }

    function finishSwipeTracking(clientX, clientY) {
      if (!pointerTracking) {
        return;
      }

      pointerTracking = false;
      swipePointerId = null;

      var deltaX = clientX - pointerStartX;
      var deltaY = clientY - pointerStartY;

      if (Math.abs(deltaX) < swipeThreshold || Math.abs(deltaX) < Math.abs(deltaY) * 1.15) {
        scheduleAutoplayResume();
        return;
      }

      if (deltaX < 0) {
        setActiveSlide(currentIndex + 1, { force: true });
      } else {
        setActiveSlide(currentIndex - 1, { force: true });
      }

      scheduleAutoplayResume();
    }

    function cancelSwipeTracking() {
      if (!pointerTracking) {
        return;
      }

      pointerTracking = false;
      swipePointerId = null;
      scheduleAutoplayResume();
    }

    var swipeSurface = root.querySelector('[data-home-slides]') || root;

    trackListener(
      swipeSurface,
      'pointerdown',
      function (event) {
        if (event.pointerType === 'mouse' && event.button !== 0) {
          return;
        }

        if (event.target.closest('[data-home-controls], .home-slider__button, a')) {
          return;
        }

        beginSwipeTracking(event.clientX, event.clientY, event.pointerId);
      },
      { passive: true }
    );

    trackListener(
      swipeSurface,
      'pointerup',
      function (event) {
        if (!pointerTracking || event.pointerId !== swipePointerId) {
          return;
        }

        finishSwipeTracking(event.clientX, event.clientY);
      },
      { passive: true }
    );

    trackListener(
      swipeSurface,
      'pointercancel',
      function (event) {
        if (event.pointerId !== swipePointerId) {
          return;
        }

        cancelSwipeTracking();
      },
      { passive: true }
    );

    root.goToHomeSlide = function (index) {
      setActiveSlide(index, { force: true });
    };

    root.goToHomeSlideByBlockId = function (blockId) {
      pauseAutoplay();
      var targetIndex = slides.findIndex(function (slide) {
        return slide.getAttribute('data-block-id') === blockId;
      });

      if (targetIndex >= 0) {
        setActiveSlide(targetIndex, { force: true });
      }
    };

    root._btCrossfadeState = state;
    root.dataset.btCrossfadeInit = 'true';
    startAutoplay();
  };

  function destroyCrossfadeSlider(root) {
    if (!root || !root._btCrossfadeState) {
      return;
    }

    try {
      var state = root._btCrossfadeState;

      if (state.autoplayTimer) {
        clearInterval(state.autoplayTimer);
      }

      if (state.resumeTimer) {
        clearTimeout(state.resumeTimer);
      }

      state.listeners.forEach(function (entry) {
        entry.target.removeEventListener(entry.type, entry.handler, entry.options);
      });
    } catch (error) {
      console.error('Crossfade slider: teardown failed.', error);
    }

    delete root._btCrossfadeState;
    delete root.goToHomeSlide;
    delete root.goToHomeSlideByBlockId;
    root.dataset.btCrossfadeInit = 'false';
  }

  window.BT.destroyCrossfadeSlider = destroyCrossfadeSlider;

  /**
   * Run callback once carousel.js APIs are available (handles async section bundles).
   */
  window.BT.whenCarouselReady = function (callback) {
    if (typeof callback !== 'function') {
      return;
    }

    function run() {
      if (window.BT && window.BT.initCrossfadeSlider && window.BT.initScrollCarousel) {
        callback();
        return true;
      }

      return false;
    }

    if (run()) {
      return;
    }

    var attempts = 0;

    function retry() {
      attempts += 1;

      if (run()) {
        return;
      }

      if (attempts < 40) {
        window.setTimeout(retry, 50);
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', retry, { once: true });
    } else {
      retry();
    }
  };

  function initAllCrossfadeSliders(scope) {
    var context = scope || document;

    if (!window.BT.initCrossfadeSlider) {
      return;
    }

    context.querySelectorAll('[data-home-slider]').forEach(function (root) {
      window.BT.initCrossfadeSlider(root);
    });
  }

  function bootCrossfadeSliders() {
    initAllCrossfadeSliders(document);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootCrossfadeSliders);
  } else {
    bootCrossfadeSliders();
  }

  document.addEventListener('shopify:section:load', function (event) {
    if (event.target) {
      initAllCrossfadeSliders(event.target);
    }
  });

  document.addEventListener('shopify:section:unload', function (event) {
    if (!event.target) {
      return;
    }

    var slider = event.target.querySelector('[data-home-slider]');

    if (slider) {
      destroyCrossfadeSlider(slider);
    }
  });
})();
