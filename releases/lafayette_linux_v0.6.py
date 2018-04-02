#!/usr/bin/env python3
import os
import shutil    # backups...
import textwrap  # dedent hard-coded symbol strings
from lxml import etree
from lxml.builder import E

XKB = '/usr/share/X11/xkb/'
NAME = 'lafayette'
LAYOUTS = {'fr': [{
    'name': 'lafayette',
    'desc': 'French (Qwerty-Lafayette)',
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.6.0
        // Last change   : 2018-04-02
        // License       : WTFPL - Do What The Fuck You Want Public License
        //
        // French (Qwerty-Lafayette)
        //
        // Base layer + dead key
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │ ~   │ ! ¡ │ @ ‘ │ # ’ │ $ ¢ │ % ‰ │ ^   │ &   │ * ★ │ (   │ )   │ _ – │ + ± ┃          ┃
        // │ `   │ 1 „ │ 2 “ │ 3 ” │ 4 £ │ 5 € │ 6   │ 7 | │ 8 ∞ │ 9   │ 0 ° │ - — │ = ≠ ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃ Q   │ W   │ E   │ R ™ │ T   │ Y ¤ │ U   │ I   │ O   │ P ¶ │ « { │ » } ┃       ┃
        // ┃ ↹      ┃   æ │   é │   è │   ® │   þ │   ¥ │   ù │   ĳ │   œ │   § │  ̂ [ │  ̈ ] ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃ A   │ S   │ D   │ F ª │ G   │ H   │ J   │ K   │ L   │  ⃡   │ "   │ |   ┃      ┃
        // ┃ ⇬       ┃   à │   ß │   ð │   ſ │   © │   ← │   ↓ │   ↑ │   → │  ⃡ ` │ '   │ \   ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃ > ≥ │ Z   │ X   │ C   │ V   │ B   │ N   │ M º │ ; • │ :   │ ? ¿ ┃               ┃
        // ┃ ⇧    ┃ < ≤ │   < │   > │   ç │   ŭ │   † │   ñ │   µ │ , · │ . … │ / \ ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
        //
        // AltGr layer
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │    ̃ │     │   « │   » │    ́ │    ̈ │    ̂ │   ⁷ │   ⁸ │   ⁹ │   ÷ │     │     ┃          ┃
        // │    ̀ │   ! │   ( │   ) │   ' │   " │   ^ │   7 │   8 │   9 │   / │     │     ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃   ≠ │     │     │   — │   ± │     │   ⁴ │   ⁵ │   ⁶ │   × │     │     ┃       ┃
        // ┃ ↹      ┃   = │   < │   > │   - │   + │     │   4 │   5 │   6 │   * │     │     ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃     │     │     │     │     │     │   ¹ │   ² │   ³ │   − │    ̇ │     ┃      ┃
        // ┃ ⇬       ┃   { │   [ │   ] │   } │   / │     │   1 │   2 │   3 │   - │    ́ │     ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃     │    ̃ │    ̀ │     │   – │     │     │   ⁰ │     │     │   ¬ ┃               ┃
        // ┃ ⇧    ┃     │   ~ │   ` │   | │   _ │   \ │     │   0 │   , │   . │   + ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛

        partial alphanumeric_keys modifier_keys
        xkb_symbols "lafayette" {
            include "pc"

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key.
            // This is the only way to have a multi-purpose dead key with XKB.

            // The real AltGr key should be an ISO_Level5_Switch; however,
            // ISO_Level5_Switch does not work as expected when applying this layout
            // with xkbcomp, so let’s use two groups instead and make the AltGr key a
            // group selector.

            name[group1]= "French (Qwerty-Lafayette)";
            name[group2]= "AltGr";

            key.type[group1] = "FOUR_LEVEL";
            key.type[group2] = "TWO_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , U201E           , exclamdown      ],[ exclam          , VoidSymbol      ]}; // 1 ! „ ¡ !
            key <AE02> {[ 2               , at              , U201C           , U2018           ],[ parenleft       , guillemotleft   ]}; // 2 @ “ ‘ ( «
            key <AE03> {[ 3               , numbersign      , U201D           , U2019           ],[ parenright      , guillemotright  ]}; // 3 # ” ’ ) »
            key <AE04> {[ 4               , dollar          , sterling        , cent            ],[ apostrophe      , dead_acute      ]}; // 4 $ £ ¢ ' ´
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           ],[ quotedbl        , dead_diaeresis  ]}; // 5 % € ‰ " ¨
            key <AE06> {[ 6               , asciicircum     , VoidSymbol      , VoidSymbol      ],[ asciicircum     , dead_circumflex ]}; // 6 ^     ^ ^
            key <AE07> {[ 7               , ampersand       , bar             , brokenbar       ],[ 7               , U2077           ]}; // 7 & | ¦ 7 ⁷
            key <AE08> {[ 8               , asterisk        , infinity        , U2605           ],[ 8               , U2078           ]}; // 8 * ∞ ★ 8 ⁸
            key <AE09> {[ 9               , parenleft       , VoidSymbol      , VoidSymbol      ],[ 9               , U2079           ]}; // 9 (     9 ⁹
            key <AE10> {[ 0               , parenright      , degree          , VoidSymbol      ],[ slash           , division        ]}; // 0 ) °   / ÷

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              ],[ equal           , notequal        ]}; // q Q æ Æ = ≠
            key <AD02> {[ w               , W               , eacute          , Eacute          ],[ less            , lessthanequal   ]}; // w W é É < ≤
            key <AD03> {[ e               , E               , egrave          , Egrave          ],[ greater         , greaterthanequal]}; // e E è È > ≥
            key <AD04> {[ r               , R               , registered      , trademark       ],[ minus           , emdash          ]}; // r R ® ™ - —
            key <AD05> {[ t               , T               , thorn           , Thorn           ],[ plus            , plusminus       ]}; // t T þ Þ + ±
            key <AD06> {[ y               , Y               , yen             , currency        ],[ VoidSymbol      , VoidSymbol      ]}; // y Y ¥ ¤
            key <AD07> {[ u               , U               , ugrave          , Ugrave          ],[ 4               , U2074           ]}; // u U ù Ù 4 ⁴
            key <AD08> {[ i               , I               , U0133           , U0132           ],[ 5               , U2075           ]}; // i I ĳ Ĳ 5 ⁵
            key <AD09> {[ o               , O               , oe              , OE              ],[ 6               , U2076           ]}; // o O œ Œ 6 ⁶
            key <AD10> {[ p               , P               , section         , paragraph       ],[ asterisk        , multiply        ]}; // p P § ¶ * ×

            // Letters, second row
            key <AC01> {[ a               , A               , agrave          , Agrave          ],[ braceleft       , VoidSymbol      ]}; // a A à À {
            key <AC02> {[ s               , S               , ssharp          , U1E9E           ],[ bracketleft     , VoidSymbol      ]}; // s S ß ẞ [
            key <AC03> {[ d               , D               , eth             , Eth             ],[ bracketright    , VoidSymbol      ]}; // d D ð Ð ]
            key <AC04> {[ f               , F               , U017F           , ordfeminine     ],[ braceright      , VoidSymbol      ]}; // f F ſ ª }
            key <AC05> {[ g               , G               , copyright       , VoidSymbol      ],[ slash           , VoidSymbol      ]}; // g G ©   /
            key <AC06> {[ h               , H               , leftarrow       , U21D0           ],[ VoidSymbol      , VoidSymbol      ]}; // h H ← ⇐
            key <AC07> {[ j               , J               , downarrow       , U21D3           ],[ 1               , onesuperior     ]}; // j J ↓ ⇓ 1 ¹
            key <AC08> {[ k               , K               , uparrow         , U21D1           ],[ 2               , twosuperior     ]}; // k K ↑ ⇑ 2 ²
            key <AC09> {[ l               , L               , rightarrow      , U21D2           ],[ 3               , threesuperior   ]}; // l L → ⇒ 3 ³
            key <AC10> {[ ISO_Level3_Latch, ISO_Level3_Latch, grave           , VoidSymbol      ],[ minus           , U2212           ]}; // ` ` `   - −

            // Letters, third row
            key <AB01> {[ z               , Z               , less            , lessthanequal   ],[ asciitilde      , dead_tilde      ]}; // z Z < ≤ ~ ~
            key <AB02> {[ x               , X               , greater         , greaterthanequal],[ grave           , dead_grave      ]}; // x X > ≥ ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        ],[ bar             , brokenbar       ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , ubreve          , Ubreve          ],[ underscore      , endash          ]}; // v V ŭ Ŭ _ –
            key <AB05> {[ b               , B               , dagger          , doubledagger    ],[ backslash       , VoidSymbol      ]}; // b B † ‡ \
            key <AB06> {[ n               , N               , ntilde          , Ntilde          ],[ VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ
            key <AB07> {[ m               , M               , mu              , masculine       ],[ 0               , U2070           ]}; // m M µ º 0 ⁰
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           ],[ comma           , VoidSymbol      ]}; // , ; · • ,
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      ],[ period          , VoidSymbol      ]}; // . : …   .
            key <AB10> {[ slash           , question        , backslash       , questiondown    ],[ plus            , notsign         ]}; // / ? \ ¿ + ¬

            // Pinky keys
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      ],[ dead_grave      , dead_tilde      ]}; // ` ~     ` ~
            key <AE11> {[ minus           , underscore      , emdash          , endash          ],[ VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       ],[ VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AD11> {[ dead_circumflex , guillemotleft   , bracketleft     , braceleft       ],[ VoidSymbol      , VoidSymbol      ]}; // ^ « [ {
            key <AD12> {[ dead_diaeresis  , guillemotright  , bracketright    , braceright      ],[ VoidSymbol      , VoidSymbol      ]}; // ¨ » ] }
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      ],[ dead_acute      , dead_abovedot   ]}; // ' "     ´ ˙
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      ],[ VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , lessthanequal   , greaterthanequal],[ VoidSymbol      , VoidSymbol      ]}; // < > ≤ ≥

            // Space bar
            key <SPCE> {[ space           , nobreakspace    , U2019           , U2019           ],[ nobreakspace    , U202F           ]}; //     ’ ’

            // AltGr
            // Note: the `ISO_Level5_Latch` here is meaningless but helps with Chromium.
            key <RALT> {
                type = "TWO_LEVEL",
                symbols = [ ISO_Level5_Latch, ISO_Level5_Latch ],
                actions = [ SetGroup(group=2), SetGroup(group=2) ]
            };
        };""")
}, {
    'name': 'lafayette42',
    'desc': 'French (Qwerty-Lafayette, compact variant)',
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.6.0
        // Last change   : 2018-04-02
        // License       : WTFPL - Do What The Fuck You Want Public License
        //
        // French (Qwerty-Lafayette, compact variant)
        //
        // Base layer + dead key
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │ ~   │ ! ¡ │ @ ‘ │ # ’ │ $ ¢ │ % ‰ │ ^ ¤ │ &   │ *   │ «   │ »   │ _ – │ + ± ┃          ┃
        // │ `   │ 1 „ │ 2 “ │ 3 ” │ 4 £ │ 5 € │ 6 ¥ │ 7   │ 8 § │ 9 ¶ │ 0 ° │ - — │ = ≠ ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃ Q   │ W   │ E   │ R   │ T   │ Y   │ U   │ I   │ O   │ P   │ {   │ }   ┃       ┃
        // ┃ ↹      ┃   æ │   é │   è │   ® │   ™ │     │   ù │   ĳ │   œ │     │ [ < │ ] > ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃ A   │ S   │ D   │ F ª │ G   │ H   │ J   │ K   │ L   │  ̈   │ "   │ |   ┃      ┃
        // ┃ ⇬       ┃   à │   ß │   ê │   ſ │   © │   ŷ │   û │   î │   ô │  ⃡ ` │ '   │ \   ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃ >   │ Z   │ X   │ C   │ V   │ B   │ N   │ M º │ ; • │ :   │ ? ¿ ┃               ┃
        // ┃ ⇧    ┃ <   │   â │     │   ç │     │     │   ñ │   µ │ , · │ . … │ / \ ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
        //
        // AltGr layer
        // ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
        // │    ̃ │     │   « │   » │    ́ │    ̈ │    ̂ │   ⁷ │   ⁸ │   ⁹ │   ÷ │     │     ┃          ┃
        // │    ̀ │   ! │   ( │   ) │   ' │   " │   ^ │   7 │   8 │   9 │   / │     │     ┃ ⌫        ┃
        // ┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
        // ┃        ┃   ≠ │     │     │   — │   ± │     │   ⁴ │   ⁵ │   ⁶ │   × │     │     ┃       ┃
        // ┃ ↹      ┃   = │   < │   > │   - │   + │     │   4 │   5 │   6 │   * │     │     ┃       ┃
        // ┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
        // ┃         ┃     │     │     │     │     │     │   ¹ │   ² │   ³ │   − │     │     ┃      ┃
        // ┃ ⇬       ┃   { │   [ │   ] │   } │   / │     │   1 │   2 │   3 │   - │    ́ │     ┃      ┃
        // ┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
        // ┃      ┃     │    ̃ │    ̀ │     │   – │     │     │   ⁰ │    ̧ │     │   ¬ ┃               ┃
        // ┃ ⇧    ┃     │   ~ │   ` │   | │   _ │   \ │     │   0 │   , │   . │   + ┃ ⇧             ┃
        // ┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
        // ┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
        // ┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                              ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
        // ┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛

        partial alphanumeric_keys modifier_keys
        xkb_symbols "lafayette42" {
            include "pc"

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key.
            // This is the only way to have a multi-purpose dead key with XKB.

            // The real AltGr key should be an ISO_Level5_Switch; however,
            // ISO_Level5_Switch does not work as expected when applying this layout
            // with xkbcomp, so let’s use two groups instead and make the AltGr key a
            // group selector.

            name[group1]= "French (Qwerty-Lafayette, compact variant)";
            name[group2]= "AltGr";

            key.type[group1] = "FOUR_LEVEL";
            key.type[group2] = "TWO_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , U201E           , exclamdown      ],[ exclam          , VoidSymbol      ]}; // 1 ! „ ¡ !
            key <AE02> {[ 2               , at              , U201C           , U2018           ],[ parenleft       , guillemotleft   ]}; // 2 @ “ ‘ ( «
            key <AE03> {[ 3               , numbersign      , U201D           , U2019           ],[ parenright      , guillemotright  ]}; // 3 # ” ’ ) »
            key <AE04> {[ 4               , dollar          , sterling        , cent            ],[ apostrophe      , dead_acute      ]}; // 4 $ £ ¢ ' ´
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           ],[ quotedbl        , dead_diaeresis  ]}; // 5 % € ‰ " ¨
            key <AE06> {[ 6               , asciicircum     , yen             , currency        ],[ asciicircum     , dead_circumflex ]}; // 6 ^ ¥ ¤ ^ ^
            key <AE07> {[ 7               , ampersand       , VoidSymbol      , VoidSymbol      ],[ 7               , U2077           ]}; // 7 &     7 ⁷
            key <AE08> {[ 8               , asterisk        , section         , VoidSymbol      ],[ 8               , U2078           ]}; // 8 * §   8 ⁸
            key <AE09> {[ 9               , guillemotleft   , paragraph       , VoidSymbol      ],[ 9               , U2079           ]}; // 9 « ¶   9 ⁹
            key <AE10> {[ 0               , guillemotright  , degree          , VoidSymbol      ],[ slash           , division        ]}; // 0 » °   / ÷

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              ],[ equal           , notequal        ]}; // q Q æ Æ = ≠
            key <AD02> {[ w               , W               , eacute          , Eacute          ],[ less            , lessthanequal   ]}; // w W é É < ≤
            key <AD03> {[ e               , E               , egrave          , Egrave          ],[ greater         , greaterthanequal]}; // e E è È > ≥
            key <AD04> {[ r               , R               , registered      , VoidSymbol      ],[ minus           , emdash          ]}; // r R ®   - —
            key <AD05> {[ t               , T               , trademark       , VoidSymbol      ],[ plus            , plusminus       ]}; // t T ™   + ±
            key <AD06> {[ y               , Y               , VoidSymbol      , VoidSymbol      ],[ VoidSymbol      , VoidSymbol      ]}; // y Y
            key <AD07> {[ u               , U               , ugrave          , Ugrave          ],[ 4               , U2074           ]}; // u U ù Ù 4 ⁴
            key <AD08> {[ i               , I               , U0133           , U0132           ],[ 5               , U2075           ]}; // i I ĳ Ĳ 5 ⁵
            key <AD09> {[ o               , O               , oe              , OE              ],[ 6               , U2076           ]}; // o O œ Œ 6 ⁶
            key <AD10> {[ p               , P               , VoidSymbol      , VoidSymbol      ],[ asterisk        , multiply        ]}; // p P     * ×

            // Letters, second row
            key <AC01> {[ a               , A               , agrave          , Agrave          ],[ braceleft       , VoidSymbol      ]}; // a A à À {
            key <AC02> {[ s               , S               , ssharp          , U1E9E           ],[ bracketleft     , VoidSymbol      ]}; // s S ß ẞ [
            key <AC03> {[ d               , D               , ecircumflex     , Ecircumflex     ],[ bracketright    , VoidSymbol      ]}; // d D ê Ê ]
            key <AC04> {[ f               , F               , U017F           , ordfeminine     ],[ braceright      , VoidSymbol      ]}; // f F ſ ª }
            key <AC05> {[ g               , G               , copyright       , VoidSymbol      ],[ slash           , VoidSymbol      ]}; // g G ©   /
            key <AC06> {[ h               , H               , U0177           , U0176           ],[ VoidSymbol      , VoidSymbol      ]}; // h H ŷ Ŷ
            key <AC07> {[ j               , J               , ucircumflex     , Ucircumflex     ],[ 1               , onesuperior     ]}; // j J û Û 1 ¹
            key <AC08> {[ k               , K               , icircumflex     , Icircumflex     ],[ 2               , twosuperior     ]}; // k K î Î 2 ²
            key <AC09> {[ l               , L               , ocircumflex     , Ocircumflex     ],[ 3               , threesuperior   ]}; // l L ô Ô 3 ³
            key <AC10> {[ ISO_Level3_Latch, dead_diaeresis  , grave           , VoidSymbol      ],[ minus           , U2212           ]}; // ` ¨ `   - −

            // Letters, third row
            key <AB01> {[ z               , Z               , acircumflex     , Acircumflex     ],[ asciitilde      , dead_tilde      ]}; // z Z â Â ~ ~
            key <AB02> {[ x               , X               , VoidSymbol      , VoidSymbol      ],[ grave           , dead_grave      ]}; // x X     ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        ],[ bar             , brokenbar       ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , VoidSymbol      , VoidSymbol      ],[ underscore      , endash          ]}; // v V     _ –
            key <AB05> {[ b               , B               , VoidSymbol      , VoidSymbol      ],[ backslash       , VoidSymbol      ]}; // b B     \
            key <AB06> {[ n               , N               , ntilde          , Ntilde          ],[ VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ
            key <AB07> {[ m               , M               , mu              , masculine       ],[ 0               , U2070           ]}; // m M µ º 0 ⁰
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           ],[ comma           , dead_cedilla    ]}; // , ; · • , ¸
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      ],[ period          , VoidSymbol      ]}; // . : …   .
            key <AB10> {[ slash           , question        , backslash       , questiondown    ],[ plus            , notsign         ]}; // / ? \ ¿ + ¬

            // Pinky keys
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      ],[ dead_grave      , dead_tilde      ]}; // ` ~     ` ~
            key <AE11> {[ minus           , underscore      , emdash          , endash          ],[ VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       ],[ VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AD11> {[ bracketleft     , braceleft       , less            , lessthanequal   ],[ VoidSymbol      , VoidSymbol      ]}; // [ { < ≤
            key <AD12> {[ bracketright    , braceright      , greater         , greaterthanequal],[ VoidSymbol      , VoidSymbol      ]}; // ] } > ≥
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      ],[ dead_acute      , VoidSymbol      ]}; // ' "     ´
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      ],[ VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , VoidSymbol      , VoidSymbol      ],[ VoidSymbol      , VoidSymbol      ]}; // < >

            // Space bar
            key <SPCE> {[ space           , nobreakspace    , U2019           , U2019           ],[ nobreakspace    , U202F           ]}; //     ’ ’

            // AltGr
            // Note: the `ISO_Level5_Latch` here is meaningless but helps with Chromium.
            key <RALT> {
                type = "TWO_LEVEL",
                symbols = [ ISO_Level5_Latch, ISO_Level5_Latch ],
                actions = [ SetGroup(group=2), SetGroup(group=2) ]
            };
        };""")
}]}


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
