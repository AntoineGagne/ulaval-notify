.PHONY: init
init:
	@pip install -r requirements.txt

.PHONY: install
install:
	@./setup.py install --optimize=1 --record=install.log

.PHONY: build
build:
	@./setup.py build

.PHONY: test
test:
	@./setup.py test

.PHONY: coverage
coverage:
	@coverage run --source ulaval_notify -m py.test
	@coverage report
	@coverage html

.PHONY: clean
clean: clean-bytecode

.PHONY: clean-bytecode
clean-bytecode:
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name '*~' -type f -delete
