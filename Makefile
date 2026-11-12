COMPOSE ?= docker compose
# Where the Python commands run. The default is inside the app container.
# To run them from a local virtualenv against the published database port: make PY=.venv/bin/python <target>
PY ?= $(COMPOSE) exec -e OPENAI_API_KEY -e OPENAI_BASE_URL -e ANSWER_MODEL app python
EVAL = $(PY) -m ragdemo.eval
ANSWERS = $(PY) -m ragdemo.eval_answers
HELDOUT = --questions eval/questions-heldout.json
HELDOUT2 = --questions eval/questions-heldout2.json

.PHONY: up down logs ingest ingest-full ingest-baseline eval eval-full eval-baseline eval-heldout eval-rerank bench eval-answers eval-answers-rerank test lint

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

eval-full:       ## the same questions against the full corpus, exact search and with the HNSW index
	$(EVAL) --collection full --label full
	$(EVAL) --collection full --use-index --label full-hnsw

eval-baseline:   ## fixed-size chunks and the untuned threshold
	$(EVAL) --collection core-fixed --threshold 0.5 --strict-threshold 0 --label core-baseline

eval-heldout:    ## the two held-out question sets; EVAL.md says how far each one is held out
	$(EVAL) $(HELDOUT) --collection core --label heldout-core
	$(EVAL) $(HELDOUT) --collection full --label heldout-full
	$(EVAL) $(HELDOUT2) --collection core --label heldout2-core
	$(EVAL) $(HELDOUT2) --collection full --label heldout2-full

eval-rerank:     ## the same runs with the optional reranker switched on
	$(EVAL) --rerank --collection core --label core-rerank
	$(EVAL) --rerank --collection full --label full-rerank
	$(EVAL) --rerank $(HELDOUT) --collection core --label heldout-core-rerank
	$(EVAL) --rerank $(HELDOUT) --collection full --label heldout-full-rerank
	$(EVAL) --rerank $(HELDOUT2) --collection core --label heldout2-core-rerank
	$(EVAL) --rerank $(HELDOUT2) --collection full --label heldout2-full-rerank

bench:           ## query latency and storage size: exact search, HNSW index, and the optional reranker
	$(PY) -m ragdemo.bench --collection core --with-index --with-rerank --label bench-core
	$(PY) -m ragdemo.bench --collection full --with-index --with-rerank --label bench-full

eval-answers:    ## generated answers graded for correctness and faithfulness; needs OPENAI_API_KEY in the environment
	$(ANSWERS) --collection core --label answers-core
	$(ANSWERS) --collection full --label answers-full
	$(ANSWERS) $(HELDOUT) --collection core --label answers-heldout-core
	$(ANSWERS) $(HELDOUT) --collection full --label answers-heldout-full
	$(ANSWERS) $(HELDOUT2) --collection core --label answers-heldout2-core
	$(ANSWERS) $(HELDOUT2) --collection full --label answers-heldout2-full

eval-answers-rerank: ## the same six runs with the optional reranker switched on
	$(ANSWERS) --rerank --collection core --label answers-core-rerank
	$(ANSWERS) --rerank --collection full --label answers-full-rerank
	$(ANSWERS) --rerank $(HELDOUT) --collection core --label answers-heldout-core-rerank
	$(ANSWERS) --rerank $(HELDOUT) --collection full --label answers-heldout-full-rerank
	$(ANSWERS) --rerank $(HELDOUT2) --collection core --label answers-heldout2-core-rerank
	$(ANSWERS) --rerank $(HELDOUT2) --collection full --label answers-heldout2-full-rerank

test:            ## needs a Postgres with pgvector at DATABASE_URL (the compose db is published on localhost)
	pytest -q

lint:
	ruff check .
