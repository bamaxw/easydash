version = `cat ./VERSION`
package-name = easydash


test:
	echo "no tests provided"

upload: test vpatch
	devpi upload
	rm -r dist

install-locally:
	pip install -U .

publish:
	devpi push "$(package-name)==$(version)" "inyourarea/prod"

vpatch:
	bumpversion patch

vminor:
	bumpversion minor

vmajor:
	bumpversion major
