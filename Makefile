create_virtualenv:
	virtualenv --python python3 venv
	./venv/bin/pip install -r requirements.txt

lint:
	flake8 stolas/

test:
	PYTHONPATH=. pytest