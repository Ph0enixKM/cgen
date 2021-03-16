all:
	python3 cgen.py

build:
	cxfreeze -c cgen.py --target-dir dist