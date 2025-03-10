include .env

.PHONY: train autopep8 isort flake8 test_update test_request one multiple isPrime format check prepare_commit server client

#* Python Rules
server:
	python $(SRC)/server.py

request:
	python $(SRC)/client.py request

update:
	python $(SRC)/client.py update

new:
	python $(SRC)/client.py new

newpdf:
	python $(SRC)/client.py new rafael.pdf

#* Git Rules
isort:
	@echo "Formatando com isort..."
	isort --settings-path=$(MAKE_CONFIG_FILE) $(SRC)

autoflake:
	@echo "Removendo imports não utilizados com autoflake..."
	autoflake --remove-all-unused-imports --in-place --recursive $(SRC)

autopep8:
	@echo "Formatando com autopep8..."
	autopep8 --in-place --recursive $(SRC)

pylint:
	@echo "Executando pylint..."
	pylint --rcfile=$(PYLINT_CONFIG_FILE) --recursive=y $(SRC)

flake8:
	@echo "Executando flake8..."
	flake8 --config=$(MAKE_CONFIG_FILE) $(SRC)

format: autoflake autopep8 isort

check: flake8 pylint

prepare_commit: autoflake autopep8 isort flake8 pylint
