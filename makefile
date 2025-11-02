.ONESHELL:

run-dev:
	docker compose down -v
	docker compose build --no-cache
	docker compose up

run-production:
	docker compose up
