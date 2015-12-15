Qwerty-Lafayette
================

A Qwerty layout for French-speaking users.

TL;DR:
------

* use a dead key on the home row for the most frequent accented characters;
* use the AltGr layer for programming symbols. Or don’t use it at all, and keep two alt keys.

This layout claims to be better than Azerty for French and better than Qwerty for programming.

Layout
------

The `;:` key is turned into a dead key that gives access to all acute accents, grave accents, cedillas and quote signs you’ll need to write in French properly:
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
│ ~   │ !   │ @   │ #   │ $   │ %   │ ^   │ &   │ *   │ (   │ )   │ _   │ +   ┃          ┃
│ `   │ 1 „ │ 2 “ │ 3 ” │ 4   │ 5 € │ 6   │ 7   │ 8   │ 9   │ 0 ° │ -   │ =   ┃ ⌫        ┃
┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┯━━━━━━━┩
┃        ┃ Q   │ W   │ E   │ R   │ T   │ Y   │ U   │ I   │ O   │ P   │ « { │ » } │ |     │
┃ ↹      ┃   æ │   é │   è │     │     │     │   ù │     │   œ │     │ ^ [ │ ¨ ] │ \     │
┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┲━━━━┷━━━━━━━┪
┃         ┃ A   │ S   │ D   │ F   │ G   │ H   │ J   │ K   │ L   │ ★   │ "   ┃            ┃
┃ ⇬       ┃   à │     │     │     │     │   ← │   ↓ │   ↑ │   → │   ` │ '   ┃ ⏎          ┃
┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┻━━━━━━━━━━━━┫
┃      ┃ >   │ Z   │ X   │ C   │ V   │ B   │ N   │ M   │ ;   │ :   │ ?   ┃               ┃
┃ ⇧    ┃ <   │     │     │   ç │     │     │     │   µ │ ,   │ . … │ /   ┃ ⇧             ┃
┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
┃       ┃       ┃       ┃ ⍽ nbsp                         ┃       ┃       ┃       ┃       ┃
┃ Ctrl  ┃ super ┃ Alt   ┃ ␣                            ’ ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
```

… which leaves the AltGr layer fully available for any customization you have in mind.
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┲━━━━━━━━━━┓
│   ~ │     │     │     │     │     │     │     │     │     │     │     │     ┃          ┃
│   ` │   ! │   ( │   ) │   = │   ? │     │   7 │   8 │   9 │   / │     │     ┃ ⌫        ┃
┢━━━━━┷━━┱──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┺━━┳━━━━━━━┫
┃        ┃     │     │     │     │     │     │     │     │     │     │     │     ┃       ┃
┃ ↹      ┃   - │   < │   > │   / │   \ │     │   4 │   5 │   6 │   * │     │     ┃       ┃
┣━━━━━━━━┻┱────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┴┬────┺┓  ⏎   ┃
┃         ┃     │     │     │     │     │     │     │     │     │     │   ˙ │     ┃      ┃
┃ ⇬       ┃   { │   [ │   ] │   } │   | │     │   1 │   2 │   3 │   - │   ´ │     ┃      ┃
┣━━━━━━┳━━┹──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┲━━┷━━━━━┻━━━━━━┫
┃      ┃     │     │     │     │     │     │     │     │     │     │     ┃               ┃
┃ ⇧    ┃     │     │     │     │     │     │     │   0 │   , │   . │   + ┃ ⇧             ┃
┣━━━━━━┻┳━━━━┷━━┳━━┷━━━━┱┴─────┴─────┴─────┴─────┴─────┴─┲━━━┷━━━┳━┷━━━━━╋━━━━━━━┳━━━━━━━┫
┃       ┃       ┃       ┃                                ┃       ┃       ┃       ┃       ┃
┃ Ctrl  ┃ super ┃ Alt   ┃                           Esc. ┃ AltGr ┃ super ┃ menu  ┃ Ctrl  ┃
┗━━━━━━━┻━━━━━━━┻━━━━━━━┹────────────────────────────────┺━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
```

The default layout allows to write in English, French, Spanish, Portuguese, Italian, German, Dutch and Esperanto easily.

More information on the website (in French): http://fabi1cazenave.github.io/qwerty-lafayette/

Why the name?
-------------

https://en.wikipedia.org/wiki/Gilbert_du_Motier,_Marquis_de_Lafayette

Alternatives
------------

There are other ways to use a Qwerty-US keyboard for French. Here are the two most intuitive ones:

* [qwerty-intl](https://en.wikipedia.org/wiki/QWERTY#US-International) — turns ``~`'"^`` into dead keys;
* [qwerty-fr](http://marin.jb.free.fr/qwerty-fr/) — no dead keys, and a smart use of the AltGr layer for all French accented characters.

The Qwerty-Lafayette project aims to provide sharper typography and better ergonomics in the long run, but has a steeper learning curve.

