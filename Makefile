all:
	kalamine build layouts/lafayette.toml    --out layouts/lafayette.json
	kalamine build layouts/lafayette101.toml --out layouts/lafayette101.json

dev:
	pip3 install kalamine

clean:
	rm -rf dist/*

install:
	@echo "Installer script for XKB (GNU/Linux). Requires super-user privileges for XOrg."
	@echo
	xkalamine install layouts/*.toml

uninstall:
	@echo "Uninstaller script for XKB (GNU/Linux). Requires super-user privileges for XOrg."
	@echo
	xkalamine remove fr/lafayette
	@echo
	xkalamine remove fr/lafayette42
	@echo
	xkalamine remove fr/lafayette101
	@echo
