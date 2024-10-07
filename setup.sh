#!/bin/bash

export ZENDESK_USER="founders@cirroe.com"
export ZENDESK_TOKEN="8TnhiwemDGvSSKHQRmjqewGjTpnMqw8aTBPgpTqz"
export ZENDESK_SUBDOMAIN="cirroe"

python3.11 -m venv .zdenv
source .zdenv/bin/activate

pip3 install --upgrade pip

pip3 install llama-index
pip3 install llama_index_core
pip3 install llama-index-embeddings-huggingface

# For finding close tickets
pip3 install --q chromadb haystack-ai jina-haystack chroma-haystack

# For clustering
pip3 install umap-learn
pip3 install hdbscan
python3 -m pip3 install -U matplotlib

# Everything else
pip3 install seaborn