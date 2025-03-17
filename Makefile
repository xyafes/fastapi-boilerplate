# Makefile

DOCKER_COMPOSE_FILE = docker-compose.yml


up:
	docker compose --verbose -f $(DOCKER_COMPOSE_FILE) up --build -d

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

r:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build -d

logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f --tail 100

prune:
	docker system prune -a
	docker image prune -a
	docker volume prune -a

exec:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh

lq:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec rabbitmq rabbitmqctl list_queues
	
init:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich init -t source.settings.tortoise_orm"

init-db:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich init-db"

upgrade:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich upgrade"

migrate:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich migrate"

psql:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db psql -U postgres

psql_user:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c 'SELECT COUNT(*) FROM public."user";'

psql_list:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "\dt"

count_ku:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "SELECT * FROM kickuser;"

count_m:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "SELECT COUNT(*) FROM UserMessage;"

backup:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec db pg_dump -U postgres db > db.sql

py:
	docker compose -f $(DOCKER_COMPOSE_FILE) exec celery sh -c "python"