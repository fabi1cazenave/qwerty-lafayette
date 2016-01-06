all:
	python3 script/make.py layout/*.yaml layout.dev/*.yaml

qwerty:
	python3 script/make.py layout/qwerty.yaml

dvorak:
	python3 script/make.py layout/dvorak.yaml

clean:
	rm -f dist/*

lint:
	flake8 script

