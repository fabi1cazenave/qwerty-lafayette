all:
	kalamine layouts/*.yaml

dev:
	pip3 install kalamine

deploy:
	scripts/deploy

clean:
	rm -rf build dist/*

# the install/uninstall targets below require Kalamine v0.4.2+

install:
	@echo "Installer script for XKB (GNU/Linux). Requires super-user privileges."
	@echo
	xkalamine install layouts/qwerty*.yaml

uninstall:
	@echo "Unistaller script for XKB (GNU/Linux). Requires super-user privileges."
	@echo
	xkalamine remove fr/lafayette
	@echo
	xkalamine remove fr/lafayette42
	@echo
