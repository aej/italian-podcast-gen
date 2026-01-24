#!/usr/bin/env python3
"""
Italian Podcast Generator - MVP Version

Generates a Michel Thomas style Italian learning podcast episode.
Phase 1: Simple hard-coded approach to validate the concept.
"""

import os
import sys
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TEACHER_VOICE = os.getenv('TEACHER_VOICE', 'alloy')
STUDENT_VOICE = os.getenv('STUDENT_VOICE', 'nova')
TARGET_DURATION = int(os.getenv('TARGET_DURATION_MINUTES', 15))

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Hard-coded vocabulary for Phase 1
# TODO: Later, parse from /areas/italian/vocabulary.md
VOCAB_WORDS = [
    {"word": "mangiare", "meaning": "to eat", "type": "verb"},
    {"word": "bere", "meaning": "to drink", "type": "verb"},
    {"word": "parlare", "meaning": "to speak", "type": "verb"},
    {"word": "guardare", "meaning": "to watch", "type": "verb"},
    {"word": "ascoltare", "meaning": "to listen", "type": "verb"},
    {"word": "la pizza", "meaning": "pizza", "type": "noun"},
    {"word": "l'acqua", "meaning": "water", "type": "noun"},
    {"word": "il caffè", "meaning": "coffee", "type": "noun"},
]


def build_prompt(vocab_list):
    """Build the LLM prompt for episode generation."""

    vocab_str = "\n".join([f"- {v['word']} ({v['meaning']})" for v in vocab_list])

    prompt = f"""You are creating an Italian language learning podcast episode in the style of Michel Thomas.

The Michel Thomas method features:
- Patient, encouraging teacher
- Student (named Alex) who makes natural mistakes and gets corrected
- Progressive building of sentences
- Grammar explanations in simple English
- Lots of Italian practice with immediate feedback
- Confidence-building approach

VOCABULARY TO COVER:
{vocab_str}

EPISODE STRUCTURE:

1. Opening (30 seconds)
   - Teacher greets Alex warmly in Italian and English
   - Preview today's vocabulary

2. Vocabulary Introduction (3-4 minutes)
   - Introduce each word with pronunciation
   - Give context and usage examples
   - Teacher models, Alex repeats

3. Practice Sentences (6-8 minutes)
   - Teacher asks Alex to build simple sentences
   - Alex makes 2-3 natural beginner mistakes
   - Teacher corrects gently with explanation
   - Focus on present tense -are verbs

4. Dialogue Practice (4-5 minutes)
   - Natural conversation using today's words
   - Scenario: ordering at a café
   - Alex gets more confident through practice

5. Summary (1 minute)
   - Recap key words
   - Encourage Alex
   - "Ottimo lavoro! See you next time."

TARGET LENGTH: {TARGET_DURATION} minutes of spoken dialogue (approximately {TARGET_DURATION * 150} words)

OUTPUT FORMAT:
Write the complete dialogue as a conversation between TEACHER and STUDENT (Alex).
Each line should start with "TEACHER:" or "STUDENT:".
Include both English and Italian naturally in the dialogue (bilingual mix).
Make sure the student's mistakes are realistic for A1-A2 level.

Generate the complete episode dialogue now."""

    return prompt


def generate_script(vocab_list):
    """Generate episode script using GPT-4o-mini."""

    print("📝 Generating episode script...")

    prompt = build_prompt(vocab_list)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Italian language teacher who uses the Michel Thomas method."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        script = response.choices[0].message.content
        print(f"✅ Script generated ({len(script)} characters)")
        return script

    except Exception as e:
        print(f"❌ Error generating script: {e}")
        sys.exit(1)


def parse_dialogue(script):
    """Parse script into teacher/student lines."""

    lines = []
    for line in script.split('\n'):
        line = line.strip()
        if line.startswith('TEACHER:'):
            text = line.replace('TEACHER:', '').strip()
            lines.append(('TEACHER', text))
        elif line.startswith('STUDENT:'):
            text = line.replace('STUDENT:', '').strip()
            lines.append(('STUDENT', text))

    print(f"📋 Parsed {len(lines)} dialogue lines")
    return lines


def generate_audio(dialogue_lines, output_path):
    """Generate audio using OpenAI TTS."""

    print("🎙️  Generating audio...")

    # Create episodes directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # For Phase 1: Generate one continuous audio file
    # Combine all lines into one script with pauses
    full_script = ""
    for speaker, text in dialogue_lines:
        if not text:  # Skip empty lines
            continue
        full_script += text + "... "  # Add pause between lines

    try:
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=TEACHER_VOICE,  # Using teacher voice for full episode in Phase 1
            input=full_script
        )

        # Save to file
        response.stream_to_file(str(output_path))

        print(f"✅ Audio saved to {output_path}")

    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        sys.exit(1)


def main():
    """Main execution flow."""

    print("=" * 60)
    print("Italian Podcast Generator - MVP")
    print("=" * 60)

    # Check API key
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        print("Please copy .env.example to .env and add your API key")
        sys.exit(1)

    # Get episode number (count existing episodes)
    episodes_dir = Path("episodes")
    episodes_dir.mkdir(exist_ok=True)
    existing_episodes = list(episodes_dir.glob("episode-*.mp3"))
    episode_num = len(existing_episodes) + 1

    print(f"\n🎬 Generating Episode {episode_num}")
    print(f"📅 Date: {date.today()}")
    print(f"📚 Vocabulary: {len(VOCAB_WORDS)} words\n")

    # Step 1: Generate script
    script = generate_script(VOCAB_WORDS)

    # Step 2: Parse dialogue
    dialogue = parse_dialogue(script)

    # Step 3: Generate audio
    output_file = episodes_dir / f"episode-{episode_num:03d}.mp3"
    generate_audio(dialogue, output_file)

    # Step 4: Save script for reference
    script_file = episodes_dir / f"episode-{episode_num:03d}-script.txt"
    with open(script_file, 'w') as f:
        f.write(script)
    print(f"📄 Script saved to {script_file}")

    print("\n" + "=" * 60)
    print("✨ Episode generation complete!")
    print("=" * 60)
    print(f"\n🎧 Listen to: {output_file}")
    print(f"📖 Read script: {script_file}")
    print("\nNext steps:")
    print("1. Listen to the episode")
    print("2. Evaluate quality (voice, content, pacing)")
    print("3. Run again to generate more test episodes")
    print("4. Once validated, proceed to Phase 2 improvements")


if __name__ == "__main__":
    main()
