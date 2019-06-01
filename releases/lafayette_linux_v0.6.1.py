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
    'desc': 'French (Lafayette)',
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.6.1
        // Last change   : 2018-04-08
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
            name[group1]= "French (Lafayette)";
            key.type[group1] = "EIGHT_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , U201E           , exclamdown      , exclam          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 1 ! „ ¡ !
            key <AE02> {[ 2               , at              , U201C           , U2018           , parenleft       , guillemotleft   , VoidSymbol      , VoidSymbol      ]}; // 2 @ “ ‘ ( «
            key <AE03> {[ 3               , numbersign      , U201D           , U2019           , parenright      , guillemotright  , VoidSymbol      , VoidSymbol      ]}; // 3 # ” ’ ) »
            key <AE04> {[ 4               , dollar          , sterling        , cent            , apostrophe      , dead_acute      , VoidSymbol      , VoidSymbol      ]}; // 4 $ £ ¢ ' ´
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           , quotedbl        , dead_diaeresis  , VoidSymbol      , VoidSymbol      ]}; // 5 % € ‰ " ¨
            key <AE06> {[ 6               , asciicircum     , VoidSymbol      , VoidSymbol      , asciicircum     , dead_circumflex , VoidSymbol      , VoidSymbol      ]}; // 6 ^     ^ ^
            key <AE07> {[ 7               , ampersand       , bar             , brokenbar       , 7               , U2077           , VoidSymbol      , VoidSymbol      ]}; // 7 & | ¦ 7 ⁷
            key <AE08> {[ 8               , asterisk        , infinity        , U2605           , 8               , U2078           , VoidSymbol      , VoidSymbol      ]}; // 8 * ∞ ★ 8 ⁸
            key <AE09> {[ 9               , parenleft       , VoidSymbol      , VoidSymbol      , 9               , U2079           , VoidSymbol      , VoidSymbol      ]}; // 9 (     9 ⁹
            key <AE10> {[ 0               , parenright      , degree          , VoidSymbol      , slash           , division        , VoidSymbol      , VoidSymbol      ]}; // 0 ) °   / ÷

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              , equal           , notequal        , VoidSymbol      , VoidSymbol      ]}; // q Q æ Æ = ≠
            key <AD02> {[ w               , W               , eacute          , Eacute          , less            , lessthanequal   , VoidSymbol      , VoidSymbol      ]}; // w W é É < ≤
            key <AD03> {[ e               , E               , egrave          , Egrave          , greater         , greaterthanequal, VoidSymbol      , VoidSymbol      ]}; // e E è È > ≥
            key <AD04> {[ r               , R               , registered      , trademark       , minus           , emdash          , VoidSymbol      , VoidSymbol      ]}; // r R ® ™ - —
            key <AD05> {[ t               , T               , thorn           , Thorn           , plus            , plusminus       , VoidSymbol      , VoidSymbol      ]}; // t T þ Þ + ±
            key <AD06> {[ y               , Y               , yen             , currency        , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // y Y ¥ ¤
            key <AD07> {[ u               , U               , ugrave          , Ugrave          , 4               , U2074           , VoidSymbol      , VoidSymbol      ]}; // u U ù Ù 4 ⁴
            key <AD08> {[ i               , I               , U0133           , U0132           , 5               , U2075           , VoidSymbol      , VoidSymbol      ]}; // i I ĳ Ĳ 5 ⁵
            key <AD09> {[ o               , O               , oe              , OE              , 6               , U2076           , VoidSymbol      , VoidSymbol      ]}; // o O œ Œ 6 ⁶
            key <AD10> {[ p               , P               , section         , paragraph       , asterisk        , multiply        , VoidSymbol      , VoidSymbol      ]}; // p P § ¶ * ×

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
            key <AB01> {[ z               , Z               , less            , lessthanequal   , asciitilde      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // z Z < ≤ ~ ~
            key <AB02> {[ x               , X               , greater         , greaterthanequal, grave           , dead_grave      , VoidSymbol      , VoidSymbol      ]}; // x X > ≥ ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        , bar             , brokenbar       , VoidSymbol      , VoidSymbol      ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , ubreve          , Ubreve          , underscore      , endash          , VoidSymbol      , VoidSymbol      ]}; // v V ŭ Ŭ _ –
            key <AB05> {[ b               , B               , dagger          , doubledagger    , backslash       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // b B † ‡ \ 
            key <AB06> {[ n               , N               , ntilde          , Ntilde          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ
            key <AB07> {[ m               , M               , mu              , masculine       , 0               , U2070           , VoidSymbol      , VoidSymbol      ]}; // m M µ º 0 ⁰
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           , comma           , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // , ; · • ,
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      , period          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // . : …   .
            key <AB10> {[ slash           , question        , backslash       , questiondown    , plus            , notsign         , VoidSymbol      , VoidSymbol      ]}; // / ? \ ¿ + ¬

            // Pinky keys
            key <AE11> {[ minus           , underscore      , emdash          , endash          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AD11> {[ dead_circumflex , guillemotleft   , bracketleft     , braceleft       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ^ « [ {
            key <AD12> {[ dead_diaeresis  , guillemotright  , bracketright    , braceright      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ¨ » ] }
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      , dead_acute      , dead_abovedot   , VoidSymbol      , VoidSymbol      ]}; // ' "     ´ ˙
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      , dead_grave      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // ` ~     ` ~
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , lessthanequal   , greaterthanequal, VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // < > ≤ ≥

            // Space bar
            key <SPCE> {[ space           , nobreakspace    , U2019           , U2019           , nobreakspace    , U202F           , VoidSymbol      , VoidSymbol      ]}; //     ’ ’

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key:
            // this is the only way to have a multi-purpose dead key with XKB.
            // The real AltGr key is an ISO_Level5_Switch.
            include "level5(ralt_switch)"
        };""")
}, {
    'name': 'lafayette42',
    'desc': 'French (Lafayette42)',
    'symbols': textwrap.dedent("""
        // Project page  : https://github.com/fabi1cazenave/qwerty-lafayette
        // Author        : Fabien Cazenave
        // Version       : 0.6.1
        // Last change   : 2018-04-08
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
            name[group1]= "French (Lafayette42)";
            key.type[group1] = "EIGHT_LEVEL";

            // Digits
            key <AE01> {[ 1               , exclam          , U201E           , exclamdown      , exclam          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // 1 ! „ ¡ !
            key <AE02> {[ 2               , at              , U201C           , U2018           , parenleft       , guillemotleft   , VoidSymbol      , VoidSymbol      ]}; // 2 @ “ ‘ ( «
            key <AE03> {[ 3               , numbersign      , U201D           , U2019           , parenright      , guillemotright  , VoidSymbol      , VoidSymbol      ]}; // 3 # ” ’ ) »
            key <AE04> {[ 4               , dollar          , sterling        , cent            , apostrophe      , dead_acute      , VoidSymbol      , VoidSymbol      ]}; // 4 $ £ ¢ ' ´
            key <AE05> {[ 5               , percent         , EuroSign        , U2030           , quotedbl        , dead_diaeresis  , VoidSymbol      , VoidSymbol      ]}; // 5 % € ‰ " ¨
            key <AE06> {[ 6               , asciicircum     , yen             , currency        , asciicircum     , dead_circumflex , VoidSymbol      , VoidSymbol      ]}; // 6 ^ ¥ ¤ ^ ^
            key <AE07> {[ 7               , ampersand       , VoidSymbol      , VoidSymbol      , 7               , U2077           , VoidSymbol      , VoidSymbol      ]}; // 7 &     7 ⁷
            key <AE08> {[ 8               , asterisk        , section         , VoidSymbol      , 8               , U2078           , VoidSymbol      , VoidSymbol      ]}; // 8 * §   8 ⁸
            key <AE09> {[ 9               , guillemotleft   , paragraph       , VoidSymbol      , 9               , U2079           , VoidSymbol      , VoidSymbol      ]}; // 9 « ¶   9 ⁹
            key <AE10> {[ 0               , guillemotright  , degree          , VoidSymbol      , slash           , division        , VoidSymbol      , VoidSymbol      ]}; // 0 » °   / ÷

            // Letters, first row
            key <AD01> {[ q               , Q               , ae              , AE              , equal           , notequal        , VoidSymbol      , VoidSymbol      ]}; // q Q æ Æ = ≠
            key <AD02> {[ w               , W               , eacute          , Eacute          , less            , lessthanequal   , VoidSymbol      , VoidSymbol      ]}; // w W é É < ≤
            key <AD03> {[ e               , E               , egrave          , Egrave          , greater         , greaterthanequal, VoidSymbol      , VoidSymbol      ]}; // e E è È > ≥
            key <AD04> {[ r               , R               , registered      , VoidSymbol      , minus           , emdash          , VoidSymbol      , VoidSymbol      ]}; // r R ®   - —
            key <AD05> {[ t               , T               , trademark       , VoidSymbol      , plus            , plusminus       , VoidSymbol      , VoidSymbol      ]}; // t T ™   + ±
            key <AD06> {[ y               , Y               , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // y Y
            key <AD07> {[ u               , U               , ugrave          , Ugrave          , 4               , U2074           , VoidSymbol      , VoidSymbol      ]}; // u U ù Ù 4 ⁴
            key <AD08> {[ i               , I               , U0133           , U0132           , 5               , U2075           , VoidSymbol      , VoidSymbol      ]}; // i I ĳ Ĳ 5 ⁵
            key <AD09> {[ o               , O               , oe              , OE              , 6               , U2076           , VoidSymbol      , VoidSymbol      ]}; // o O œ Œ 6 ⁶
            key <AD10> {[ p               , P               , VoidSymbol      , VoidSymbol      , asterisk        , multiply        , VoidSymbol      , VoidSymbol      ]}; // p P     * ×

            // Letters, second row
            key <AC01> {[ a               , A               , agrave          , Agrave          , braceleft       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // a A à À {
            key <AC02> {[ s               , S               , ssharp          , U1E9E           , bracketleft     , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // s S ß ẞ [
            key <AC03> {[ d               , D               , ecircumflex     , Ecircumflex     , bracketright    , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // d D ê Ê ]
            key <AC04> {[ f               , F               , U017F           , ordfeminine     , braceright      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // f F ſ ª }
            key <AC05> {[ g               , G               , copyright       , VoidSymbol      , slash           , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // g G ©   /
            key <AC06> {[ h               , H               , U0177           , U0176           , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // h H ŷ Ŷ
            key <AC07> {[ j               , J               , ucircumflex     , Ucircumflex     , 1               , onesuperior     , VoidSymbol      , VoidSymbol      ]}; // j J û Û 1 ¹
            key <AC08> {[ k               , K               , icircumflex     , Icircumflex     , 2               , twosuperior     , VoidSymbol      , VoidSymbol      ]}; // k K î Î 2 ²
            key <AC09> {[ l               , L               , ocircumflex     , Ocircumflex     , 3               , threesuperior   , VoidSymbol      , VoidSymbol      ]}; // l L ô Ô 3 ³
            key <AC10> {[ ISO_Level3_Latch, dead_diaeresis  , grave           , VoidSymbol      , minus           , U2212           , VoidSymbol      , VoidSymbol      ]}; // ` ¨ `   - −

            // Letters, third row
            key <AB01> {[ z               , Z               , acircumflex     , Acircumflex     , asciitilde      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // z Z â Â ~ ~
            key <AB02> {[ x               , X               , VoidSymbol      , VoidSymbol      , grave           , dead_grave      , VoidSymbol      , VoidSymbol      ]}; // x X     ` `
            key <AB03> {[ c               , C               , ccedilla        , Ccedilla        , bar             , brokenbar       , VoidSymbol      , VoidSymbol      ]}; // c C ç Ç | ¦
            key <AB04> {[ v               , V               , VoidSymbol      , VoidSymbol      , underscore      , endash          , VoidSymbol      , VoidSymbol      ]}; // v V     _ –
            key <AB05> {[ b               , B               , VoidSymbol      , VoidSymbol      , backslash       , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // b B     \ 
            key <AB06> {[ n               , N               , ntilde          , Ntilde          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // n N ñ Ñ
            key <AB07> {[ m               , M               , mu              , masculine       , 0               , U2070           , VoidSymbol      , VoidSymbol      ]}; // m M µ º 0 ⁰
            key <AB08> {[ comma           , semicolon       , periodcentered  , U2022           , comma           , dead_cedilla    , VoidSymbol      , VoidSymbol      ]}; // , ; · • , ¸
            key <AB09> {[ period          , colon           , ellipsis        , VoidSymbol      , period          , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // . : …   .
            key <AB10> {[ slash           , question        , backslash       , questiondown    , plus            , notsign         , VoidSymbol      , VoidSymbol      ]}; // / ? \ ¿ + ¬

            // Pinky keys
            key <AE11> {[ minus           , underscore      , emdash          , endash          , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // - _ — –
            key <AE12> {[ equal           , plus            , notequal        , plusminus       , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // = + ≠ ±
            key <AD11> {[ bracketleft     , braceleft       , less            , lessthanequal   , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // [ { < ≤
            key <AD12> {[ bracketright    , braceright      , greater         , greaterthanequal, VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ] } > ≥
            key <AC11> {[ apostrophe      , quotedbl        , VoidSymbol      , VoidSymbol      , dead_acute      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // ' "     ´
            key <TLDE> {[ grave           , asciitilde      , VoidSymbol      , VoidSymbol      , dead_grave      , dead_tilde      , VoidSymbol      , VoidSymbol      ]}; // ` ~     ` ~
            key <BKSL> {[ backslash       , bar             , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // \ |
            key <LSGT> {[ less            , greater         , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      , VoidSymbol      ]}; // < >

            // Space bar
            key <SPCE> {[ space           , nobreakspace    , U2019           , U2019           , nobreakspace    , U202F           , VoidSymbol      , VoidSymbol      ]}; //     ’ ’

            // The “OneDeadKey” is an ISO_Level3_Latch, i.e. a “dead AltGr” key:
            // this is the only way to have a multi-purpose dead key with XKB.
            // The real AltGr key is an ISO_Level5_Switch.
            include "level5(ralt_switch)"
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
    with open(path, 'r+', encoding='utf-8') as symbols:
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

    # announce modified file
    print('... ' + path)


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
    print('... ' + path)
