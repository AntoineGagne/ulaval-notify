MAIN_PACKAGE := ulaval_notify

.PHONY: init
init:
	@pip install -r requirements.txt

.PHONY: install
install:
	@./setup.py install --optimize=2 --record=install.log

.PHONY: build
build:
	@./setup.py build

.PHONY: check
check: init
	@echo "================== flake8 =================="
	@flake8 --show-source --statistics $(MAIN_PACKAGE)
	@echo -e "\n\n================== pylint =================="
	@pylint $(MAIN_PACKAGE)

.PHONY: test
test:
	@./setup.py test

.PHONY: test-all
test-all: init
	@tox

.PHONY: tox
tox: test-all

.PHONY: coverage
coverage: init
	@coverage run --source $(MAIN_PACKAGE) -m py.test
	@coverage report
	@coverage html

.PHONY: clean
clean: clean-bytecode

.PHONY: clean-bytecode
clean-bytecode:
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name '*~' -type f -delete
