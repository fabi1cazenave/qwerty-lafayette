#!/usr/bin/env python3
import glob
import os
import re
from lxml import etree

XKB = '/usr/share/X11/xkb/'

NAME = 'lafayette'


###############################################################################
# XKB/symbols: remove custom layouts
#    // [NAME]::BEGIN
#    xkb_symbols "lafayette"   { ... }
#    xkb_symbols "lafayette42" { ... }
#    // [NAME]::END

MARK_BEGIN = NAME.upper() + '::BEGIN\n'
MARK_END = NAME.upper() + '::END\n'

pattern = re.compile("^[a-z][a-z]$")

for path in glob.glob(os.path.join(XKB, 'symbols/??')):
    text = ''
    between_marks = False
    modified_text = False
    with open(path, 'r+') as symbols:
        for line in symbols:
            if line.endswith(MARK_BEGIN):
                between_marks = True
                modified_text = True
            elif line.endswith(MARK_END):
                between_marks = False
            elif not between_marks:
                text += line
        if modified_text:  # clear previous 'lafayette' layouts
            print('resetting: ' + path)
            symbols.seek(0)
            symbols.write(text)
            symbols.truncate()


###############################################################################
# XKB/rules: remove layout references in {base,evdev}.xml
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

    # remove existing "lafayette" layout references, if any
    variantList = tree.xpath('//variant[@type="' + NAME + '"]')
    if len(variantList) > 0:
        for variant in variantList:
            variant.getparent().remove(variant)
        print('resetting: ' + path)
        tree.write(path,
                   pretty_print=True, xml_declaration=True, encoding='utf-8')
