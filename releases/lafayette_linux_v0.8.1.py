#!/usr/bin/env python3
"""
This Python installer is designed to tweak XKB to update keyboard layouts.
It operates on three files:
    - /usr/share/X11/xkb/symbols/[locale] is a text file containing all layouts
    - /usr/share/X11/xkb/rules/{base,evdev}.xml is an index listing all layouts
When run as root, it will:
    - erase any legacy Lafayette or kalamine::lafayette layout
    - install the kalamine::lafayette layout at the end of this file

Most of this file is just a copy of kalamine’s xkb_manager.py module. It should
do exactly the same thing as running xkalamine as root, without having to
pip-install kalamine as root. The installer itself is in the very last section.
"""

import os
import shutil
import sys
import textwrap  # dedent hard-coded symbol strings
import traceback

from lxml import etree
from lxml.builder import E


class XKBManager:
    """ Wrapper to list/add/remove keyboard drivers to XKB. """

    def __init__(self, xkb_root='/usr/share/X11/xkb/'):
        self._rootdir = xkb_root
        self._index = {}

    @property
    def index(self):
        return self._index.items()

    def add(self, layout):
        locale = layout.meta['locale']
        variant = layout.meta['variant']
        if locale not in self._index:
            self._index[locale] = {}
        self._index[locale][variant] = layout

    def remove(self, layout_id):
        locale, variant = layout_id.split('/')
        if locale not in self._index:
            self._index[locale] = {}
        self._index[locale][variant] = None

    def update(self):
        update_symbols(self._rootdir, self._index)  # XKB/symbols/{locales}
        update_rules(self._rootdir, self._index)  # XKB/rules/{base,evdev}.xml
        self._index = {}


###############################################################################
# Helpers: XKB/symbols
#

""" On GNU/Linux, keyboard layouts must be installed in /usr/share/X11/xkb. To
    be able to revert a layout installation, Kalamine marks layouts like this:

    - XKB/symbols/[locale]: layout definitions
        // KALAMINE::[NAME]::BEGIN
        xkb_symbols "[name]" { ... }
        // KALAMINE::[NAME]::END

    - XKB/rules/{base,evdev}.xml: layout references
        <variant>
            <configItem>
                <name>lafayette42</name>
                <description>French (Lafayette42)</description>
            </configItem>
        </variant>

    Unfortunately, the Lafayette project has released a first installer before
    the XKalamine installer was developed, so we have to handle this situation
    too:

    - XKB/symbols/[locale]: layout definitions
        // LAFAYETTE::BEGIN
        xkb_symbols "lafayette"   { ... }
        xkb_symbols "lafayette42" { ... }
        // LAFAYETTE::END

    - XKB/rules/{base,evdev}.xml: layout references
        <variant type="lafayette">
            <configItem>
                <name>lafayette</name>
                <description>French (Lafayette)</description>
            </configItem>
        </variant>
        <variant type="lafayette">
            <configItem>
                <name>lafayette42</name>
                <description>French (Lafayette42)</description>
            </configItem>
        </variant>

    Consequence: these two Lafayette layouts must be uninstalled together.
    Because of the way they are grouped in symbols/fr, it is impossible to
    remove one without removing the other.
"""

LEGACY_MARK = {
    'begin': '// LAFAYETTE::BEGIN\n',
    'end': '// LAFAYETTE::END\n'
}


def get_symbol_mark(name):
    return {
        'begin': '// KALAMINE::' + name.upper() + '::BEGIN\n',
        'end': '// KALAMINE::' + name.upper() + '::END\n'
    }


def update_symbols_locale(path, named_layouts):
    """ Update Kalamine layouts in an xkb/symbols file. """

    text = ''
    modified_text = False
    NAMES = list(map(lambda n: n.upper(), named_layouts.keys()))

    def is_marked_for_deletion(line):
        if line.startswith('// KALAMINE::'):
            name = line[13:-8]
        elif line.startswith('// LAFAYETTE::'):
            name = 'LAFAYETTE'
        else:
            return False
        return name in NAMES

    with open(path, 'r+') as symbols:

        # look for Kalamine layouts to be updated or removed
        between_marks = False
        closing_mark = ''
        for line in symbols:
            if line.endswith('::BEGIN\n'):
                if is_marked_for_deletion(line):
                    closing_mark = line[:-6] + 'END\n'
                    modified_text = True
                    between_marks = True
                    text = text.rstrip()
                else:
                    text += line
            elif line.endswith('::END\n'):
                if between_marks and line.startswith(closing_mark):
                    between_marks = False
                    closing_mark = ''
                else:
                    text += line
            elif not between_marks:
                text += line

        # clear previous Kalamine layouts if needed
        if modified_text:
            symbols.seek(0)
            symbols.write(text.rstrip() + '\n')
            symbols.truncate()

        # add new Kalamine layouts
        for name, layout in named_layouts.items():
            if layout is None:
                print('      - ' + name)
            else:
                print('      + ' + name)
                MARK = get_symbol_mark(name)
                symbols.write('\n')
                symbols.write(MARK['begin'])
                symbols.write(layout.xkb_patch.rstrip() + '\n')
                symbols.write(MARK['end'])

        symbols.close()


def update_symbols(xkb_root, kbindex):
    """ Update Kalamine layouts in all xkb/symbols files. """

    for locale, named_layouts in kbindex.items():
        path = os.path.join(xkb_root, 'symbols', locale)
        if not os.path.exists(path):
            exit_LocaleNotSupported(locale)

        try:
            if not os.path.isfile(path + '.orig'):
                # backup, just in case :-)
                shutil.copy(path, path + '.orig')
                print('... ' + path + '.orig (backup)')

            print('... ' + path)
            update_symbols_locale(path, named_layouts)

        except Exception as e:
            exit_FileNotWritable(e, path)


###############################################################################
# Helpers: XKB/rules
#

def get_rules_locale(tree, locale):
    query = '//layout/configItem/name[text()="%s"]/../..' % locale
    result = tree.xpath(query)
    if len(result) != 1:
        exit_LocaleNotSupported(locale)
    return tree.xpath(query)[0]


def remove_rules_variant(variant_list, name):
    query = f"variant/configItem/name[text()='{name}']/../.."
    for variant in variant_list.xpath(query):
        variant.getparent().remove(variant)

def add_rules_variant(variant_list, name, description):
    variant_list.append(
        E.variant(
            E.configItem(E.name(name), E.description(description))))


def update_rules(xkb_root, kbindex):
    """ Update references in XKB/rules/{base,evdev}.xml. """

    for filename in ['base.xml', 'evdev.xml']:
        try:
            path = os.path.join(xkb_root, 'rules', filename)
            tree = etree.parse(path, etree.XMLParser(remove_blank_text=True))

            for locale, named_layouts in kbindex.items():
                vlist = get_rules_locale(tree, locale).xpath('variantList')
                if len(vlist) != 1:
                    exit('Error: unexpected xml format in %s.' % path)
                for name, layout in named_layouts.items():
                    remove_rules_variant(vlist[0], name)
                    if layout is not None:
                        description = layout.meta['description']
                        add_rules_variant(vlist[0], name, description)

            tree.write(path, pretty_print=True, xml_declaration=True,
                       encoding='utf-8')
            print('... ' + path)

        except Exception as e:
            exit_FileNotWritable(e, path)


###############################################################################
# Exception Handling (there must be a better way...)
#

def exit(message):
    print('')
    print(message)
    sys.exit(1)


def exit_LocaleNotSupported(locale):
    exit('Error: the `%s` locale is not supported.' % locale)


def exit_FileNotWritable(exception, path):
    if isinstance(exception, PermissionError):  # noqa: F821
        exit('Permission denied. Are you root?')
    elif isinstance(exception, IOError):
        exit('Error: could not write to file %s.' % path)
    else:  # exit('Unexpected error: ' + sys.exc_info()[0])
        exit('Error: {}.\n{}'.format(exception, traceback.format_exc()))


###############################################################################
# Layouts to install
#

LOCALE = 'fr'
PREFIX = 'lafayette'
LAYOUTS = [{
    'meta': {
        'locale': LOCALE,
        'variant': 'lafayette',
        'description': 'French (Qwerty-Lafayette)',
    },
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.8.0
        // Last change   : 2023-01-17
        // License       : WTFPL - Do What The Fuck You Want Public License
        //
        // French (Qwerty-Lafayette)
        //
        // Base layer + dead key
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │ ~   │ ! ¡ │ @ ‘ │ # ’ │ $ ¢ │ % ‰ │ ^   │ &   │ * ★ │ (   │ )   │ _ – │ + ± ┃          ┃
        // │ `   │ 1 „ │ 2 “ │ 3 ” │ 4 £ │ 5 € │ 6 ¤ │ 7   │ 8 § │ 9 ¶ │ 0 ° │ - — │ = ≠ ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃ Q   │ W   │ E   │ R ™ │ T   │ Y   │ U   │ I   │ O   │ P   │ «   │ »   ┃       ┃
        // ┃ ↹      ┃   æ │   é │   è │   ® │   þ │     │   ù │   ĳ │   œ │     │*^   │*¨   ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃ A   │ S   │ D   │ F ª │ G   │ H   │ J   │ K   │ L   │**   │ "   │ |   ┃      ┃
        // ┃ ⇬       ┃   à │   ß │   ð │   ſ │   © │   ← │   ↓ │   ↑ │   → │** ` │ '   │ \\   ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃ > ≥ │ Z   │ X   │ C   │ V   │ B   │ N   │ M º │ ; • │ :   │ ? ¿ ┃               ┃
        // ┃ ⇧    ┃ < ≤ │     │   × │   ç │   ŭ │   † │   ñ │   µ │ , · │ . … │ / ÷ ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
        //
        // AltGr layer
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │  *~ │     │   ⁽ │   ⁾ │  *´ │  *¨ │  *^ │   ⁷ │   ⁸ │   ⁹ │   ÷ │     │     ┃          ┃
        // │  *` │   ! │   ( │   ) │   ' │   " │  *¤ │   7 │   8 │   9 │   / │     │     ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃   ≠ │     │     │   — │   ± │     │   ⁴ │   ⁵ │   ⁶ │   × │     │     ┃       ┃
        // ┃ ↹      ┃   = │   < │   > │   - │   + │     │   4 │   5 │   6 │   * │  *ˇ │     ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃     │     │     │     │     │     │   ¹ │   ² │   ³ │   − │  *˙ │     ┃      ┃
        // ┃ ⇬       ┃   { │   [ │   ] │   } │   / │     │   1 │   2 │   3 │   - │  *´ │     ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃     │  *~ │  *` │     │   – │     │     │   ⁰ │  *¸ │     │   ¬ ┃               ┃
        // ┃ ⇧    ┃     │   ~ │   ` │   | │   _ │   \\ │     │   0 │   , │   . │   + ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛

        partial alphanumeric_keys modifier_keys
        xkb_symbols "lafayette" {
            name[group1]= "French (Qwerty-Lafayette)";
            key.type[group1] = "EIGHT_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , U201E           , exclamdown      , exclam          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 1 ! „ ¡ !
            key <AE02> {[ 2               , at              , U201C           , U2018           , parenleft       , U207D           , VoidSymbol      , VoidSymbol      ]}; // 2 @ “ ‘ ( ⁽
            key <AE03> {[ 3               , numbersign      , U201D           , U2019           , parenright      , U207E           , VoidSymbol      , VoidSymbol      ]}; // 3 # ” ’ ) ⁾
            key <AE04> {[ 4               , dollar          , sterling        , cent            , apostrophe      , dead_acute      , VoidSymbol      , VoidSymbol      ]}; // 4 $ £ ¢ ' ´
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           , quotedbl        , dead_diaeresis  , VoidSymbol      , VoidSymbol      ]}; // 5 % € ‰ " ¨
            key <AE06> {[ 6               , asciicircum     , currency        , VoidSymbol      , dead_currency   , dead_circumflex , VoidSymbol      , VoidSymbol      ]}; // 6 ^ ¤   ¤ ^
            key <AE07> {[ 7               , ampersand       , VoidSymbol      , VoidSymbol      , 7               , U2077           , VoidSymbol      , VoidSymbol      ]}; // 7 &     7 ⁷
            key <AE08> {[ 8               , asterisk        , section         , U2605           , 8               , U2078           , VoidSymbol      , VoidSymbol      ]}; // 8 * § ★ 8 ⁸
            key <AE09> {[ 9               , parenleft       , paragraph       , VoidSymbol      , 9               , U2079           , VoidSymbol      , VoidSymbol      ]}; // 9 ( ¶   9 ⁹
            key <AE10> {[ 0               , parenright      , degree          , VoidSymbol      , slash           , division        , VoidSymbol      , VoidSymbol      ]}; // 0 ) °   / ÷

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              , equal           , notequal        , VoidSymbol      , VoidSymbol      ]}; // q Q æ Æ = ≠
            key <AD02> {[ w               , W               , eacute          , Eacute          , less            , lessthanequal   , VoidSymbol      , VoidSymbol      ]}; // w W é É < ≤
            key <AD03> {[ e               , E               , egrave          , Egrave          , greater         , greaterthanequal, VoidSymbol      , VoidSymbol      ]}; // e E è È > ≥
            key <AD04> {[ r               , R               , registered      , trademark       , minus           , emdash          , VoidSymbol      , VoidSymbol      ]}; // r R ® ™ - —
            key <AD05> {[ t               , T               , thorn           , Thorn           , plus            , plusminus       , VoidSymbol      , VoidSymbol      ]}; // t T þ Þ + ±
            key <AD06> {[ y               , Y               , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // y Y
            key <AD07> {[ u               , U               , ugrave          , Ugrave          , 4               , U2074           , VoidSymbol      , VoidSymbol      ]}; // u U ù Ù 4 ⁴
            key <AD08> {[ i               , I               , U0133           , U0132           , 5               , U2075           , VoidSymbol      , VoidSymbol      ]}; // i I ĳ Ĳ 5 ⁵
            key <AD09> {[ o               , O               , oe              , OE              , 6               , U2076           , VoidSymbol      , VoidSymbol      ]}; // o O œ Œ 6 ⁶
            key <AD10> {[ p               , P               , VoidSymbol      , VoidSymbol      , asterisk        , multiply        , VoidSymbol      , VoidSymbol      ]}; // p P     * ×

            // Letters, second row
            key <AC01> {[ a               , A               , agrave          , Agrave          , braceleft       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // a A à À {
            key <AC02> {[ s               , S               , ssharp          , U1E9E           , bracketleft     , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // s S ß ẞ [
            key <AC03> {[ d               , D               , eth             , Eth             , bracketright    , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // d D ð Ð ]
            key <AC04> {[ f               , F               , U017F           , ordfeminine     , braceright      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // f F ſ ª }
            key <AC05> {[ g               , G               , copyright       , VoidSymbol      , slash           , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // g G ©   /
            key <AC06> {[ h               , H               , leftarrow       , U21D0           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // h H ← ⇐
            key <AC07> {[ j               , J               , downarrow       , U21D3           , 1               , onesuperior     , VoidSymbol      , VoidSymbol      ]}; // j J ↓ ⇓ 1 ¹
            key <AC08> {[ k               , K               , uparrow         , U21D1           , 2               , twosuperior     , VoidSymbol      , VoidSymbol      ]}; // k K ↑ ⇑ 2 ²
            key <AC09> {[ l               , L               , rightarrow      , U21D2           , 3               , threesuperior   , VoidSymbol      , VoidSymbol      ]}; // l L → ⇒ 3 ³
            key <AC10> {[ ISO_Level3_Latch, ISO_Level3_Latch, grave           , VoidSymbol      , minus           , U2212           , VoidSymbol      , VoidSymbol      ]}; // ` ` `   - −

            // Letters, third row
            key <AB01> {[ z               , Z               , VoidSymbol      , VoidSymbol      , asciitilde      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // z Z     ~ ~
            key <AB02> {[ x               , X               , multiply        , VoidSymbol      , grave           , dead_grave      , VoidSymbol      , VoidSymbol      ]}; // x X ×   ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        , bar             , brokenbar       , VoidSymbol      , VoidSymbol      ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , ubreve          , Ubreve          , underscore      , endash          , VoidSymbol      , VoidSymbol      ]}; // v V ŭ Ŭ _ –
            key <AB05> {[ b               , B               , dagger          , doubledagger    , backslash       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // b B † ‡ \ 
            key <AB06> {[ n               , N               , ntilde          , Ntilde          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ
            key <AB07> {[ m               , M               , mu              , masculine       , 0               , U2070           , VoidSymbol      , VoidSymbol      ]}; // m M µ º 0 ⁰
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           , comma           , dead_cedilla    , VoidSymbol      , VoidSymbol      ]}; // , ; · • , ¸
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      , period          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // . : …   .
            key <AB10> {[ slash           , question        , division        , questiondown    , plus            , notsign         , VoidSymbol      , VoidSymbol      ]}; // / ? ÷ ¿ + ¬

            // Pinky keys
            key <AE11> {[ minus           , underscore      , emdash          , endash          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AE13> {[ VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; //
            key <AD11> {[ dead_circumflex , guillemotleft   , VoidSymbol      , VoidSymbol      , dead_caron      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ^ «     ˇ
            key <AD12> {[ dead_diaeresis  , guillemotright  , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ¨ »
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      , dead_acute      , dead_abovedot   , VoidSymbol      , VoidSymbol      ]}; // ' "     ´ ˙
            key <AB11> {[ VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; //
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      , dead_grave      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // ` ~     ` ~
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , lessthanequal   , greaterthanequal, VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // < > ≤ ≥

            // Space bar
            key <SPCE> {[ space           , U202F           , U2019           , U2019           , space           , nobreakspace    , VoidSymbol      , VoidSymbol      ]}; //     ’ ’

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key:
            // this is the only way to have a multi-purpose dead key with XKB.
            // The real AltGr key is an ISO_Level5_Switch.
            include "level5(ralt_switch)"
        };""")
}, {
    'meta': {
        'locale': LOCALE,
        'variant': 'lafayette42',
        'description': 'French (Qwerty-Lafayette, compact variant)',
    },
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.8.0
        // Last change   : 2023-01-17
        // License       : WTFPL - Do What The Fuck You Want Public License
        //
        // French (Qwerty-Lafayette, compact variant)
        //
        // Base layer + dead key
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │ ~   │ ! „ │ @ “ │ # ” │ $ ¢ │ % ‰ │ ^   │ &   │ *   │ (   │ )   │ _ – │ + ± ┃          ┃
        // │ `   │ 1 ¡ │ 2 « │ 3 » │ 4 £ │ 5 € │ 6 ¥ │ 7 ¤ │ 8 § │ 9 ¶ │ 0 ° │ - — │ = ≠ ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃ Q   │ W   │ E   │ R   │ T   │ Y   │ U   │ I   │ O   │ P   │ {   │ }   ┃       ┃
        // ┃ ↹      ┃   æ │   é │   è │   ® │   ™ │     │   ù │   ĳ │   œ │     │ [   │ ]   ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃ A   │ S   │ D   │ F ª │ G   │ H   │ J   │ K   │ L   │*¨   │ "   │ |   ┃      ┃
        // ┃ ⇬       ┃   à │   ß │   ê │   ſ │   © │   ŷ │   û │   î │   ô │** ` │ '   │ \\   ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃ >   │ Z   │ X   │ C   │ V   │ B   │ N   │ M º │ ; • │ :   │ ? ÷ ┃               ┃
        // ┃ ⇧    ┃ <   │   â │   × │   ç │   ŭ │   † │   ñ │   µ │ , · │ . … │ / ¿ ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
        //
        // AltGr layer
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │     │     │     │     │     │     │     │     │     │     │     │     │     ┃          ┃
        // │     │     │     │     │     │     │     │     │     │     │     │     │     ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃     │     │     │     │   ‰ │  *^ │     │   × │  *´ │     │     │     ┃       ┃
        // ┃ ↹      ┃   1 │   [ │   ] │   $ │   % │   ^ │   & │   * │   ' │   0 │     │     ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃     │   ⁽ │   ⁾ │     │   ≠ │   ± │   — │     │     │  *¨ │     │     ┃      ┃
        // ┃ ⇬       ┃   { │   ( │   ) │   } │   = │   + │   - │   < │   > │   " │     │     ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃     │  *~ │  *` │     │   – │   ÷ │     │     │  *¸ │   ¬ │     ┃               ┃
        // ┃ ⇧    ┃     │   ~ │   ` │   | │   _ │   / │   \\ │   @ │   # │   ! │   ? ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛

        partial alphanumeric_keys modifier_keys
        xkb_symbols "lafayette42" {
            name[group1]= "French (Qwerty-Lafayette, compact variant)";
            key.type[group1] = "EIGHT_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , exclamdown      , U201E           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 1 ! ¡ „
            key <AE02> {[ 2               , at              , guillemotleft   , U201C           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 2 @ « “
            key <AE03> {[ 3               , numbersign      , guillemotright  , U201D           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 3 # » ”
            key <AE04> {[ 4               , dollar          , sterling        , cent            , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 4 $ £ ¢
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 5 % € ‰
            key <AE06> {[ 6               , asciicircum     , yen             , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 6 ^ ¥
            key <AE07> {[ 7               , ampersand       , currency        , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 7 & ¤
            key <AE08> {[ 8               , asterisk        , section         , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 8 * §
            key <AE09> {[ 9               , parenleft       , paragraph       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 9 ( ¶
            key <AE10> {[ 0               , parenright      , degree          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 0 ) °

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              , 1               , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // q Q æ Æ 1
            key <AD02> {[ w               , W               , eacute          , Eacute          , bracketleft     , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // w W é É [
            key <AD03> {[ e               , E               , egrave          , Egrave          , bracketright    , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // e E è È ]
            key <AD04> {[ r               , R               , registered      , VoidSymbol      , dollar          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // r R ®   $
            key <AD05> {[ t               , T               , trademark       , VoidSymbol      , percent         , U2030           , VoidSymbol      , VoidSymbol      ]}; // t T ™   % ‰
            key <AD06> {[ y               , Y               , VoidSymbol      , VoidSymbol      , asciicircum     , dead_circumflex , VoidSymbol      , VoidSymbol      ]}; // y Y     ^ ^
            key <AD07> {[ u               , U               , ugrave          , Ugrave          , ampersand       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // u U ù Ù &
            key <AD08> {[ i               , I               , U0133           , U0132           , asterisk        , multiply        , VoidSymbol      , VoidSymbol      ]}; // i I ĳ Ĳ * ×
            key <AD09> {[ o               , O               , oe              , OE              , apostrophe      , dead_acute      , VoidSymbol      , VoidSymbol      ]}; // o O œ Œ ' ´
            key <AD10> {[ p               , P               , VoidSymbol      , VoidSymbol      , 0               , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // p P     0

            // Letters, second row
            key <AC01> {[ a               , A               , agrave          , Agrave          , braceleft       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // a A à À {
            key <AC02> {[ s               , S               , ssharp          , U1E9E           , parenleft       , U207D           , VoidSymbol      , VoidSymbol      ]}; // s S ß ẞ ( ⁽
            key <AC03> {[ d               , D               , ecircumflex     , Ecircumflex     , parenright      , U207E           , VoidSymbol      , VoidSymbol      ]}; // d D ê Ê ) ⁾
            key <AC04> {[ f               , F               , U017F           , ordfeminine     , braceright      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // f F ſ ª }
            key <AC05> {[ g               , G               , copyright       , VoidSymbol      , equal           , notequal        , VoidSymbol      , VoidSymbol      ]}; // g G ©   = ≠
            key <AC06> {[ h               , H               , U0177           , U0176           , plus            , plusminus       , VoidSymbol      , VoidSymbol      ]}; // h H ŷ Ŷ + ±
            key <AC07> {[ j               , J               , ucircumflex     , Ucircumflex     , minus           , emdash          , VoidSymbol      , VoidSymbol      ]}; // j J û Û - —
            key <AC08> {[ k               , K               , icircumflex     , Icircumflex     , less            , lessthanequal   , VoidSymbol      , VoidSymbol      ]}; // k K î Î < ≤
            key <AC09> {[ l               , L               , ocircumflex     , Ocircumflex     , greater         , greaterthanequal, VoidSymbol      , VoidSymbol      ]}; // l L ô Ô > ≥
            key <AC10> {[ ISO_Level3_Latch, dead_diaeresis  , grave           , VoidSymbol      , quotedbl        , dead_diaeresis  , VoidSymbol      , VoidSymbol      ]}; // ` ¨ `   " ¨

            // Letters, third row
            key <AB01> {[ z               , Z               , acircumflex     , Acircumflex     , asciitilde      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // z Z â Â ~ ~
            key <AB02> {[ x               , X               , multiply        , VoidSymbol      , grave           , dead_grave      , VoidSymbol      , VoidSymbol      ]}; // x X ×   ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        , bar             , brokenbar       , VoidSymbol      , VoidSymbol      ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , ubreve          , Ubreve          , underscore      , endash          , VoidSymbol      , VoidSymbol      ]}; // v V ŭ Ŭ _ –
            key <AB05> {[ b               , B               , dagger          , doubledagger    , slash           , division        , VoidSymbol      , VoidSymbol      ]}; // b B † ‡ / ÷
            key <AB06> {[ n               , N               , ntilde          , Ntilde          , backslash       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ \ 
            key <AB07> {[ m               , M               , mu              , masculine       , at              , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // m M µ º @
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           , numbersign      , dead_cedilla    , VoidSymbol      , VoidSymbol      ]}; // , ; · • # ¸
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      , exclam          , notsign         , VoidSymbol      , VoidSymbol      ]}; // . : …   ! ¬
            key <AB10> {[ slash           , question        , questiondown    , division        , question        , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // / ? ¿ ÷ ?

            // Pinky keys
            key <AE11> {[ minus           , underscore      , emdash          , endash          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AE13> {[ VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; //
            key <AD11> {[ bracketleft     , braceleft       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // [ {
            key <AD12> {[ bracketright    , braceright      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ] }
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ' "
            key <AB11> {[ VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; //
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ` ~
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // < >

            // Space bar
            key <SPCE> {[ space           , U202F           , U2019           , U2019           , space           , nobreakspace    , VoidSymbol      , VoidSymbol      ]}; //     ’ ’

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key:
            // this is the only way to have a multi-purpose dead key with XKB.
            // The real AltGr key is an ISO_Level5_Switch.
            include "level5(ralt_switch)"
        };""")
}]

class KeyboardLayout:  # fake kalamine KeyboardLayout object
    def __init__(self, data):
        self.meta = data['meta']
        self.xkb_patch = data['symbols']

xkb = XKBManager()
xkb.remove('fr/lafayette')
xkb.remove('fr/lafayette42')
for layout_data in LAYOUTS:
    xkb.add(KeyboardLayout(layout_data))
xkb.update()

print()
print('Installed layouts:')
for layout_data in LAYOUTS:
    meta = layout_data['meta']
    name = f"{meta['locale']}/{meta['variant']}"
    print(f"{name:<24} {meta['description']}")
