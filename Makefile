pypi:
	rm dist/*
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

sphinx:
	sphinx-build -aEv docs docs/_build
