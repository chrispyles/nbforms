distro:
	rm dist/*
	python3 setup.py sdist bdist_wheel

pypi:
	rm dist/*
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

test-pypi:
	rm dist/*
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/* --repository-url https://test.pypi.org/legacy/
