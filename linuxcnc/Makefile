

all: format check install

format:
	ruff format mpg.py

check:
	ruff check mpg.py

install:
	sudo cp mpg.py /usr/local/bin/mpg
	sudo chmod 755 /usr/local/bin/mpg

