#!/usr/bin/env python3
import os
import shutil  # backups...
from lxml import etree
from lxml.builder import E

XKB = '/usr/share/X11/xkb/'

NAME = 'lafayette'
LAYOUTS = {
    'fr': [
        {
            'name': 'lafayette',
            'desc': 'French (Qwerty-Lafayette)',
            'symbols': ''
        },
        {
            'name': 'lafayette42',
            'desc': 'French (Qwerty-Lafayette, compact variant)',
            'symbols': ''
        }
    ]
}

# load XKB snippets (symbols) if not already included in LAYOUTS
for locale, layouts in LAYOUTS.items():
    for info in layouts:
        if len(info['symbols']) == 0:
            with open('dist/xkb/' + locale + '/' + info['name']) as infile:
                info['symbols'] = '\n'
                for line in infile:
                    # filter out Vim modelines
                    if not line.startswith('// vim:'):
                        info['symbols'] += line
                infile.close()


###############################################################################
# XKB/symbols: append new layouts
#    // [NAME]::BEGIN
#    xkb_symbols "lafayette"   { ... }
#    xkb_symbols "lafayette42" { ... }
#    // [NAME]::END

MARK_BEGIN = NAME.upper() + '::BEGIN\n'
MARK_END = NAME.upper() + '::END\n'

for locale, layouts in LAYOUTS.items():
    path = os.path.join(XKB, 'symbols', locale)

    # backup, just in case :-)
    if not os.path.isfile(path + '.orig'):
        shutil.copy(path, path + '.orig')

    # update XKB/symbols/[locale]
    text = ''
    between_marks = False
    modified_text = False
    with open(path, 'r+') as symbols:
        # load system symbols without any previous 'lafayette' layouts
        for line in symbols:
            if line.endswith(MARK_BEGIN):
                between_marks = True
                modified_text = True
            elif line.endswith(MARK_END):
                between_marks = False
            elif not between_marks:
                text += line
        if modified_text:  # clear previous 'lafayette' layouts
            symbols.seek(0)
            symbols.write(text)
            symbols.truncate()

        # append our additional symbols
        symbols.write('// ' + MARK_BEGIN)
        for info in layouts:
            symbols.write('\n')
            symbols.write(info['symbols'])
        symbols.write('\n')
        symbols.write('// ' + MARK_END)
        symbols.close()


###############################################################################
# XKB/rules: update layout references in {base,evdev}.xml
#   <variant type="lafayette">
#       <configItem>
#           <name>lafayette42</name>
#           <description>French (Qwerty-Lafayette)</description>
#       </configItem>
#   </variant>

PARSER = etree.XMLParser(remove_blank_text=True)
for filename in ['base.xml', 'evdev.xml']:
    path = os.path.join(XKB, 'rules', filename)
    tree = etree.parse(path, PARSER)

    # backup, just in case :-)
    if not os.path.isfile(path + '.orig'):
        shutil.copy(path, path + '.orig')

    # remove existing "lafayette" layout references, if any
    for variant in tree.xpath('//variant[@type="' + NAME + '"]'):
        variant.getparent().remove(variant)

    # add new layout references to XKB/rules/{base,evdev}.xml
    for locale, layouts in LAYOUTS.items():
        variantList = tree.xpath('//layout/configItem/name[text()="' +
                                 locale + '"]/../../variantList')[0]
        for info in layouts:
            variantList.append(
                E.variant(
                    E.configItem(
                        E.name(info['name']),
                        E.description(info['desc'])
                    ), type=NAME
                )
            )

    # update the file
    tree.write(path, pretty_print=True, xml_declaration=True, encoding='utf-8')
