all:

build:
	python setup.py build

# A race condition occurs where the file hasn't been completely copied before
# the testrunner tries to import `_jump`. To prevent this we copy the file
# manually before running the tests.
%.so:
	cp $(shell find build -name "_jump*.so") "$(CURDIR)/$<"


test: build %.so
	python setup.py test

clean:
	rm -rfv build dist *.egg-info *.so
