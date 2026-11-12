COMPOSE ?= docker compose
# Where the Python commands run. The default is inside the app container.
# To run them from a local virtualenv against the published database port: make PY=.venv/bin/python <target>
PY ?= $(COMPOSE) exec -e OPENAI_API_KEY app python
EVAL = $(PY) -m ragdemo.eval
ANSWERS = $(PY) -m ragdemo.eval_answers
HELDOUT = --questions eval/questions-heldout.json
HELDOUT2 = --questions eval/questions-heldout2.json

.PHONY: up down logs ingest ingest-full ingest-baseline eval eval-full eval-baseline eval-norerank eval-heldout bench eval-answers test lint

up:              ## build and start Postgres and the app; the first start ingests the 12 core PDFs
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f app

ingest:          ## 12 PDFs, heading and page aware chunks, collection "core"
	$(PY) -m ragdemo.ingest --corpus core

ingest-full:     ## all PDFs in corpus/sources.json, collection "full" (over an hour on a 4-core CPU the first time)
	$(PY) -m ragdemo.ingest --corpus full

ingest-baseline: ## 12 PDFs, fixed-size chunks, collection "core-fixed"
	$(PY) -m ragdemo.ingest --corpus core --strategy fixed

eval:            ## retrieval, citations and refusals on eval/questions.json, 12 PDFs, extractive answers
	$(EVAL) --collection core --label core

eval-full:       ## the same questions against the full corpus
	$(EVAL) --collection full --label full

eval-baseline:   ## fixed-size chunks and the untuned threshold
	$(EVAL) --collection core-fixed --threshold 0.5 --strict-threshold 0 --no-rerank --label core-baseline

eval-norerank:   ## the same runs with the reranker switched off, to show what it changes
	$(EVAL) --collection core --no-rerank --label core-norerank
	$(EVAL) --collection full --no-rerank --label full-norerank
	$(EVAL) $(HELDOUT2) --collection core --no-rerank --label heldout2-core-norerank
	$(EVAL) $(HELDOUT2) --collection full --no-rerank --label heldout2-full-norerank

eval-heldout:    ## questions written after the settings were fixed
	$(EVAL) $(HELDOUT) --collection core --label heldout-core
	$(EVAL) $(HELDOUT) --collection full --label heldout-full
	$(EVAL) $(HELDOUT2) --collection core --label heldout2-core
	$(EVAL) $(HELDOUT2) --collection full --label heldout2-full

bench:           ## query latency and storage size, exact search and HNSW index
	$(PY) -m ragdemo.bench --collection core --with-index --label bench-core
	$(PY) -m ragdemo.bench --collection full --with-index --label bench-full

eval-answers:    ## generated answers graded for correctness and faithfulness; needs OPENAI_API_KEY in the environment
	$(ANSWERS) --collection core --label answers-core
	$(ANSWERS) --collection full --label answers-full
	$(ANSWERS) $(HELDOUT) --collection core --label answers-heldout-core
	$(ANSWERS) $(HELDOUT) --collection full --label answers-heldout-full
	$(ANSWERS) $(HELDOUT2) --collection core --label answers-heldout2-core
	$(ANSWERS) $(HELDOUT2) --collection full --label answers-heldout2-full

test:            ## needs a Postgres with pgvector at DATABASE_URL (the compose db is published on localhost)
	pytest -q

lint:
	ruff check .
