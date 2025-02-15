SHELL := /bin/bash

all:
	make build
	make up

build:
	docker compose -f srcs/docker-compose.yml build

up:
	docker compose -f srcs/docker-compose.yml up

down:
	docker compose -f srcs/docker-compose.yml down

logs:
	docker compose logs -f

streamlit:
	venv/bin/streamlit run streamlit_app/app.py --server.address 0.0.0.0 --server.port 8501

backend-shell:
	docker exec -it $$(docker ps -qf "name=backend") /bin/sh

frontend-shell:
	docker exec -it $$(docker ps -qf "name=frontend") /bin/sh

clean:
	docker compose -f srcs/docker-compose.yml down --rmi all --volumes --remove-orphans

.PHONY: all build up down clean streamlit