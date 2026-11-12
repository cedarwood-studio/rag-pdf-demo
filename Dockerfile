FROM docker.io/library/python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FASTEMBED_CACHE_PATH=/opt/fastembed

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download the embedding model at build time so the container starts without network access to the model hub.
# The optional reranker model is not baked in: it is downloaded on first use when RERANK=1.
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='BAAI/bge-small-en-v1.5')"

COPY ragdemo ragdemo
COPY corpus corpus
COPY eval/*.json eval/

EXPOSE 8000
# First start downloads the core PDFs and ingests them (9 to 10 minutes on a 4-core CPU); later starts skip straight to serving.
# A first start that was interrupted is ingested again from the start.
CMD ["sh", "-c", "python -m ragdemo.ingest --unless-complete && exec uvicorn ragdemo.api:app --host 0.0.0.0 --port 8000"]
