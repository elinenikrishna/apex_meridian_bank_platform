.PHONY: test sample api frontend

test:
	python -m pytest -q

sample:
	python -m apex_meridian.data_generation.generator --records 5000 --batch-size 1000 --domains all --output data/generated/local_demo

api:
	uvicorn apps.backend.app.main:app --host 0.0.0.0 --port 8080 --reload

frontend:
	python -m http.server 8088 --directory frontend

