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

  // display a percentage value
  const setPercent = (elt, num, precision) => {
    const x = 10 ** precision;
    elt.innerText = `${Math.round(x * num) / x}%`;
  };
  const showPercent = (sel, num, precision) => {
    setPercent(document.querySelector(sel), num, precision);
  };

  // display a finger/frequency table and bar graph
  const showFingerData = (div, values, maxValue, precision) => {
    const canvas = document.createElement('canvas');
    const table = document.createElement('table');
    const tr = document.createElement('tr');
    tr.appendChild(document.createElement('td'));

    canvas.width = 1000;
    canvas.height = 100;
    const ctx = canvas.getContext('2d');
    ctx.save();
    ctx.fillStyle = '#88f';
    const width = canvas.width / 11;
    const margin = 20;
    const scale = 100 / maxValue;

    // for (const [f, load] of Object.entries(fingerLoad)) {
    Object.values(values).forEach((value, i) => {
      if (i == 4) {
        tr.appendChild(document.createElement('td'));
      }
      const idx = i >= 4 ? i + 2 : i + 1;
      const td = document.createElement('td');
      setPercent(td, value, precision);
      tr.appendChild(td);
      ctx.fillRect(idx * width + margin / 2, canvas.height - value * scale,
        width - margin / 2, value * scale);
    });
    ctx.restore();

    tr.appendChild(document.createElement('td'));
    table.appendChild(tr);
    div.innerHTML = '';
    div.appendChild(canvas);
    div.appendChild(table);
  };

  // compute the same-finger and same-key usages
  const sfu = () => {
    const skuCount = {}; // same-key usage
    const sfuCount = {}; // same-finger usage
    const sfuDigrams = [];
    const fingers = ['l5', 'l4', 'l3', 'l2', 'r2', 'r3', 'r4', 'r5'];
    fingers.forEach((finger) => {
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
            // sfuCount[finger] += frequency;
          }
          else if (keyFinger[acc] === finger) {
            console.log(digram, frequency);
            sfuDigrams.push({digram, frequency});
            sfuCount[finger] += frequency;
          }
        }
        return key.id;
      }, '');
    });

    // note: in Ergol, ï and î are same-finger digrams
    // even though they are single characters => count symbols, too?
    const sum = (acc, freq) => acc + freq;
    showPercent('#sfu-all', Object.values(sfuCount).reduce(sum, 0), 2);
    showPercent('#sku-all', Object.values(skuCount).reduce(sum, 0), 2);

    // display metrics
    showFingerData(document.querySelector('#sfu'), sfuCount, 2.0, 2);
    showFingerData(document.querySelector('#sku'), skuCount, 2.0, 2);
    console.log(sfuDigrams);
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
    Object.entries(fingerCount).forEach(([f, count]) => {
      fingerLoad[f] = (100 * count) / keystrokes;
    });
    const sum = (acc, id) => fingerLoad[id] + acc;
    showPercent('#load-left', ['l2', 'l3', 'l4', 'l5'].reduce(sum, 0), 1);
    showPercent('#load-right', ['r2', 'r3', 'r4', 'r5'].reduce(sum, 0), 1);

    // display metrics
    showFingerData(document.querySelector('#load'), fingerLoad, 25.0, 1);
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
