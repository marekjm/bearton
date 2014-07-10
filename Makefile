PYTHON_VERSION=`python3 -c "import sys; v=sys.version_info;print('{0}.{1}'.format(v[0], v[1]))"`
PYTHON_SITE_PACKAGES=~/.local/lib/python${PYTHON_VERSION}/site-packages
PYTHON_UNITTEST_FLAGS=--failfast --catch --verbose

.PHONY: tests

check-python:
	@echo "Python 3 version: ${PYTHON_VERSION}"
	@echo "Python site packages: ${PYTHON_SITE_PACKAGES}"


tests:
	python3 ./tests/util.py ${PYTHON_UNITTEST_FLAGS}
	python3 ./tests/initialisation.py ${PYTHON_UNITTEST_FLAGS}


install:
	python3 install.py
