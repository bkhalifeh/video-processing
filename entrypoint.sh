#!/bin/sh
uv run alembic upgrade head
uv run fastapi run --port 80