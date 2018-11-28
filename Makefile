package: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

release: package
	twine upload dist/*
