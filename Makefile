all:
	kalamine layouts/*.yaml

dev:
	pip3 install kalamine

clean:
	rm -rf dist/*

# the install/uninstall targets below require Kalamine v0.4+

install:
	@echo "Installer script for XKB (GNU/Linux). Requires super-user privileges."
	@echo
	xkalamine install layouts/qwerty.yaml
	@echo
	xkalamine install layouts/qwerty42.yaml
	@echo

uninstall:
	@echo "Unistaller script for XKB (GNU/Linux). Requires super-user privileges."
	@echo
	xkalamine remove fr/lafayette
	@echo
	xkalamine remove fr/lafayette42
	@echo
