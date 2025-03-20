# Makefile

DOCKER_COMPOSE_FILE = docker compose --verbose -f docker-compose.yml


up:
	$(DOCKER_COMPOSE_FILE) up --build -d

down:
	$(DOCKER_COMPOSE_FILE) down

r:
	$(DOCKER_COMPOSE_FILE) down
	$(DOCKER_COMPOSE_FILE) up --build -d

build:
	$(DOCKER_COMPOSE_FILE) up --build -d

logs:
	$(DOCKER_COMPOSE_FILE) logs -f --tail 100

prune:
	docker system prune -a
	docker image prune -a
	docker volume prune -a

exec:
	$(DOCKER_COMPOSE_FILE) exec celery sh

lq:
	$(DOCKER_COMPOSE_FILE) exec rabbitmq rabbitmqctl list_queues
	
init:
	$(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich init -t source.settings.tortoise_orm"

init-db:
	$(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich init-db"

upgrade:
	$(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich upgrade"

migrate:
	$(DOCKER_COMPOSE_FILE) exec celery sh -c "aerich migrate"

psql:
	$(DOCKER_COMPOSE_FILE) exec db psql -U postgres

psql_user:
	$(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "\dt"

count_ku:
	$(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "SELECT * FROM kickuser;"

count_m:
	$(DOCKER_COMPOSE_FILE) exec db psql -U postgres -d db -c "SELECT COUNT(*) FROM UserMessage;"

backup:
	$(DOCKER_COMPOSE_FILE) exec db pg_dump -U postgres db > db.sql
# todo: ADD ipython
py:
	$(DOCKER_COMPOSE_FILE) exec celery sh -c "python"