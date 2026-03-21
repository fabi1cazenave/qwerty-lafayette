Contributing to Qwerty-Lafayette
================================================================================

Generate new layout version
--------------------------------------------------------------------------------

- Install [kalamine]
- Go to [lafayette.toml](./layouts/lafayette.toml) and increment version
- Go to `layouts` directory and generate files with:
  ```sh
  kalamine build lafayette.toml
  ```
- Move and rename generated files:
  ```sh
  mv dist/qwerty-l.json lafayette.json
  mv dist/qwerty-l.svg ../releases/lafayette.svg
  mv dist/qwerty-l.xkb_symbols ../releases/lafayette_linux.xkb_custom
  mv dist/qwerty-l.xkb_keymap ../releases/lafayette_linux_portable.xkb_keymap
  mv dist/qwerty-l.keylayout ../releases/lafayette_macos.keylayout
  mv dist/qwerty-l.klc ../releases/lafayette_windows.klc
  mv dist/qwerty-l.ahk ../releases/lafayette_windows_portable.ahk
  ```
- Generate Windows driver `lafayette_windows.exe` with KbdEdit and `lafayette_windows.klc`
  [using Kana instead of AltGr](https://www.kbdedit.com/manual/ex13_replacing_altgr_with_kana.html)
- Generate Windows portable AHK `lafayette_windows_portable.exe`
- Zip into `releases/lafayette.zip` the following files:
  - `lafayette.toml`
  - `lafayette.svg`
  - `lafayette_linux_portable.xkb_keymap`
  - `lafayette_macos.keylayout`
  - `lafayette_windows.klc`
  - `lafayette_windows_portable.ahk`
  - `lafayette_windows_portable.exe`
- Create a new tag in the git repository `vX.X` (replacing `X` by the generated version)


[kalamine]: https://github.com/OneDeadKey/kalamine
