#!/bin/bash

alembic upgrade head

export PYTHONPATH=src 

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
