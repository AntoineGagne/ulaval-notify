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
clean: clean-bytecode clean-coverage clean-eggs \
	clean-dist clean-build clean-tox clean-cache \
	clean-dev clean-install

.PHONY: clean-install
clean-install:
	@rm -f install.log

.PHONY: clean-bytecode
clean-bytecode:
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name '*~' -type f -delete
	@find . -name '__pycache__' -type d -exec rm -fr {} +

.PHONY: clean-coverage
clean-coverage:
	@rm -rf htmlcov
	@rm -f .coverage

.PHONY: clean-eggs
clean-eggs:
	@rm -rf .eggs
	@rm -rf *.egg-info

.PHONY: clean-dist
clean-dist:
	@rm -rf dist

.PHONY: clean-build
clean-build:
	@rm -rf build

.PHONY: clean-tox
clean-tox:
	@rm -rf .tox

.PHONY: clean-cache
clean-cache:
	@rm -rf .cache

.PHONY: clean-dev
clean-dev:
	@find . -name '.mypy_cache' -type d -exec rm -fr {} +
	@find . -name '.ropeproject' -type d -exec rm -fr {} +

.PHONY: release
release: clean
	@./setup.py sdist upload
	@./setup.py bdist_wheel upload

.PHONY: dist
dist: clean
	@./setup.py sdist
	@./setup.py bdist_wheel

.PHONY: docs
docs:
	@sphinx-apidoc -o docs/ $(MAIN_PACKAGE)
	@$(MAKE) -C docs clean
	@$(MAKE) -C docs html
