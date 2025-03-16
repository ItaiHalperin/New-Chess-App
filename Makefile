.PHONY: black black_check flake8 unit_test functional_test
all: black_check flake8 typecheck

black:
	black .

black_check:
	black .

flake8:
	# stop the build if there are Python syntax errors or undefined names
	flake8 src --count --show-source --statistic --max-line-length=120

typecheck:
	mypy ./src


