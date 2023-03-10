install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=cli --cov=mlib --cov=utilscli --cov=app test.py

format:
	black *.py

lint:
	pylint --disable=R,C *.py 
	
all: install lint test format 