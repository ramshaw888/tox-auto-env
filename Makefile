package: clean
	python setup.py sdist bdist_wheel

upload: package
	twine upload dist/*

git-tag:
	$(eval TAG := "v$(shell python setup.py --version)")
	git tag -a -m "Release!" $(TAG)
	git push origin $(TAG)

clean:
	rm -rf dist

release: upload git-tag
