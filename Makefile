all:
	kalamine layouts/*.yaml

install:
	@echo "Installer script for XKB (GNU/Linux). Requires super-user privileges."
	python3 bin/xkb_install.py
	@echo
	@echo "Testable with one of the following:"
	@echo "    setxkbmap fr -variant lafayette"
	@echo "    setxkbmap fr -variant lafayette42"

clean:
	rm -rf dist/*
