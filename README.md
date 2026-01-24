# Italian Podcast Generator

Auto-generated Italian learning podcast episodes in Michel Thomas style.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OpenAI API key

# Generate first episode
python generate.py
```

## Phase 1 - MVP

Simple single-script approach:
- Hard-coded vocabulary for first episodes
- OpenAI GPT-4o-mini for script generation
- OpenAI TTS for Italian audio
- Manual deployment

## Status

Currently in initial development.

