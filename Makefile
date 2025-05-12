.PHONY: run-dev
run-dev:
	docker compose up --build


.PHONY: run-prod
run-prod:
	docker-compose -f docker-compose.prod.yaml up --build


.PHONY: kill-prod
kill-prod:
	docker-compose -f docker-compose.prod.yaml down


.PHONY: api-sh
api-sh:
	docker exec -it homebroker-backend-1 sh
