SHELL := /bin/bash
DOCKER_COMPOSE := docker-compose -f ./stack/docker-compose.yml
SERVICE_NAME ?= crawler-service

help: ## Show this help
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

build: ## Build container
	@${DOCKER_COMPOSE} build

up: ## Start container
	@${DOCKER_COMPOSE} up -d

ps: ## List running containers
	@${DOCKER_COMPOSE} ps

down: ## Close running containers
	@${DOCKER_COMPOSE} down

logs: ## Show container's logs
	@${DOCKER_COMPOSE} logs ${SERVICE_NAME}

tail: ## Tail container's logs
	@${DOCKER_COMPOSE} logs -f ${SERVICE_NAME}

shell: ## Run shell in container
	@${DOCKER_COMPOSE} run --rm ${SERVICE_NAME} bash

test: ## Run unit tests
	@${DOCKER_COMPOSE} run --rm -e TEST=True ${SERVICE_NAME} sh -c "scrapy crawl wbcsd && python3 -m unittest"