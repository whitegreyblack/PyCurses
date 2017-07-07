clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*.log' -exec rm --force {} +
	find . -name '*.db' -exec rm --force {} +
check: clean
	python checker.py testfolder/

test: clean

populate: clean
	python populate.py testfolder/

