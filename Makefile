.PHONY: help clean test

help:
	cat README.md

clean:
	rm -rf src/*.pyc
	rm -rf src/*__pycache__
	rm -rf test/*.pyc
	rm -rf test/*__pycache__

test:
	python3 -m unittest -v test || exit 0

chstyle:
	pylint src || exit 0

chstyle-test:
	pylint test || exit 0
