help:
	cat README.md

clean:
	rm src/*.pyc
	rm -r src/*__pycache__
	rm test/*.pyc
	rm -r test/*__pycache__
