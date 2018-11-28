package: clean
	python setup.py sdist bdist_wheel

release: package
	twine upload dist/*

clean:
	rm -rf dist
