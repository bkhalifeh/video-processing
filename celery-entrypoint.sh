#!/bin/sh
uv run celery -A app.tasks.video_tasks.celery_app worker --concurrency=100 --loglevel=INFO
