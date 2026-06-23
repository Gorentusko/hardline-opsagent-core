setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check app tests

run:
	python -m app.main

docker-up:
	docker compose up --build

demo:
	bash scripts/demo_generate_report.sh
