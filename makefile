.ONESHELL:

run-dev:
	docker compose down -v
	docker compose build --no-cache
	docker compose up

run:
	docker compose up

stop:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f django

shell:
	docker compose exec django python manage.py shell

migrate:
	docker compose exec django python manage.py migrate

makemigrations:
	docker compose exec django python manage.py makemigrations

createsuperuser:
	docker compose exec django python manage.py createsuperuser

run-production:
	docker compose up -d
