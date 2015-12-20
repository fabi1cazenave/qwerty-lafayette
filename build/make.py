#!/usr/bin/python3

layers = []

DEAD_KEYS = {                                            # combining diacritics
    '\u20e1': { 'klc': '¤', 'xkb': 'ISO_Level3_Latch' }, #  ⃡ #
    '\u0300': { 'klc': '`', 'xkb': 'dead_grave'       }, #  ̀ #
    '\u0301': { 'klc': '´', 'xkb': 'dead_acute'       }, #  ́ #
    '\u0302': { 'klc': '^', 'xkb': 'dead_circumflex'  }, #  ̂ #
    '\u0303': { 'klc': '~', 'xkb': 'dead_tilde'       }, #  ̃ #
    '\u0307': { 'klc': '˙', 'xkb': 'dead_abovedot'    }, #  ̇ #
    '\u0308': { 'klc': '¨', 'xkb': 'dead_diaeresis'   }, #  ̈ #
    '\u030a': { 'klc': '˚', 'xkb': 'dead_abovering'   }, #  ̊ #
    '\u0326': { 'klc': ',', 'xkb': 'dead_commabelow'  }, #  ̦ #
    '\u0327': { 'klc': '¸', 'xkb': 'dead_cedilla'     }, #  ̧ #
    '\u0328': { 'klc': '˛', 'xkb': 'dead_ogonek'      }  #  ̨ #
}

LAYER_KEYS = [
    '- digits',
    'ae01', 'ae02', 'ae03', 'ae04', 'ae05',
    'ae06', 'ae07', 'ae08', 'ae09', 'ae10',

    '- letters, first row',
    'ad01', 'ad02', 'ad03', 'ad04', 'ad05',
    'ad06', 'ad07', 'ad08', 'ad09', 'ad10',

    '- letters, second row',
    'ac01', 'ac02', 'ac03', 'ac04', 'ac05',
    'ac06', 'ac07', 'ac08', 'ac09', 'ac10',

    '- letters, third row',
    'ab01', 'ab02', 'ab03', 'ab04', 'ab05',
    'ab06', 'ab07', 'ab08', 'ab09', 'ab10',

    '- pinky keys',
    'tlde', 'ae11', 'ae12', 'ad11', 'ad12', 'bksl', 'ac11', 'lsgt'
]

def import_layout(filePath):
    layout = open(filePath).read()

    keys = [
        '', 'tlde',
        '', 'ae01', 'ae02', 'ae03', 'ae04', 'ae05',
        '', 'ae06', 'ae07', 'ae08', 'ae09', 'ae10',
        '', 'ae11', 'ae12', '', '',
        '', '',
        '', 'ad01', 'ad02', 'ad03', 'ad04', 'ad05',
        '', 'ad06', 'ad07', 'ad08', 'ad09', 'ad10',
        '', 'ad11', 'ad12', 'bksl', '',
        '', '',
        '', 'ac01', 'ac02', 'ac03', 'ac04', 'ac05',
        '', 'ac06', 'ac07', 'ac08', 'ac09', 'ac10',
        '', 'ac11', '', '', '',
        '', 'lsgt',
        '', 'ab01', 'ab02', 'ab03', 'ab04', 'ab05',
        '', 'ab06', 'ab07', 'ab08', 'ab09', 'ab10'
    ]

    lines = layout.split('\u2502') # │
    levels = [
        lines[9]  + lines[13] + lines[17] + lines[21], #       base
        lines[33] + lines[37] + lines[41] + lines[45], # shift base
        lines[10] + lines[14] + lines[18] + lines[22], #       lafayette
        lines[34] + lines[38] + lines[42] + lines[46], # shift lafayette
        lines[11] + lines[15] + lines[19] + lines[23], #       AltGr
        lines[35] + lines[39] + lines[43] + lines[47]  # shift AltGr
    ]

    for level in range(6):
        layer = {}
        i = 0
        keyValue = levels[level][0]
        for keyName in keys:
            nextValue = levels[level][i + 1]
            if (nextValue in DEAD_KEYS):
                layer[keyName] = nextValue
                i = i + 1
            elif (keyName != '' and keyValue != ' ' and keyValue != ' '):
                layer[keyName] = keyValue
            i = i + 1
            keyValue = nextValue
        layers.append(layer)

def hex_ord(char):
    return hex(ord(char))[2:].zfill(4)

##
# Linux layout
#

def export_xkb():
    supportedSymbols = { # /usr/include/X11/keysymdef.h
        '\u0020': 'space',
        '\u0021': 'exclam',
        '\u0022': 'quotedbl',
        '\u0023': 'numbersign',
        '\u0024': 'dollar',
        '\u0025': 'percent',
        '\u0026': 'ampersand',
        '\u0027': 'apostrophe',
        '\u0027': 'quoteright',
        '\u0028': 'parenleft',
        '\u0029': 'parenright',
        '\u002a': 'asterisk',
        '\u002b': 'plus',
        '\u002c': 'comma',
        '\u002d': 'minus',
        '\u002e': 'period',
        '\u002f': 'slash',
        '\u0030': '0',
        '\u0031': '1',
        '\u0032': '2',
        '\u0033': '3',
        '\u0034': '4',
        '\u0035': '5',
        '\u0036': '6',
        '\u0037': '7',
        '\u0038': '8',
        '\u0039': '9',
        '\u003a': 'colon',
        '\u003b': 'semicolon',
        '\u003c': 'less',
        '\u003d': 'equal',
        '\u003e': 'greater',
        '\u003f': 'question',
        '\u0040': 'at',
        '\u0041': 'A',
        '\u0042': 'B',
        '\u0043': 'C',
        '\u0044': 'D',
        '\u0045': 'E',
        '\u0046': 'F',
        '\u0047': 'G',
        '\u0048': 'H',
        '\u0049': 'I',
        '\u004a': 'J',
        '\u004b': 'K',
        '\u004c': 'L',
        '\u004d': 'M',
        '\u004e': 'N',
        '\u004f': 'O',
        '\u0050': 'P',
        '\u0051': 'Q',
        '\u0052': 'R',
        '\u0053': 'S',
        '\u0054': 'T',
        '\u0055': 'U',
        '\u0056': 'V',
        '\u0057': 'W',
        '\u0058': 'X',
        '\u0059': 'Y',
        '\u005a': 'Z',
        '\u005b': 'bracketleft',
        '\u005c': 'backslash',
        '\u005d': 'bracketright',
        '\u005e': 'asciicircum',
        '\u005f': 'underscore',
        '\u0060': 'grave',
        '\u0060': 'quoteleft',
        '\u0061': 'a',
        '\u0062': 'b',
        '\u0063': 'c',
        '\u0064': 'd',
        '\u0065': 'e',
        '\u0066': 'f',
        '\u0067': 'g',
        '\u0068': 'h',
        '\u0069': 'i',
        '\u006a': 'j',
        '\u006b': 'k',
        '\u006c': 'l',
        '\u006d': 'm',
        '\u006e': 'n',
        '\u006f': 'o',
        '\u0070': 'p',
        '\u0071': 'q',
        '\u0072': 'r',
        '\u0073': 's',
        '\u0074': 't',
        '\u0075': 'u',
        '\u0076': 'v',
        '\u0077': 'w',
        '\u0078': 'x',
        '\u0079': 'y',
        '\u007a': 'z',
        '\u007b': 'braceleft',
        '\u007c': 'bar',
        '\u007d': 'braceright',
        '\u007e': 'asciitilde',

        '\u00a0': 'nobreakspace',
        '\u00a1': 'exclamdown',
        '\u00a2': 'cent',
        '\u00a3': 'sterling',
        '\u00a4': 'currency',
        '\u00a5': 'yen',
        '\u00a6': 'brokenbar',
        '\u00a7': 'section',
        '\u00a8': 'diaeresis',
        '\u00a9': 'copyright',
        '\u00aa': 'ordfeminine',
        '\u00ab': 'guillemotleft',
        '\u00ac': 'notsign',
        '\u00ad': 'hyphen',
        '\u00ae': 'registered',
        '\u00af': 'macron',
        '\u00b0': 'degree',
        '\u00b1': 'plusminus',
        '\u00b2': 'twosuperior',
        '\u00b3': 'threesuperior',
        '\u00b4': 'acute',
        '\u00b5': 'mu',
        '\u00b6': 'paragraph',
        '\u00b7': 'periodcentered',
        '\u00b8': 'cedilla',
        '\u00b9': 'onesuperior',
        '\u00ba': 'masculine',
        '\u00bb': 'guillemotright',
        '\u00bc': 'onequarter',
        '\u00bd': 'onehalf',
        '\u00be': 'threequarters',
        '\u00bf': 'questiondown',
        '\u00c0': 'Agrave',
        '\u00c1': 'Aacute',
        '\u00c2': 'Acircumflex',
        '\u00c3': 'Atilde',
        '\u00c4': 'Adiaeresis',
        '\u00c5': 'Aring',
        '\u00c6': 'AE',
        '\u00c7': 'Ccedilla',
        '\u00c8': 'Egrave',
        '\u00c9': 'Eacute',
        '\u00ca': 'Ecircumflex',
        '\u00cb': 'Ediaeresis',
        '\u00cc': 'Igrave',
        '\u00cd': 'Iacute',
        '\u00ce': 'Icircumflex',
        '\u00cf': 'Idiaeresis',
        '\u00d0': 'ETH',
        '\u00d0': 'Eth',
        '\u00d1': 'Ntilde',
        '\u00d2': 'Ograve',
        '\u00d3': 'Oacute',
        '\u00d4': 'Ocircumflex',
        '\u00d5': 'Otilde',
        '\u00d6': 'Odiaeresis',
        '\u00d7': 'multiply',
        '\u00d8': 'Oslash',
        '\u00d8': 'Ooblique',
        '\u00d9': 'Ugrave',
        '\u00da': 'Uacute',
        '\u00db': 'Ucircumflex',
        '\u00dc': 'Udiaeresis',
        '\u00dd': 'Yacute',
        '\u00de': 'THORN',
        '\u00de': 'Thorn',
        '\u00df': 'ssharp',
        '\u00e0': 'agrave',
        '\u00e1': 'aacute',
        '\u00e2': 'acircumflex',
        '\u00e3': 'atilde',
        '\u00e4': 'adiaeresis',
        '\u00e5': 'aring',
        '\u00e6': 'ae',
        '\u00e7': 'ccedilla',
        '\u00e8': 'egrave',
        '\u00e9': 'eacute',
        '\u00ea': 'ecircumflex',
        '\u00eb': 'ediaeresis',
        '\u00ec': 'igrave',
        '\u00ed': 'iacute',
        '\u00ee': 'icircumflex',
        '\u00ef': 'idiaeresis',
        '\u00f0': 'eth',
        '\u00f1': 'ntilde',
        '\u00f2': 'ograve',
        '\u00f3': 'oacute',
        '\u00f4': 'ocircumflex',
        '\u00f5': 'otilde',
        '\u00f6': 'odiaeresis',
        '\u00f7': 'division',
        '\u00f8': 'oslash',
        '\u00f8': 'ooblique',
        '\u00f9': 'ugrave',
        '\u00fa': 'uacute',
        '\u00fb': 'ucircumflex',
        '\u00fc': 'udiaeresis',
        '\u00fd': 'yacute',
        '\u00fe': 'thorn',
        '\u00ff': 'ydiaeresis',
    }

    indent = '    '
    maxLength = 16 # `ISO_Level3_Latch` should be the longest dead key name

    output = []
    for keyName in LAYER_KEYS:
        if keyName == '':
            continue

        if keyName.startswith('-'):
            if len(output):
                output.append('')
            output.append(indent + '//' + keyName[1:])
            continue

        symbols = []
        description = '//'
        for layer in layers:
            if keyName in layer:
                symbol = layer[keyName]
                desc = symbol
                if symbol in DEAD_KEYS:
                    desc   = DEAD_KEYS[symbol]['klc']
                    symbol = DEAD_KEYS[symbol]['xkb']
                elif symbol in supportedSymbols \
                        and len(supportedSymbols[symbol]) < maxLength:
                    symbol = supportedSymbols[symbol]
                else:
                    symbol = 'U' + hex_ord(symbol).upper()
                symbols.append(symbol)
            else:
                desc = ' '
                symbols.append('VoidSymbol')
            description = description + ' ' + desc

        output.append(indent + 'key ' +                  \
                '<' + keyName.upper() + '> ' + '{[ '   + \
                symbols[0].ljust(maxLength)  +  ', '   + \
                symbols[1].ljust(maxLength)  +  ', '   + \
                symbols[2].ljust(maxLength)  +  ', '   + \
                symbols[3].ljust(maxLength)  + '],[ '  + \
                symbols[4].ljust(maxLength)  +  ', '   + \
                symbols[5].ljust(maxLength)  + ' ]}; ' + \
                description.strip())

    return '\n'.join(output)

##
# Windows layout - should be converted to UTF-16LE
#

def export_klc_layout():
    supportedSymbols = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'Z', 'X', 'C', 'V', 'B', 'M',
        'z', 'x', 'c', 'v', 'b', 'm'
    ]

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
        for i in [ 0, 1, 4, 5 ]:
            layer = layers[i]

            if keyName in layer:
                symbol = layer[keyName]
                desc = symbol
                if symbol in DEAD_KEYS:
                    desc = DEAD_KEYS[symbol]['klc']
                    symbol = hex_ord(desc) + '@'
                elif not symbol in supportedSymbols:
                    symbol = hex_ord(symbol)
                symbols.append(symbol)
            else:
                desc = ' '
                symbols.append('-1')
            description = description + ' ' + desc

        output.append(klcKeys[keyName] +                             \
            symbols[0] + '\u0009' + symbols[1] + '\u0009-1\u0009' +  \
            symbols[2] + '\u0009' + symbols[3] + '\u0009' +          \
            description.strip())

    return '\n'.join(output)

def export_klc_deadkey():
    output = []

    for i in [ 0, 1 ]:
        baseLayer = layers[i]
        extLayer = layers[i + 2]

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
                output.append(hex_ord(base) + '\u0009' + \
                    lafayette + '\u0009' + '// ' + base + ' -> ' + ext)

    return '\n'.join(output)

##
# Geometry views
#

GEOMETRY_ANSI = {
    'template': [
        "┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓",
        "│     │     │     │     │     │     │     │     │     │     │     │     │     ┃          ┃",
        "│     │     │     │     │     │     │     │     │     │     │     │     │     ┃ ⌫        ┃",
        "┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┯━━━━━━━┩",
        "┃        ┃     │     │     │     │     │     │     │     │     │     │     │     │       │",
        "┃ ↹      ┃     │     │     │     │     │     │     │     │     │     │     │     │       │",
        "┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┲━━━━┷━━━━━━━┪",
        "┃         ┃     │     │     │     │     │     │     │     │     │     │     ┃            ┃",
        "┃ ⇬       ┃     │     │     │     │     │     │     │     │     │     │     ┃ ⏎          ┃",
        "┣━━━━━━━━━┻━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┻━━━━━━━━━━━━┫",
        "┃            ┃     │     │     │     │     │     │     │     │     │     ┃               ┃",
        "┃ ⇧          ┃     │     │     │     │     │     │     │     │     │     ┃ ⇧             ┃",
        "┣━━━━━━━┳━━━━┻━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫",
        "┃       ┃       ┃       ┃ ⍽ nbsp                         ┃       ┃       ┃       ┃       ┃",
        "┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                            ’ ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃",
        "┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛"
    ],
    'rows': [
        { 'offset': 2, 'keys': [
            'tlde',
            'ae01', 'ae02', 'ae03', 'ae04', 'ae05',
            'ae06', 'ae07', 'ae08', 'ae09', 'ae10',
            'ae11', 'ae12'
        ]},
        { 'offset': 11, 'keys': [
            'ad01', 'ad02', 'ad03', 'ad04', 'ad05',
            'ad06', 'ad07', 'ad08', 'ad09', 'ad10',
            'ad11', 'ad12', 'bksl'
        ]},
        { 'offset': 12, 'keys': [
            'ac01', 'ac02', 'ac03', 'ac04', 'ac05',
            'ac06', 'ac07', 'ac08', 'ac09', 'ac10',
            'ac11'
        ]},
        { 'offset': 15, 'keys': [
            'ab01', 'ab02', 'ab03', 'ab04', 'ab05',
            'ab06', 'ab07', 'ab08', 'ab09', 'ab10'
        ]}
    ]
}

GEOMETRY_ISO = {
    'template': [
        "┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓",
        "│     │     │     │     │     │     │     │     │     │     │     │     │     ┃          ┃",
        "│     │     │     │     │     │     │     │     │     │     │     │     │     ┃ ⌫        ┃",
        "┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫",
        "┃        ┃     │     │     │     │     │     │     │     │     │     │     │     ┃       ┃",
        "┃ ↹      ┃     │     │     │     │     │     │     │     │     │     │     │     ┃       ┃",
        "┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃",
        "┃         ┃     │     │     │     │     │     │     │     │     │     │     │     ┃      ┃",
        "┃ ⇬       ┃     │     │     │     │     │     │     │     │     │     │     │     ┃      ┃",
        "┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫",
        "┃      ┃     │     │     │     │     │     │     │     │     │     │     ┃               ┃",
        "┃ ⇧    ┃     │     │     │     │     │     │     │     │     │     │     ┃ ⇧             ┃",
        "┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫",
        "┃       ┃       ┃       ┃ ⍽ nbsp                         ┃       ┃       ┃       ┃       ┃",
        "┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                            ’ ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃",
        "┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛"
    ],
    'rows': [
        { 'offset': 2, 'keys': [
            'tlde',
            'ae01', 'ae02', 'ae03', 'ae04', 'ae05',
            'ae06', 'ae07', 'ae08', 'ae09', 'ae10',
            'ae11', 'ae12'
        ]},
        { 'offset': 11, 'keys': [
            'ad01', 'ad02', 'ad03', 'ad04', 'ad05',
            'ad06', 'ad07', 'ad08', 'ad09', 'ad10',
            'ad11', 'ad12'
        ]},
        { 'offset': 12, 'keys': [
            'ac01', 'ac02', 'ac03', 'ac04', 'ac05',
            'ac06', 'ac07', 'ac08', 'ac09', 'ac10',
            'ac11', 'bksl',
        ]},
        { 'offset': 9, 'keys': [
            'lsgt',
            'ab01', 'ab02', 'ab03', 'ab04', 'ab05',
            'ab06', 'ab07', 'ab08', 'ab09', 'ab10'
        ]}
    ]
}

GEOMETRY_ERGO = {
    'template': [
        "╭╌╌╌╌╌┰─────┬─────┬─────┬─────┬─────┰─────┬─────┬─────┬─────┬─────┰╌╌╌╌╌┬╌╌╌╌╌╮",
        "┆     ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "┆     ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "╰╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤",
        "      ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "      ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "      ┠─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┼╌╌╌╌╌┤",
        "      ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "      ┃     │     │     │     │     ┃     │     │     │     │     ┃     ┆     ┆",
        "╭╌╌╌╌╌╂─────┼─────┼─────┼─────┼─────╂─────┼─────┼─────┼─────┼─────╂╌╌╌╌╌┴╌╌╌╌╌╯",
        "┆     ┃     │     │     │     │     ┃     │     │     │     │     ┃            ",
        "┆     ┃     │     │     │     │     ┃     │     │     │     │     ┃            ",
        "╰╌╌╌╌╌┸─────┴─────┴─────┴─────┴─────┸─────┴─────┴─────┴─────┴─────┚            ",
        "                ╭───────┬───────────────────────┬───────╮                      ",
        "                │  Alt  │                       │ AltGr │                      ",
        "                ╰───────┴───────────────────────┴───────╯                      "
    ],
    'rows': [
        { 'offset': 2, 'keys': GEOMETRY_ISO['rows'][0]['keys'] },
        { 'offset': 8, 'keys': GEOMETRY_ISO['rows'][1]['keys'] },
        { 'offset': 8, 'keys': GEOMETRY_ISO['rows'][2]['keys'] },
        { 'offset': 2, 'keys': GEOMETRY_ISO['rows'][3]['keys'] }
    ]
}

def get_template(template, rows, layerNumber):
    if layerNumber == 0: # base layer
        colOffset = 0
        shiftPrevails = True
    else: # AltGr or dead key (lafayette)
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
            if key in layers[layerNumber]:
                baseKey = layers[layerNumber][key]
                if baseKey in DEAD_KEYS:
                    # baseKey = ' ' + baseKey
                    baseKey = DEAD_KEYS[baseKey]['klc']

            shiftKey = ' '
            if key in layers[layerNumber + 1]:
                shiftKey = layers[layerNumber + 1][key]
                if shiftKey in DEAD_KEYS:
                    # shiftKey = ' ' + shiftKey
                    shiftKey = DEAD_KEYS[shiftKey]['klc']

            if shiftPrevails:
                shift[i] = shiftKey
                if baseKey.upper() != shiftKey:
                    base[i] = baseKey
            else:
                base[i] = baseKey
                if baseKey.upper() != shiftKey:
                    shift[i] = shiftKey

            i = i + 6

        template[2 + j * 3] = ''.join(base)
        template[1 + j * 3] = ''.join(shift)
        j = j + 1

    return template

def export_geometry_base(geometry, prepend=''):
    template = get_template(geometry['template'][:], geometry['rows'], 0)
    return '\n'.join([ (prepend + '{0}').format(line) for line in template ])

def export_geometry_altgr(geometry, prepend=''):
    template = get_template(geometry['template'][:], geometry['rows'], 4)
    return '\n'.join([ (prepend + '{0}').format(line) for line in template ])

def export_geometry_dead(geometry, prepend=''):
    template = geometry['template'][:]
    template = get_template(template, geometry['rows'], 0)
    template = get_template(template, geometry['rows'], 2)
    return '\n'.join([ (prepend + '{0}').format(line) for line in template ])

def export_geometry(geometry, prepend=''):
    return \
        export_geometry_dead(geometry, prepend) + '\n\n' + \
        export_geometry_altgr(geometry, prepend)

##
# Main
#

import re

input_path = 'lafayette'
import_layout(input_path)

# Linux (xkb) driver
xkb_layout   = export_xkb()
xkb_geometry = export_geometry(GEOMETRY_ISO, '    // ')

xkb_path = input_path + '.xkb'
xkb_out = open('template.xkb').read()
xkb_out = re.sub(r'.*LAFAYETTE::LAYOUT.*',   xkb_layout,   xkb_out)
xkb_out = re.sub(r'.*LAFAYETTE::GEOMETRY.*', xkb_geometry, xkb_out)
open(xkb_path, 'w').write(xkb_out)
print(xkb_path)

# Windows (klc) driver
klc_layout   = export_klc_layout()
klc_deadkey  = export_klc_deadkey()
klc_geometry = export_geometry(GEOMETRY_ANSI, '// ')

klc_path = input_path + '.klc'
klc_out = open('template.klc', 'r', encoding='utf-16le').read()
klc_out = re.sub(r'.*LAFAYETTE::LAYOUT.*',   klc_layout,   klc_out)
klc_out = re.sub(r'.*LAFAYETTE::DEADKEY.*',  klc_deadkey,  klc_out)
klc_out = re.sub(r'.*LAFAYETTE::GEOMETRY.*', klc_geometry, klc_out)
open(klc_path, 'w', encoding='utf-16le').write(klc_out.replace('\n', '\r\n'))
print(klc_path)

# A quick visual control never hurts
print(export_geometry_dead(GEOMETRY_ERGO))

