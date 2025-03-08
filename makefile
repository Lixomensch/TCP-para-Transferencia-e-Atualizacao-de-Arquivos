include .env

.PHONY: train autopep8 isort flake8

#* Python Rules
server:
	python src/server.py

client:
	python src/client.py $(action)
	
request:
	python src/client.py request

update:
	python src/client.py update

#* Test Rules
one:
	python tests/test_oneClient.py

multiple:
	python tests/test_multipleClients.py

isPrime:
	python tests/test_isPrime.py

#* Git Rules
isort:
	isort --settings-path=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

autoflake:
	autoflake --remove-all-unused-imports --in-place --recursive $(FORMAT_CHECK_SRC)

autopep8:
	autopep8 --in-place --recursive $(FORMAT_CHECK_SRC)

pylint:
	pylint --rcfile=$(PYLINT_CONFIG_FILE)  --recursive=y  $(FORMAT_CHECK_SRC)

flake8:
	flake8 --config=$(MAKE_CONFIG_FILE) $(FORMAT_CHECK_SRC)

format: autoflake autopep8 isort

check: flake8 pylint

prepare_commit: autoflake autopep8 isort flake8 pylint
