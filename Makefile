all:
	python3 script/make.py layout/*.yaml

lafayette:
	python3 script/make.py layout/lafayette.yaml

lint:
	flake8 script

