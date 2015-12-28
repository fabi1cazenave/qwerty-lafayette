#!/usr/bin/env python3

import re
import unicodedata
import yaml

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

# Yes, this is a global, shared, mutable variable. Sue me.
layout_layers = [{}, {}, {}, {}, {}, {}]

GEOMETRY = yaml.load(open('tpl/geometry.yaml'))
SYMBOLS = yaml.load(open('tpl/symbols.yaml'))


##
# Helper functions
#


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


def template_to_text(template, indent=''):
    out = ''
    for line in template:
        out = out + indent + add_spaces_before_combining_chars(line) + '\n'
    return out[:-1]


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


##
# Linux layout
#


def export_xkb(showDescription=True):
    global layout_layers

    supportedSymbols = SYMBOLS['xkb']
    indent = '    '
    maxLength = 16  # `ISO_Level3_Latch` should be the longest dead key name

    output = []
    for keyName in LAYER_KEYS:
        if keyName == '':
            continue

        if keyName.startswith('-'):  # separator
            if len(output):
                output.append('')
            output.append(indent + '//' + keyName[1:])
            continue

        symbols = []
        description = ' //'
        for layer in layout_layers:
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

        line = indent + 'key ' +                   \
            '<' + keyName.upper() + '> ' + '{[ ' + \
            symbols[0].ljust(maxLength) + ', ' +   \
            symbols[1].ljust(maxLength) + ', ' +   \
            symbols[2].ljust(maxLength) + ', ' +   \
            symbols[3].ljust(maxLength) + '],[ ' + \
            symbols[4].ljust(maxLength) + ', ' +   \
            symbols[5].ljust(maxLength) + ']};'
        if showDescription:
            line = line + description
        output.append(line)

    return '\n'.join(output)


##
# Windows layout - should be converted to UTF-16LE
#


def export_klc_layout():
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
            layer = layout_layers[i]

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

    return '\n'.join(output)


def export_klc_deadkey():
    global layout_layers

    output = []
    for i in [0, 1]:
        baseLayer = layout_layers[i]
        extLayer = layout_layers[i + 2]

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

    return '\n'.join(output)


##
# Geometry views
#


def fill_template(template, rows, layerNumber):
    global layout_layers

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
            if key in layout_layers[layerNumber]:
                baseKey = layout_layers[layerNumber][key]

            shiftKey = ' '
            if key in layout_layers[layerNumber + 1]:
                shiftKey = layout_layers[layerNumber + 1][key]

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


def export_geometry_base(name='ISO', indent=''):
    rows = GEOMETRY[name]['rows']
    template = GEOMETRY[name]['template'].split('\n')[:-1]
    return template_to_text(fill_template(template, rows, 0), indent)


def export_geometry_altgr(name='ISO', indent=''):
    rows = GEOMETRY[name]['rows']
    template = GEOMETRY[name]['template'].split('\n')[:-1]
    return template_to_text(fill_template(template, rows, 4), indent)


def export_geometry_dead(name='ISO', indent=''):
    rows = GEOMETRY[name]['rows']
    template = GEOMETRY[name]['template'].split('\n')[:-1]
    template = fill_template(template, rows, 0)
    template = fill_template(template, rows, 2)
    return template_to_text(template, indent)


def export_geometry(name='ISO', indent=''):
    return \
        export_geometry_dead(name, indent) + '\n\n' + \
        export_geometry_altgr(name, indent)


##
# Layout importer
#


def parse_template(template, rows, layerNumber):
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
                layout_layers[layerNumber + 0][key] = baseKey
            if (shiftKey != ' '):
                layout_layers[layerNumber + 1][key] = shiftKey

            i = i + 6

        j = j + 1


def import_layout(filePath):
    global layout_layers
    layout_layers = [{}, {}, {}, {}, {}, {}]

    cfg = yaml.load(open(filePath))
    rows = GEOMETRY[cfg['geometry']]['rows']
    base = remove_spaces_before_combining_chars(cfg['base']).split('\n')
    altgr = remove_spaces_before_combining_chars(cfg['altgr']).split('\n')
    parse_template(base, rows, 0)
    parse_template(base, rows, 2)
    parse_template(altgr, rows, 4)


##
# Main
#


def make_layout(name):
    import_layout('src/' + name + '.yaml')

    # Linux (xkb) driver
    xkb_layout = export_xkb(False)
    xkb_geometry = export_geometry('ISO', '  // ')

    xkb_path = 'out/' + name + '.xkb'
    xkb_out = open('tpl/template.xkb').read()
    xkb_out = re.sub(r'.*LAFAYETTE::LAYOUT.*', xkb_layout, xkb_out)
    xkb_out = re.sub(r'.*LAFAYETTE::GEOMETRY.*', xkb_geometry, xkb_out)
    open(xkb_path, 'w').write(xkb_out)
    print(xkb_path)

    # Windows (klc) driver
    klc_layout = export_klc_layout()
    klc_deadkey = export_klc_deadkey()
    klc_geometry = export_geometry('ANSI', '// ')

    klc_path = 'out/' + name + '.klc'
    klc_out = open('tpl/template.klc', 'r', encoding='utf-16le').read()
    klc_out = re.sub(r'.*LAFAYETTE::LAYOUT.*', klc_layout, klc_out)
    klc_out = re.sub(r'.*LAFAYETTE::DEADKEY.*', klc_deadkey, klc_out)
    klc_out = re.sub(r'.*LAFAYETTE::GEOMETRY.*', klc_geometry, klc_out)
    open(klc_path, 'w',
         encoding='utf-16le').write(klc_out.replace('\n', '\r\n'))
    print(klc_path)


make_layout('dvorak')
make_layout('qwerty42a')
make_layout('qwerty42b')
make_layout('lafayette')

# A quick visual control never hurts
print(export_geometry_dead('ERGO'))
print(export_geometry_altgr('ERGO'))
