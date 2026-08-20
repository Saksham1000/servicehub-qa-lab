.PHONY: setup start stop test smoke regression api-test ui-test db-test graphql-test performance-test
setup:
	python -m pip install -r requirements.txt
start:
	docker compose up --build -d
stop:
	docker compose down
test:
	pytest --html=reports/report.html --junitxml=reports/junit.xml
smoke:
	pytest -m smoke
regression:
	pytest -m regression
api-test:
	pytest automation/api -m api
ui-test:
	pytest automation/ui -m ui --browser chrome
db-test:
	pytest automation/database -m database
graphql-test:
	pytest automation/graphql app/backend/tests/test_graphql.py -m graphql
performance-test:
	locust -f performance/locustfile.py --host http://localhost:8000
