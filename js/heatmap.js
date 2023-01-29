window.addEventListener('DOMContentLoaded', () => {
  'use strict'; // eslint-disable-line

  const keyboard = document.querySelector('x-keyboard');

  let keyChars = {};
  let corpus = {};
  let digrams = {};
  let corpusName = '';

  // create an efficient hash table to parse a text
  const supportedChars = (keymap, deadkeys) => {
    const charTable = {};
    const deadTable = {};

    // main chars, directly accessible (or with Shift / AltGr)
    Object.entries(keymap).forEach(([key, values]) => {
      values.forEach((char) => {
        if (!(char in charTable)) {
          if (char.length === 1) {
            charTable[char] = [key];
          } else if (!(char in deadTable)) {
            deadTable[char] = key;
          }
        }
      });
    });

    // additional chars, requiring dead keys
    Object.entries(deadkeys).forEach(([key, dict]) => {
      Object.entries(dict).forEach(([orig, char]) => {
        if (!(char in charTable) && charTable[orig]) {
          charTable[char] = [deadTable[key]].concat(charTable[orig]);
        }
      });
    });

    return charTable;
  };

  const sfu = () => {
    const sfuCount = {}; // same-finger usage
    const skuCount = {}; // same-key usage
    ['l5', 'l4', 'l3', 'l2', 'r2', 'r3', 'r4', 'r5'].forEach((finger) => {
      sfuCount[finger] = 0;
      skuCount[finger] = 0;
    });

    const keyFinger = {};
    Object.entries(keyboard.fingerAssignments).forEach(([f, keys]) => {
      keys.forEach((keyName) => { keyFinger[keyName] = f; });
    });

    Object.entries(digrams).forEach(([digram, frequency]) => {
      keyboard.layout.getKeySequence(digram).reduce((acc, key) => {
        const finger = keyFinger[key.id];
        if (finger) { // in case there's no key for the current character...
          if (acc === key.id) {
            skuCount[finger] += frequency;
          }
          else if (keyFinger[acc] === finger) {
            console.log(digram, frequency);
            sfuCount[finger] += frequency;
          }
        }
        return key.id;
      }, '');
    });

    // note: in Ergol, ï and î are same-finger digrams
    // even though they are single characters => count symbols, too?
    console.log(sfuCount);
    console.log(skuCount);
    console.log(Object.values(sfuCount).reduce((acc, freq) => acc + freq));
  };

  // compute the heatmap for a text on a given layout
  const heatmap = () => {
    const keyCount = {};
    Object.values(keyChars).forEach((keys) => {
      keys.forEach((key) => {
        keyCount[key] = 0;
      });
    });

    // count the key strokes in the corpus
    const unsupportedChars = {};
    Object.entries(corpus).forEach(([char, count]) => {
      const keys = keyChars[char];
      if (keys) {
        keys.forEach((key) => { keyCount[key] += count; });
      } else {
        unsupportedChars[char] = true;
      }
    });

    // console.log(Object.keys(unsupportedChars).sort());
    // console.log(keyCount);

    // display the heatmap
    const colormap = {};
    const contrast = 5;
    const total = Object.values(corpus).reduce((acc, n) => n + acc);
    Object.entries(keyCount).forEach(([key, count]) => {
      if (key !== 'Space') {
        const lvl = 255 - Math.floor((255 * contrast * count) / total);
        colormap[key] = `rgb(${lvl}, ${lvl}, 255)`; // blue scale
      }
    });
    keyboard.setCustomColors(colormap);

    // give some metrics
    const fingerCount = {};
    const fingerLoad = {};
    let keystrokes = 0;
    Object.entries(keyboard.fingerAssignments).forEach(([f, keys]) => {
      fingerCount[f] = keys.filter((id) => id in keyCount)
        .reduce((acc, id) => acc + keyCount[id], 0);
      keystrokes += fingerCount[f];
    });
    const percent = (num) => `${Math.round(10 * num) / 10}%`;
    Object.entries(fingerCount).forEach(([f, count]) => {
      fingerLoad[f] = (100 * count) / keystrokes;
      document.getElementById(f).innerText = percent(fingerLoad[f]);
    });
    const totalLoad = (acc, id) => fingerLoad[id] + acc;
    const left = ['l2', 'l3', 'l4', 'l5'].reduce(totalLoad, 0);
    const right = ['r2', 'r3', 'r4', 'r5'].reduce(totalLoad, 0);
    document.getElementById('left').innerText = percent(left);
    document.getElementById('right').innerText = percent(right);

    // display metrics
    const canvas = document.querySelector('#load canvas');
    canvas.width = 1000;
    canvas.height = 100;
    const ctx = canvas.getContext('2d');
    ctx.save();
    ctx.fillStyle = '#88f';
    const width = canvas.width / 11;
    const margin = 20;
    // for (const [f, load] of Object.entries(fingerLoad)) {
    Object.values(fingerLoad).forEach((load, i) => {
      const idx = i >= 4 ? i + 2 : i + 1;
      ctx.fillRect(idx * width + margin / 2, canvas.height - load * 4,
        width - margin / 2, load * 4);
    });
    ctx.restore();
  };

  // keyboard state: these <select> element IDs match the x-keyboard properties
  // -- but the `layout` property requires a JSON fetch
  const IDs = [ 'layout', 'geometry', 'corpus' ];
  const setProp = (key, value) => {
    if (key === 'layout') {
      if (value) {
        fetch(`layouts.heatmap/${value}.json`)
          .then((response) => response.json())
          .then((data) => {
            keyboard.setKeyboardLayout(data.keymap, data.deadkeys,
              data.geometry.replace('ergo', 'iso'));
            data.keymap.Enter = [ '\r', '\n' ];
            keyChars = supportedChars(data.keymap, data.deadkeys);
            if (Object.keys(corpus).length > 0) {
              heatmap();
              sfu();
            }
          });
      } else {
        keyboard.setKeyboardLayout();
        keyChars = {};
        // input.placeholder = 'select a keyboard layout';
      }
    } else if (key === 'corpus') {
      if (value && value !== corpusName) {
        fetch(`corpus/${value}.json`)
          .then((response) => response.json())
          .then((data) => {
            corpus = data.symbols;
            digrams = data.digrams;
            if (Object.keys(keyChars).length > 0) {
              heatmap();
              sfu();
            }
          });
        corpusName = value;
      }
    } else {
      keyboard[key] = value;
    }
    document.getElementById(key).value = value;
  };

  // store the keyboard state in the URL hash like it's 1995 again! :-)
  const state = {};
  const updateHashState = (key, value) => {
    state[key] = value;
    window.location.hash = IDs
      .reduce((hash, prop) => `${hash}/${state[prop]}`, '')
      .replace(/\/+$/, '');
  };
  const applyHashState = () => {
    const hashState = window.location.hash.split('/').slice(1);
    IDs.forEach((key, i) => {
      setProp(key, hashState[i] || '');
      state[key] = hashState[i] || '';
    });
  };
  IDs.forEach((key) => {
    document.getElementById(key).addEventListener('change',
      (event) => updateHashState(key, event.target.value));
  });
  window.addEventListener('hashchange', applyHashState);
  applyHashState();
});
