window.addEventListener('DOMContentLoaded', () => {
  'use strict'; // eslint-disable-line

  const keyboard = document.querySelector('x-keyboard');
  const button   = document.querySelector('button');
  const input    = document.querySelector('input');
  const geometry = document.querySelector('#demo select');
  const demo     = document.querySelector('#demo');

  if (!keyboard.layout) {
    console.warn('web components are not supported');
    return; // the web component has not been loaded
  }

  fetch(`layouts/qwerty.json`)
    .then(response => response.json())
    .then(data => {
      const shape = data.geometry.replace('ERGO', 'OL60').toLowerCase();
      keyboard.setKeyboardLayout(data.layout, data.dead_keys, shape);
      geometry.value = shape;
      button.hidden = false;
      button.focus();
    });

  geometry.onchange = (event) => {
    keyboard.geometry = event.target.value;
  };

  /**
   * Open/Close modal
   */
  function open() {
    demo.hidden = false;
    input.value = '';
    input.focus();
  }
  function close() {
    keyboard.clearStyle()
    demo.hidden = true;
  }
  button.onclick = open;
  demo.onclick = (event) => {
    if (event.target.id === 'demo') {
      close();
    }
  };

  /**
   * Keyboard highlighting & layout emulation
   */
  input.onkeyup = event => keyboard.keyUp(event.code);
  input.onkeydown = (event) => {
    const value = keyboard.keyDown(event.code);
    if (value && !(event.ctrlKey || event.altKey || event.metaKey)) {
      event.target.value += value;
    } else if (event.code === 'Enter') {
      event.target.value = '';
    } else if (event.code === 'Escape' || event.code === 'Tab') {
      setTimeout(close, 100);
    } else {
      return true; // don't intercept special keys or key shortcuts
    }
    return false; // event has been consumed, stop propagation
  };

  /**
   * When pressing a "real" dead key + key sequence:
   *  - Chromium does not raise any event until the key sequence is complete
   *    => "real" dead keys are unusable for this emulation, unfortunately;
   *  - Firefox triggers two `keydown` events (as expected),
   *    but also adds the composed character directly to the text input
   *    (and nicely triggers an `insertCompositionText` input event)
   *    => the code below works around that.
   */
  input.oninput = (event) => {
    if (event.data && event.inputType === 'insertCompositionText') {
      event.target.value = event.target.value.slice(0, -event.data.length);
    }
  };
});
