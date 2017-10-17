all: docs publish

docs: FORCE
	jupyter nbconvert docs/lyx_readme.ipynb --to html --template=basic --execute; \
	mv docs/lyx_readme.html docs/readme.html; \
	jupyter nbconvert docs/lyx_readme.ipynb --to markdown --execute; \
	mv docs/lyx_readme.md README.md; \
  cd ~/code/lyxithea/docs; \
	make html

publish: FORCE
	mkdir -p ~/pages/lyxithea; \
	cd ~/pages/lyxithea; \
	git rm -r *; \
	cd ~/code/lyxithea/docs; \
	cp -r _build/html/* ~/pages/lyxithea; \
	cd ~/pages/lyxithea; \
	git add *; \
	touch .nojekyll; \
	git add .nojekyll; \
	git commit -am "$(shell git log -1 --pretty=%B | tr -d '\n')"; \
	git push origin gh-pages; \
	cd ~/code/lyxithea

FORCE:
