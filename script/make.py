#!/usr/bin/env python3

import os
import re
import sys
import unicodedata
import yaml


def add_spaces_before_combining_chars(text):
    out = ''
    for char in text:
        if unicodedata.combining(char):
            out = out + ' ' + char
        else:
            out = out + char
    return out


def remove_spaces_before_combining_chars(text):
    out = list('')
    for char in text:
        if unicodedata.combining(char):
            out[-1] = char
        else:
            out.append(char)
    return ''.join(out)


def lines_to_text(lines, indent=''):
    out = ''
    for line in lines:
        if len(line):
            out = out + indent + add_spaces_before_combining_chars(line)
        out = out + '\n'
    return out[:-1]


def substitute_lines(template, variable, lines):
    prefix = 'LAFAYETTE::'
    exp = re.compile('.*' + prefix + variable + '.*')

    indent = ''
    for line in template.split('\n'):
        m = exp.match(line)
        if m:
            indent = m.group().split(prefix)[0]
            break

    return exp.sub(lines_to_text(lines, indent), template)


def substitute_token(template, token, value):
    exp = re.compile('\$\{' + token + '(=[^\}]*){0,1}\}')
    return exp.sub(value, template)


def upper_key(letter):
    customAlpha = {
        '\u00df': '\u1e9e',  # ß ẞ
        '\u007c': '\u00a6',  # | ¦
        '\u003c': '\u2264',  # < ≤
        '\u003e': '\u2265',  # > ≥
        '\u2020': '\u2021',  # † ‡
        '\u2190': '\u21d0',  # ← ⇐
        '\u2191': '\u21d1',  # ↑ ⇑
        '\u2192': '\u21d2',  # → ⇒
        '\u2193': '\u21d3',  # ↓ ⇓
    }
    if letter in customAlpha:
        return customAlpha[letter]
    elif letter.upper() != letter.lower():
        return letter.upper()
    else:
        return ' '


def hex_ord(char):
    return hex(ord(char))[2:].zfill(4)


def openLocalFile(fileName):
    return open(sys.path[0] + '/' + fileName)


GEOMETRY = yaml.load(openLocalFile('geometry.yaml'))
SYMBOLS = yaml.load(openLocalFile('symbols.yaml'))

DEAD_KEYS = {                                           # combining diacritics
    '\u20e1': {'klc': '¤', 'xkb': 'ISO_Level3_Latch'},  # | ⃡|
    '\u0300': {'klc': '`', 'xkb': 'dead_grave'},        # | ̀|
    '\u0301': {'klc': '´', 'xkb': 'dead_acute'},        # | ́|
    '\u0302': {'klc': '^', 'xkb': 'dead_circumflex'},   # | ̂|
    '\u0303': {'klc': '~', 'xkb': 'dead_tilde'},        # | ̃|
    '\u0307': {'klc': '˙', 'xkb': 'dead_abovedot'},     # | ̇|
    '\u0308': {'klc': '¨', 'xkb': 'dead_diaeresis'},    # | ̈|
    '\u030a': {'klc': '˚', 'xkb': 'dead_abovering'},    # | ̊|
    '\u0326': {'klc': ',', 'xkb': 'dead_commabelow'},   # | ̦|
    '\u0327': {'klc': '¸', 'xkb': 'dead_cedilla'},      # | ̧|
    '\u0328': {'klc': '˛', 'xkb': 'dead_ogonek'},       # | ̨|
}

LAYER_KEYS = [
    '- Digits',
    'ae01', 'ae02', 'ae03', 'ae04', 'ae05',
    'ae06', 'ae07', 'ae08', 'ae09', 'ae10',

    '- Letters, first row',
    'ad01', 'ad02', 'ad03', 'ad04', 'ad05',
    'ad06', 'ad07', 'ad08', 'ad09', 'ad10',

    '- Letters, second row',
    'ac01', 'ac02', 'ac03', 'ac04', 'ac05',
    'ac06', 'ac07', 'ac08', 'ac09', 'ac10',

    '- Letters, third row',
    'ab01', 'ab02', 'ab03', 'ab04', 'ab05',
    'ab06', 'ab07', 'ab08', 'ab09', 'ab10',

    '- Pinky keys',
    'tlde', 'ae11', 'ae12', 'ad11', 'ad12', 'ac11', 'bksl', 'lsgt'
]


class Layout:
    """ Lafayette-style keyboard layout: base + dead key + altgr layers. """

    def __init__(self, filePath):
        """ Import a keyboard layout to instanciate the object. """

        self.layers = [{}, {}, {}, {}, {}, {}]
        cfg = yaml.load(open(filePath))
        rows = GEOMETRY[cfg['geometry']]['rows']
        base = remove_spaces_before_combining_chars(cfg['base']).split('\n')
        altgr = remove_spaces_before_combining_chars(cfg['altgr']).split('\n')
        self._parse_template(base, rows, 0)
        self._parse_template(base, rows, 2)
        self._parse_template(altgr, rows, 4)

    def _parse_template(self, template, rows, layerNumber):
        """ Extract a keyboard layer from a template. """

        if layerNumber == 0:  # base layer
            colOffset = 0
        else:  # AltGr or dead key (lafayette)
            colOffset = 2

        j = 0
        for row in rows:
            i = row['offset'] + colOffset
            keys = row['keys']

            base = list(template[2 + j * 3])
            shift = list(template[1 + j * 3])

            for key in keys:
                baseKey = base[i]
                shiftKey = shift[i]

                if layerNumber == 0 and baseKey == ' ':  # 'shift' prevails
                    baseKey = shiftKey.lower()
                if layerNumber != 0 and shiftKey == ' ':
                    shiftKey = upper_key(baseKey)

                if (baseKey != ' '):
                    self.layers[layerNumber + 0][key] = baseKey
                if (shiftKey != ' '):
                    self.layers[layerNumber + 1][key] = shiftKey

                i = i + 6

            j = j + 1

    def _fill_template(self, template, rows, layerNumber):
        """ Fill a template with a keyboard layer. """

        if layerNumber == 0:  # base layer
            colOffset = 0
            shiftPrevails = True
        else:  # AltGr or dead key (lafayette)
            colOffset = 2
            shiftPrevails = False

        j = 0
        for row in rows:
            i = row['offset'] + colOffset
            keys = row['keys']

            base = list(template[2 + j * 3])
            shift = list(template[1 + j * 3])

            for key in keys:
                baseKey = ' '
                if key in self.layers[layerNumber]:
                    baseKey = self.layers[layerNumber][key]

                shiftKey = ' '
                if key in self.layers[layerNumber + 1]:
                    shiftKey = self.layers[layerNumber + 1][key]

                if shiftPrevails:
                    shift[i] = shiftKey
                    if upper_key(baseKey) != shiftKey:
                        base[i] = baseKey
                else:
                    base[i] = baseKey
                    if upper_key(baseKey) != shiftKey:
                        shift[i] = shiftKey

                i = i + 6

            template[2 + j * 3] = ''.join(base)
            template[1 + j * 3] = ''.join(shift)
            j = j + 1

        return template

    def get_geometry(self, layers=[0], name='ISO'):
        """ `geometry` view of the requested layers. """

        rows = GEOMETRY[name]['rows']
        template = GEOMETRY[name]['template'].split('\n')[:-1]
        for i in layers:
            template = self._fill_template(template, rows, i)
        return template

    @property
    def xkb(self):
        """ Linux layout. """

        showDescription = True
        supportedSymbols = SYMBOLS['xkb']
        maxLength = 16  # `ISO_Level3_Latch` should be the longest symbol name

        output = []
        for keyName in LAYER_KEYS:
            if keyName == '':
                continue

            if keyName.startswith('-'):  # separator
                if len(output):
                    output.append('')
                output.append('//' + keyName[1:])
                continue

            symbols = []
            description = ' //'
            for layer in self.layers:
                if keyName in layer:
                    symbol = layer[keyName]
                    desc = symbol
                    if symbol in DEAD_KEYS:
                        desc = DEAD_KEYS[symbol]['klc']
                        symbol = DEAD_KEYS[symbol]['xkb']
                    elif symbol in supportedSymbols \
                            and len(supportedSymbols[symbol]) <= maxLength:
                        symbol = supportedSymbols[symbol]
                    else:
                        symbol = 'U' + hex_ord(symbol).upper()
                    symbols.append(symbol)
                else:
                    desc = ' '
                    symbols.append('VoidSymbol')
                description = description + ' ' + desc

            line = 'key <' + keyName.upper() + '> ' + '{[ ' + \
                symbols[0].ljust(maxLength) + ', ' +   \
                symbols[1].ljust(maxLength) + ', ' +   \
                symbols[2].ljust(maxLength) + ', ' +   \
                symbols[3].ljust(maxLength) + '],[ ' + \
                symbols[4].ljust(maxLength) + ', ' +   \
                symbols[5].ljust(maxLength) + ']};'
            if showDescription:
                line = line + description
            output.append(line)

        return output

    @property
    def klc(self):
        """ Windows layout, main part. """

        klcKeys = {
            'ae01': '02	1	0	',
            'ae02': '03	2	0	',
            'ae03': '04	3	0	',
            'ae04': '05	4	0	',
            'ae05': '06	5	0	',
            'ae06': '07	6	0	',
            'ae07': '08	7	0	',
            'ae08': '09	8	0	',
            'ae09': '0a	9	0	',
            'ae10': '0b	0	0	',

            # letters, first row
            'ad01': '10	Q	1	',
            'ad02': '11	W	1	',
            'ad03': '12	E	1	',
            'ad04': '13	R	1	',
            'ad05': '14	T	1	',
            'ad06': '15	Y	1	',
            'ad07': '16	U	1	',
            'ad08': '17	I	1	',
            'ad09': '18	O	1	',
            'ad10': '19	P	1	',

            # letters, second row
            'ac01': '1e	A	1	',
            'ac02': '1f	S	1	',
            'ac03': '20	D	1	',
            'ac04': '21	F	1	',
            'ac05': '22	G	1	',
            'ac06': '23	H	1	',
            'ac07': '24	J	1	',
            'ac08': '25	K	1	',
            'ac09': '26	L	1	',
            'ac10': '27	OEM_1	0	',

            # letters, third row
            'ab01': '2c	Z	1	',
            'ab02': '2d	X	1	',
            'ab03': '2e	C	1	',
            'ab04': '2f	V	1	',
            'ab05': '30	B	1	',
            'ab06': '31	N	1	',
            'ab07': '32	M	1	',
            'ab08': '33	OEM_COMMA	0	',
            'ab09': '34	OEM_PERIOD	0	',
            'ab10': '35	OEM_2	0	',

            # pinky keys
            'ae11': '0c	OEM_MINUS	0	',
            'ae12': '0d	OEM_PLUS	0	',
            'ad11': '1a	OEM_4	0	',
            'ad12': '1b	OEM_6	0	',
            'ac11': '28	OEM_7	0	',
            'tlde': '29	OEM_3	0	',
            'bksl': '2b	OEM_5	0	',
            'lsgt': '56	OEM_102	0	'
        }

        output = []
        for keyName in LAYER_KEYS:
            if keyName == '':
                continue

            if keyName.startswith('-'):
                if len(output):
                    output.append('')
                output.append('//' + keyName[1:])
                continue

            symbols = []
            description = '//'
            for i in [0, 1, 4, 5]:
                layer = self.layers[i]

                if keyName in layer:
                    symbol = layer[keyName]
                    desc = symbol
                    if symbol in DEAD_KEYS:
                        desc = DEAD_KEYS[symbol]['klc']
                        symbol = hex_ord(desc) + '@'
                    elif symbol not in SYMBOLS['klc']:
                        symbol = hex_ord(symbol)
                    symbols.append(symbol)
                else:
                    desc = ' '
                    symbols.append('-1')
                description = description + ' ' + desc

            output.append(
                klcKeys[keyName] +
                symbols[0] + '\u0009' + symbols[1] + '\u0009-1\u0009' +
                symbols[2] + '\u0009' + symbols[3] + '\u0009' +
                description.strip())

        return output

    @property
    def klc_deadkey(self):
        """ Windows layout, dead key. """

        output = []
        for i in [0, 1]:
            baseLayer = self.layers[i]
            extLayer = self.layers[i + 2]

            for keyName in LAYER_KEYS:
                if keyName.startswith('-'):
                    if len(output):
                        output.append('')
                    output.append('//' + keyName[1:])
                    continue
                elif keyName in extLayer:
                    base = baseLayer[keyName]
                    if base in DEAD_KEYS:
                        base = DEAD_KEYS[base]['klc']
                    ext = extLayer[keyName]
                    if (ext in DEAD_KEYS):
                        ext = DEAD_KEYS[ext]['klc']
                        lafayette = hex_ord(ext) + '@'
                    else:
                        lafayette = hex_ord(ext)
                    output.append(
                        hex_ord(base) + '\u0009' +
                        lafayette + '\u0009' + '// ' + base + ' -> ' + ext)

        return output


def make_layout(filePath):
    layout = Layout(filePath)
    layout_qwerty = layout.get_geometry([0, 2])  # base + dead key
    layout_altgr = layout.get_geometry([4])      # altgr

    name = os.path.splitext(os.path.basename(filePath))[0]
    if not os.path.exists('dist'):
        os.makedirs('dist')

    # Linux (xkb) driver
    xkb_path = 'dist/' + name + '.xkb'
    xkb_out = openLocalFile('template.xkb').read()
    xkb_out = substitute_lines(xkb_out, 'LAYOUT', layout.xkb)
    xkb_out = substitute_lines(xkb_out, 'GEOMETRY_qwerty', layout_qwerty)
    xkb_out = substitute_lines(xkb_out, 'GEOMETRY_altgr', layout_altgr)
    open(xkb_path, 'w').write(xkb_out)
    print('... ' + xkb_path)

    # Windows (klc) driver
    klc_path = 'dist/' + name + '.klc'
    # klc_out = open('template.klc', 'r', encoding='utf-16le').read()
    klc_out = openLocalFile('template.utf8.klc').read()
    klc_out = substitute_lines(klc_out, 'LAYOUT', layout.klc)
    klc_out = substitute_lines(klc_out, 'DEADKEY', layout.klc_deadkey)
    klc_out = substitute_lines(klc_out, 'GEOMETRY_qwerty', layout_qwerty)
    klc_out = substitute_lines(klc_out, 'GEOMETRY_altgr', layout_altgr)
    klc_out = substitute_token(klc_out, 'encoding', 'UTF-16LE')
    open(klc_path, 'w', encoding='utf-16le') \
        .write(klc_out.replace('\n', '\r\n'))
    print('... ' + klc_path)

for f in sys.argv[1:]:
    make_layout(f)
