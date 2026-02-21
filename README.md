# Italian Podcast Generator

Auto-generated Italian learning podcast episodes in Michel Thomas style.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- OpenAI API key (for script generation)
- ElevenLabs API key (for Italian TTS)
- [ffmpeg](https://ffmpeg.org/) - Required for audio processing
  - macOS: `brew install ffmpeg`
  - Ubuntu: `apt-get install ffmpeg`

## Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install ffmpeg (macOS)
brew install ffmpeg

# Sync dependencies (uv will create venv automatically)
uv sync

# Configure API keys
cp .env.example .env
# Edit .env and add:
# - Your OpenAI API key (for script generation)
# - Your ElevenLabs API key (get one at https://elevenlabs.io/)
# - ElevenLabs voice IDs for teacher and student

# Generate first episode
uv run generate.py
```

## ElevenLabs Voice Selection

This project uses ElevenLabs for high-quality multilingual TTS with authentic Italian pronunciation.

### Finding Voice IDs

1. Visit the [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
2. Browse for Italian voices or multilingual voices that handle Italian well
3. Recommended voices:
   - **Valentino** - Native Italian male voice
   - **Gianni** - Native Italian male voice
   - **Domi** - Multilingual voice (good for mixed Italian/English)
   - **Adam** - Clear multilingual voice (good for student)

4. Click on a voice to hear samples
5. Copy the voice ID from the URL or voice details

### Configuring Voices

Edit your `.env` file:
```bash
# Example with Italian voices
TEACHER_VOICE_ID=XB0fDUnXU5powFXDhCwa  # Valentino (Italian teacher)
STUDENT_VOICE_ID=pNInz6obpgDQGcFmaJgB  # Adam (student learning)

# Or use voice names (will auto-lookup)
TEACHER_VOICE_NAME=Valentino
STUDENT_VOICE_NAME=Adam
```

### Voice Settings

The generator uses optimized settings for language learning:
- **Stability**: 0.5 (more consistent pronunciation)
- **Similarity Boost**: 0.75 (maintains voice character)
- **Style**: 0.0 (neutral, clear speech)
- **Speaker Boost**: Enabled (enhanced clarity)
- **Model**: `eleven_multilingual_v2` (best for Italian/English mix)

## Phase 1 - MVP

Simple single-script approach:
- Hard-coded vocabulary for first episodes
- OpenAI GPT-4o-mini for script generation
- OpenAI TTS for Italian audio
- Manual deployment

## Status

Currently in initial development.

