clean:
	@find . -name '*.pyc' -exec rm --force {} +
	@find . -name '*.pyo' -exec rm --force {} +
	@find . -name '*.log' -exec rm --force {} +
	@find . -name '*.db' -exec rm --force {} +
	@find . | grep -E "(__pycache__)" | xargs rm -rf

lint: clean
	flake8 --exclude=.log .

check: clean
	python checker.py testfolder/

test: clean

populate: clean
	python populate.py testfolder/

push: clean
	git push origin master
