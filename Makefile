all:
	kalamine layout/*.yaml layout.dev/*.yaml

qwerty:
	kalamine layout/qwerty.yaml

dvorak:
	kalamine layout/dvorak.yaml

clean:
	rm -f dist/*
