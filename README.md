# Italian Podcast Generator

Auto-generated Italian learning podcast episodes in Michel Thomas style.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- OpenAI API key

## Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (uv will create venv automatically)
uv sync

# Configure API keys
cp .env.example .env
# Edit .env with your OpenAI API key

# Generate first episode
uv run generate.py
```

## Phase 1 - MVP

Simple single-script approach:
- Hard-coded vocabulary for first episodes
- OpenAI GPT-4o-mini for script generation
- OpenAI TTS for Italian audio
- Manual deployment

## Status

Currently in initial development.

