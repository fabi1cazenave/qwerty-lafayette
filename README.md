Qwerty-Lafayette
================================================================================

A Qwerty layout for French-speaking users.


TL;DR:
--------------------------------------------------------------------------------

* use a dead key on the home row for the most frequent accented characters;
* use the AltGr layer for programming symbols. Or don’t use it at all, and keep two alt keys.

This layout claims to be better than Azerty for French and better than Qwerty for programming.


Layout
--------------------------------------------------------------------------------

The <kbd>;</kbd> key is turned into a dead key that gives access to all acute accents, grave accents, cedillas, digraphs and quote signs you’ll need to write in proper French:

![base & dead key layout](layouts/qwerty_1dk.png)

… which leaves the AltGr layer fully available for any customization you have in mind.

![altgr layout](layouts/qwerty_alt.png)

The default layout allows to write in English, French, Spanish, Portuguese, Italian, German, Dutch and Esperanto easily.

More information on the website (in French): https://qwerty-lafayette.org/


Download
--------------------------------------------------------------------------------

https://qwerty-lafayette.org/#download


Make your own
--------------------------------------------------------------------------------

You’ll need the latest version of [Kalamine](https://github.com/fabi1cazenave/kalamine) to build your own layout:

```bash
pip3 install kalamine
```

And build your custom layout like this:

```bash
kalamine MyCustomLayout.yaml
```


Why the name?
--------------------------------------------------------------------------------

Because of [Gilbert du Motier, Marquis de Lafayette](https://en.wikipedia.org/wiki/Gilbert_du_Motier,_Marquis_de_Lafayette).


Alternatives
--------------------------------------------------------------------------------

There are other ways to use a Qwerty-US keyboard for French. Here are the two most intuitive ones:

* [qwerty-intl](https://en.wikipedia.org/wiki/QWERTY#US-International) — turns <kbd>`</kbd><kbd>~</kbd><kbd>'</kbd><kbd>"</kbd><kbd>^</kbd> into dead keys;
* [qwerty-fr](http://marin.jb.free.fr/qwerty-fr/) — no dead keys, and a smart use of the AltGr layer for all French accented characters.

Qwerty-Lafayette provides sharper typography and better ergonomics in the long run, but has a steeper learning curve for non-touch-typists.
