install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ndfl-vitalyapro

build:
	python -m build

upload:
	python -m twine upload --repository testpypi dist/* -u __token__