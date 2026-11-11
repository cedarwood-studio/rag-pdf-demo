COMPOSE ?= docker compose

.PHONY: up down logs ingest ingest-baseline eval eval-baseline eval-steps eval-heldout test lint

up:            ## build and start Postgres and the app; first start ingests the PDFs
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f app

ingest:        ## rebuild the tuned collection (heading and page aware chunks)
	$(COMPOSE) exec app python -m ragdemo.ingest --strategy heading --collection heading

ingest-baseline: ## build the baseline collection (fixed-size chunks)
	$(COMPOSE) exec app python -m ragdemo.ingest --strategy fixed --collection fixed

EVAL = $(COMPOSE) exec app python -m ragdemo.eval
HELDOUT = --questions eval/questions-heldout.json

eval:          ## score the tuned configuration on eval/questions.json
	$(EVAL) --collection heading --threshold 0.62 --strict-threshold 0.75 --no-hybrid --label tuned

eval-baseline: ## score the baseline configuration (run make ingest-baseline first)
	$(EVAL) --collection fixed --threshold 0.5 --strict-threshold 0 --no-hybrid --label baseline

eval-steps:    ## the intermediate steps recorded in EVAL.md
	$(EVAL) --collection heading --threshold 0.5 --strict-threshold 0 --no-hybrid --label step1-heading-chunks
	$(EVAL) --collection heading --threshold 0.5 --strict-threshold 0 --hybrid --keyword-weight 1.0 --label step2-hybrid-rejected
	$(EVAL) --collection heading --threshold 0.62 --strict-threshold 0 --no-hybrid --label step3-threshold

eval-heldout:  ## questions written after the settings were fixed
	$(EVAL) $(HELDOUT) --collection fixed --threshold 0.5 --strict-threshold 0 --no-hybrid --label heldout-baseline
	$(EVAL) $(HELDOUT) --collection heading --threshold 0.62 --strict-threshold 0.75 --no-hybrid --label heldout-tuned

test:          ## needs a Postgres with pgvector at DATABASE_URL (the compose db is published on localhost:54329)
	pytest -q

lint:
	ruff check .
