all:

build:
	python setup.py build

test:
	python setup.py test

clean:
	rm -rfv build dist *.egg-info *.so
