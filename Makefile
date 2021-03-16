all:
	python3 cgen.py

build:
	cxfreeze -c cgen.py --target-dir dist
	if [ -f 'cgen_linux_x86_64.tar.gz'] ; then rm cgen_linux_x86_64.tar.gz; fi
	tar -czvf cgen_linux_x86_64.tar.gz dist