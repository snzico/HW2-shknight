run:
	python3 -m PyInstaller while.py
	cp ./dist/while while
	rm -fr build
	rm -fr dist
