/**
 * AdBlockPlus is likely to hide a few keys *sigh*
 * => ensure that all keys are properly displayed.
 */

if (window.addEventListener) window.addEventListener('load', function() {
  var badRendering = document.getElementById('badRendering');
  if (!badRendering)
    return;

  // All browsers supporting .addEventListener are reported to support
  // .querySelectorAll and the ^= selector (IE9, Firefox 3+, Safari...)
  var keys = document.querySelectorAll('[id^="key_A"]');
  for (var i = 0; i < keys.length; i++) {
    if (parseInt(keys[i].getBoundingClientRect().width, 10) < 40) {
      badRendering.style.display = 'block';
      break;
    }
  }
}, false);

