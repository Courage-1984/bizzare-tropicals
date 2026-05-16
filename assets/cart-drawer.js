/**
 * AJAX cart drawer — Cart API + Sections Rendering API.
 */
(function () {
  'use strict';

  var drawerRoot = null;
  var config = null;
  var lastTrigger = null;
  var isOpen = false;
  var isBusy = false;

  function readConfig() {
    try {
      var script = document.querySelector('[data-cart-drawer-config]');
      if (!script) {
        return null;
      }
      return JSON.parse(script.textContent);
    } catch (error) {
      console.error('Cart drawer: invalid configuration.', error);
      return null;
    }
  }

  function getDrawerElements() {
    if (!drawerRoot) {
      drawerRoot = document.querySelector('[data-cart-drawer]');
    }
    if (!drawerRoot) {
      return null;
    }
    return {
      root: drawerRoot,
      overlay: drawerRoot.querySelector('[data-cart-drawer-overlay]'),
      panel: drawerRoot.querySelector('[data-cart-drawer-panel]'),
      body: drawerRoot.querySelector('[data-cart-drawer-body]'),
      closeButtons: drawerRoot.querySelectorAll('[data-cart-drawer-close]'),
    };
  }

  function setBusy(busy) {
    isBusy = busy;
    var elements = getDrawerElements();
    if (elements && elements.root) {
      elements.root.classList.toggle('cart-drawer--busy', busy);
      elements.root.setAttribute('aria-busy', busy ? 'true' : 'false');
    }
  }

  function updateHeaderCount(itemCount) {
    try {
      var cartTriggers = document.querySelectorAll('[data-cart-drawer-open]');
      cartTriggers.forEach(function (trigger) {
        var count = typeof itemCount === 'number' ? itemCount : 0;
        var labelKey = count > 0 ? 'cartWithCount' : 'cart';
        var templateWithCount = trigger.dataset.labelCartWithCount;
        var templateCart = trigger.dataset.labelCart;

        if (count > 0 && templateWithCount) {
          trigger.setAttribute('aria-label', templateWithCount.replace('__COUNT__', String(count)));
        } else if (templateCart) {
          trigger.setAttribute('aria-label', templateCart);
        }

        var badge = trigger.querySelector('[data-header-cart-count]');
        if (count > 0) {
          if (!badge) {
            badge = document.createElement('span');
            badge.className = 'site-header__cart-count';
            badge.setAttribute('data-header-cart-count', '');
            badge.setAttribute('aria-hidden', 'true');
            trigger.appendChild(badge);
          }
          badge.textContent = String(count);
          badge.hidden = false;
        } else if (badge) {
          badge.remove();
        }
      });
    } catch (error) {
      console.error('Cart drawer: failed to update header count.', error);
    }
  }

  function fetchCartJson() {
    var root = config && config.rootUrl ? config.rootUrl : '/';
    return fetch(root + 'cart.js', {
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    }).then(function (response) {
      if (!response.ok) {
        throw new Error('Cart drawer: cart.js request failed.');
      }
      return response.json();
    });
  }

  function fetchSectionHtml() {
    var sectionId = config.sectionId;
    var sectionHandle = config.sectionHandle || 'cart-drawer';
    var root = config.rootUrl || '/';
    var url = root + '?sections=' + encodeURIComponent(sectionId);

    return fetch(url, {
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Cart drawer: section render failed.');
        }
        return response.json();
      })
      .then(function (sections) {
        var html = sections[sectionId] || sections[sectionHandle] || '';
        if (html) {
          return html;
        }
        return fetch(root + 'cart?sections=' + encodeURIComponent(sectionId), {
          credentials: 'same-origin',
          headers: { Accept: 'application/json' },
        })
          .then(function (cartResponse) {
            if (!cartResponse.ok) {
              return '';
            }
            return cartResponse.json();
          })
          .then(function (cartSections) {
            return cartSections[sectionId] || cartSections[sectionHandle] || '';
          });
      });
  }

  function replaceDrawerContents(sectionHtml) {
    var elements = getDrawerElements();
    if (!elements || !elements.body || !sectionHtml) {
      return;
    }

    var doc = new DOMParser().parseFromString(sectionHtml, 'text/html');
    var sourceBody = doc.querySelector('[data-cart-drawer-body]');
    if (!sourceBody) {
      return;
    }

    elements.body.innerHTML = sourceBody.innerHTML;
  }

  function refreshDrawer() {
    setBusy(true);
    return Promise.all([fetchCartJson(), fetchSectionHtml()])
      .then(function (results) {
        var cart = results[0];
        var sectionHtml = results[1];
        replaceDrawerContents(sectionHtml);
        updateHeaderCount(cart.item_count);
        return cart;
      })
      .catch(function (error) {
        console.error('Cart drawer: refresh failed.', error);
        throw error;
      })
      .finally(function () {
        setBusy(false);
      });
  }

  function openDrawer(trigger) {
    var elements = getDrawerElements();
    if (!elements || !elements.root || isOpen) {
      return;
    }

    lastTrigger = trigger || lastTrigger || document.activeElement;
    isOpen = true;

    elements.root.classList.add('is-open');
    elements.root.setAttribute('aria-hidden', 'false');

    if (elements.overlay) {
      elements.overlay.hidden = false;
      elements.overlay.setAttribute('aria-hidden', 'false');
    }

    if (elements.panel) {
      elements.panel.setAttribute('aria-hidden', 'false');
    }

    document.documentElement.classList.add('is-scroll-locked');

    var closeBtn = elements.root.querySelector('[data-cart-drawer-close]');
    if (closeBtn) {
      closeBtn.focus();
    }
  }

  function closeDrawer() {
    var elements = getDrawerElements();
    if (!elements || !elements.root || !isOpen) {
      return;
    }

    isOpen = false;

    elements.root.classList.remove('is-open');
    elements.root.setAttribute('aria-hidden', 'true');

    if (elements.overlay) {
      elements.overlay.hidden = true;
      elements.overlay.setAttribute('aria-hidden', 'true');
    }

    if (elements.panel) {
      elements.panel.setAttribute('aria-hidden', 'true');
    }

    document.documentElement.classList.remove('is-scroll-locked');

    if (lastTrigger && typeof lastTrigger.focus === 'function') {
      lastTrigger.focus();
    }
    lastTrigger = null;
  }

  function addFromForm(form) {
    setBusy(true);
    var formData = new FormData(form);

    return fetch(config.cartAddUrl, {
      method: 'POST',
      credentials: 'same-origin',
      body: formData,
    })
      .then(function (response) {
        return response.json().then(function (data) {
          if (!response.ok) {
            var message = data && data.description ? data.description : 'Add to cart failed.';
            throw new Error(message);
          }
          return data;
        });
      })
      .then(function () {
        return refreshDrawer();
      })
      .then(function () {
        openDrawer(form.querySelector('[data-add-to-cart]'));
      })
      .catch(function (error) {
        console.error('Cart drawer: add to cart failed.', error);
        setBusy(false);
        throw error;
      });
  }

  function changeLineQuantity(lineKey, quantity) {
    setBusy(true);

    return fetch(config.cartChangeUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: lineKey,
        quantity: quantity,
      }),
    })
      .then(function (response) {
        return response.json().then(function (data) {
          if (!response.ok) {
            var message = data && data.description ? data.description : 'Cart update failed.';
            throw new Error(message);
          }
          return data;
        });
      })
      .then(function () {
        return refreshDrawer();
      })
      .catch(function (error) {
        console.error('Cart drawer: quantity update failed.', error);
        setBusy(false);
        throw error;
      });
  }

  function handleQtyClick(event) {
    var button = event.target.closest('[data-cart-qty-minus], [data-cart-qty-plus]');
    if (!button) {
      return;
    }

    var qtyRoot = button.closest('[data-cart-qty]');
    if (!qtyRoot) {
      return;
    }

    var lineKey = qtyRoot.getAttribute('data-line-key');
    var input = qtyRoot.querySelector('[data-cart-qty-input]');
    if (!lineKey || !input) {
      return;
    }

    var current = parseInt(input.getAttribute('data-quantity'), 10) || 0;
    var next = current;

    if (button.hasAttribute('data-cart-qty-plus')) {
      next = current + 1;
    } else {
      next = Math.max(0, current - 1);
    }

    event.preventDefault();
    if (isBusy) {
      return;
    }

    changeLineQuantity(lineKey, next);
  }

  function bindDocumentEvents() {
    document.addEventListener('click', function (event) {
      var openTrigger = event.target.closest('[data-cart-drawer-open]');
      if (openTrigger) {
        event.preventDefault();

        if (isOpen) {
          closeDrawer();
          return;
        }

        lastTrigger = openTrigger;
        refreshDrawer()
          .then(function () {
            openDrawer(openTrigger);
          })
          .catch(function () {
            window.location.href = config.cartUrl;
          });
        return;
      }

      if (event.target.closest('[data-cart-drawer-close]')) {
        event.preventDefault();
        closeDrawer();
        return;
      }

      if (event.target.closest('[data-cart-drawer-overlay]')) {
        event.preventDefault();
        closeDrawer();
        return;
      }

      handleQtyClick(event);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen) {
        event.preventDefault();
        closeDrawer();
      }
    });

    document.addEventListener('submit', function (event) {
      var form = event.target;
      if (!form || form.tagName !== 'FORM') {
        return;
      }

      var productRoot = form.closest('[data-main-product]');
      if (!productRoot) {
        return;
      }

      var submitter = event.submitter;
      if (submitter && submitter.name !== 'add' && !submitter.hasAttribute('data-add-to-cart')) {
        return;
      }

      event.preventDefault();
      if (isBusy) {
        return;
      }

      addFromForm(form);
    });
  }

  function init() {
    drawerRoot = document.querySelector('[data-cart-drawer]');
    config = readConfig();

    if (!drawerRoot || !config) {
      return;
    }

    bindDocumentEvents();
    fetchCartJson()
      .then(function (cart) {
        updateHeaderCount(cart.item_count);
      })
      .catch(function () {
        /* Non-blocking */
      });
  }

  window.CartDrawer = {
    open: function (trigger) {
      refreshDrawer().then(function () {
        openDrawer(trigger);
      });
    },
    close: closeDrawer,
    refresh: refreshDrawer,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', function (event) {
    if (event.target && event.target.querySelector('[data-cart-drawer]')) {
      drawerRoot = null;
      init();
    }
  });
})();
