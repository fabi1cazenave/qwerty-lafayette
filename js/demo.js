window.addEventListener('DOMContentLoaded', () => {
  'use strict'; // eslint-disable-line

  const dialog   = document.querySelector('dialog');
  const keyboard = document.querySelector('dialog x-keyboard');
  const input    = document.querySelector('dialog input');
  const geometry = document.querySelector('dialog select');
  const button   = document.querySelector('button');

  if (!keyboard.layout) {
    console.warn('web components are not supported');
    return; // the web component has not been loaded
  }

  fetch(keyboard.getAttribute('src'))
    .then(response => response.json())
    .then(data => {
      const shape = 'iso'; // data.geometry.replace('ergo', 'ol60').toLowerCase();
      keyboard.setKeyboardLayout(data.keymap, data.deadkeys, shape);
      geometry.value = shape;
      button.hidden = false;
      if (!window.location.hash) {
        button.focus();
      }
    });

  geometry.onchange = (event) => {
    keyboard.geometry = event.target.value;
  };

  /**
   * Open/Close modal
   */
  button.onclick = () => {
    dialog.showModal();
    input.value = '';
    input.focus();
  }
  input.onblur = () => {
    keyboard.clearStyle()
    dialog.close();
  }

  /**
   * Keyboard highlighting & layout emulation
   */

  // required to work around a Chrome bug, see the `keyup` listener below
  const pressedKeys = {};

  // highlight keyboard keys and emulate the selected layout
  input.onkeydown = (event) => {
    pressedKeys[event.code] = true;
    const value = keyboard.keyDown(event);
    if (value) {
      event.target.value += value;
    } else if (event.code === 'Enter') { // clear text input on <Enter>
      event.target.value = '';
    } else if ((event.code === 'Tab') || (event.code === 'Escape')) {
      setTimeout(close, 100);
    } else {
      return true; // don't intercept special keys or key shortcuts
    }
    return false; // event has been consumed, stop propagation
  };
  input.addEventListener('keyup', (event) => {
    if (pressedKeys[event.code]) { // expected behavior
      keyboard.keyUp(event);
      delete pressedKeys[event.code];
    } else {
      /**
       * We got a `keyup` event for a key that did not trigger any `keydown`
       * event first: this is a known bug with "real" dead keys on Chrome.
       * As a workaround, emulate a keydown + keyup. This introduces some lag,
       * which can result in a typo (especially when the "real" dead key is used
       * for an emulated dead key) -- but there's not much else we can do.
       */
      event.target.value += keyboard.keyDown(event);
      setTimeout(() => keyboard.keyUp(event), 100);
    }
  });

  /**
   * When pressing a "real" dead key + key sequence, Firefox and Chrome will
   * add the composed character directly to the text input (and nicely trigger
   * an `insertCompositionText` or `insertText` input event, respectively).
   * Not sure wether this is a bug or not -- but this is not the behavior we
   * want for a keyboard layout emulation. The code below works around that.
   */
  input.addEventListener('input', (event) => {
    if (event.inputType === 'insertCompositionText'
      || event.inputType === 'insertText') {
      event.target.value = event.target.value.slice(0, -event.data.length);
    }
  });
});
