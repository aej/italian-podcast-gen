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
from elevenlabs import ElevenLabs, VoiceSettings

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# ElevenLabs voice configuration
# You can find voice IDs at: https://elevenlabs.io/voice-library
# Or use voice names (will auto-lookup)
TEACHER_VOICE_ID = os.getenv('TEACHER_VOICE_ID', os.getenv('TEACHER_VOICE_NAME'))
STUDENT_VOICE_ID = os.getenv('STUDENT_VOICE_ID', os.getenv('STUDENT_VOICE_NAME'))

TARGET_DURATION = int(os.getenv('TARGET_DURATION_MINUTES', 15))

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

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

    # Limit to first 4 items for better learning
    vocab_list = vocab_list[:4]
    vocab_str = "\n".join([f"- {v['word']} ({v['meaning']})" for v in vocab_list])

    prompt = f"""You are creating an Italian language learning podcast episode in the style of Michel Thomas.

The Michel Thomas method features:
- Patient, encouraging teacher
- Student (named Alex) who makes natural mistakes and gets corrected
- Progressive building of sentences
- Grammar explanations in simple English
- Lots of Italian practice with immediate feedback
- Confidence-building approach
- PAUSES after questions so listeners can attempt answers themselves

VOCABULARY TO COVER (introduce one at a time, NOT all at once):
{vocab_str}

CRITICAL LANGUAGE RULES:

1. TEACHER speaks:
   - English for instructions and explanations
   - Italian for demonstrations and examples
   - Example: "In Italian, 'to eat' is 'mangiare.' Listen: Io mangio la pizza."

2. STUDENT (Alex) speaks:
   - PRIMARILY ITALIAN when practicing vocabulary and sentences
   - May ask clarification questions in English ("What does that mean?")
   - NEVER translates Italian back to English as a response
   - NEVER mixes English and Italian in the same phrase
   - Makes realistic A1 mistakes in Italian grammar/pronunciation

3. After EVERY teacher question, include: [PAUSE X seconds]
   - After questions requiring construction: [PAUSE 7 seconds]
   - After repetition requests: [PAUSE 4 seconds]
   - After student response: [PAUSE 3 seconds]

INCORRECT EXAMPLE (DO NOT DO THIS):
TEACHER: "Io mangio la pizza" means "I eat pizza."
STUDENT: I eat pizza.  ❌ NO - Student is just translating

CORRECT EXAMPLE (DO THIS):
TEACHER: "Io mangio la pizza." Can you repeat that?
[PAUSE 4 seconds]
STUDENT: Io mangio la pizza.  ✅ YES - Student is practicing Italian
TEACHER: Excellent pronunciation!

EPISODE STRUCTURE:

1. Opening (1 minute)
   - Teacher greets Alex warmly: "Ciao, Alex!"
   - Brief intro in English about today's focus
   - DO NOT list all vocabulary upfront

2. Vocabulary Introduction (8-10 minutes)
   - Introduce ONE word at a time with pronunciation
   - Teacher models the Italian word
   - [PAUSE] - Alex repeats in Italian
   - Give context and usage example in Italian
   - [PAUSE] - Alex attempts to use it
   - Explain grammar patterns (e.g., "-are verbs: drop -are, add -o for 'I'")
   - Build to simple sentences gradually

3. Practice Sentences (6-8 minutes)
   - Teacher asks Alex to construct sentences in Italian
   - [PAUSE 7 seconds] before Alex attempts
   - Alex makes 2-3 natural beginner mistakes IN ITALIAN
   - Teacher corrects gently with explanation
   - Focus on present tense -are verbs conjugation pattern

4. Dialogue Practice (3-4 minutes)
   - Simple café scenario
   - Teacher asks "How would you say [X] in Italian?"
   - [PAUSE 7 seconds] - Alex attempts IN ITALIAN
   - Teacher provides gentle corrections
   - Alex should speak Italian phrases, not English

5. Summary (1 minute)
   - Quick recap of the words learned
   - Encourage Alex
   - "Ottimo lavoro! A presto!" (See you soon!)

TARGET LENGTH: {TARGET_DURATION} minutes of spoken dialogue (approximately {TARGET_DURATION * 200} words)

GRAMMAR FOCUS:
- Explain the -are verb conjugation pattern explicitly
- Show how "mangiare" becomes "mangio" (I eat)
- Have Alex discover the pattern with guidance

OUTPUT FORMAT:
Write the complete dialogue as a conversation between TEACHER and STUDENT (Alex).
Each line should start with "TEACHER:" or "STUDENT:" (no bold formatting).
Include [PAUSE X seconds] after every question.
Make sure Alex speaks ITALIAN when practicing, not English translations.
Make sure Alex's mistakes are realistic Italian grammar errors (wrong verb form, wrong article), not code-switching.

Generate the complete episode dialogue now."""

    return prompt


def generate_script(vocab_list):
    """Generate episode script using GPT-4o-mini."""

    print("📝 Generating episode script...")

    prompt = build_prompt(vocab_list)

    try:
        response = openai_client.chat.completions.create(
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
    """Parse script into teacher/student lines and pause markers."""

    lines = []
    for line in script.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Check for pause markers
        if '[PAUSE' in line and 'seconds]' in line:
            # Extract just the pause marker
            pause_marker = line[line.index('[PAUSE'):line.index('seconds]')+8]
            lines.append(('PAUSE', pause_marker))
            continue

        # Remove markdown bold formatting if present
        line = line.replace('**', '')

        # Try multiple formats that GPT might use
        if line.startswith('TEACHER:') or line.startswith('Teacher:'):
            text = line.replace('TEACHER:', '').replace('Teacher:', '').strip()
            if text:
                lines.append(('TEACHER', text))
        elif line.startswith('STUDENT:') or line.startswith('Student:') or line.startswith('ALEX:') or line.startswith('Alex:'):
            text = line.replace('STUDENT:', '').replace('Student:', '').replace('ALEX:', '').replace('Alex:', '').strip()
            if text:
                lines.append(('STUDENT', text))

    dialogue_count = sum(1 for s, _ in lines if s in ['TEACHER', 'STUDENT'])
    pause_count = sum(1 for s, _ in lines if s == 'PAUSE')
    print(f"📋 Parsed {dialogue_count} dialogue lines + {pause_count} pauses")

    if dialogue_count == 0:
        print("⚠️  WARNING: No dialogue lines parsed!")
        print("Script preview (first 500 chars):")
        print(script[:500])
        print("\n💡 The script will be saved for inspection.")

    return lines


def generate_audio(dialogue_lines, output_path):
    """Generate audio using ElevenLabs TTS with pauses."""

    print("🎙️  Generating audio with ElevenLabs...")

    # Create episodes directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Import audio library for combining segments
    from pydub import AudioSegment
    import io

    # Build combined audio with pauses
    combined = AudioSegment.empty()
    segment_count = 0

    # Voice settings optimized for multilingual content
    voice_settings = VoiceSettings(
        stability=0.5,  # More stable for language learning
        similarity_boost=0.75,  # Keep voice consistent
        style=0.0,  # Neutral style
        use_speaker_boost=True  # Enhance clarity
    )

    for speaker, text in dialogue_lines:
        if not text:  # Skip empty lines
            continue

        # Check if this is a pause marker
        if text.startswith('[PAUSE') and 'seconds]' in text:
            # Extract pause duration
            try:
                duration = int(text.split('[PAUSE')[1].split('seconds]')[0].strip())
                silence = AudioSegment.silent(duration=duration * 1000)  # Convert to milliseconds
                combined += silence
                print(f"  Added {duration}s pause")
            except:
                # If parsing fails, add default 3 second pause
                combined += AudioSegment.silent(duration=3000)
                print(f"  Added 3s pause (default)")
            continue

        # Select voice based on speaker
        voice_id = TEACHER_VOICE_ID if speaker == 'TEACHER' else STUDENT_VOICE_ID

        try:
            # Generate speech for this segment using ElevenLabs
            audio_generator = elevenlabs_client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_multilingual_v2",  # Best for Italian/English mix
                voice_settings=voice_settings,
            )

            # Collect audio chunks
            audio_chunks = b""
            for chunk in audio_generator:
                audio_chunks += chunk

            # Load audio data into pydub
            segment = AudioSegment.from_mp3(io.BytesIO(audio_chunks))
            combined += segment
            segment_count += 1
            print(f"  Generated segment {segment_count} ({speaker}): {len(text)} chars")

        except Exception as e:
            print(f"❌ Error generating segment: {e}")
            print(f"   Speaker: {speaker}, Voice ID: {voice_id}")
            print(f"   Text: {text[:100]}...")
            sys.exit(1)

    # Export final combined audio
    try:
        combined.export(str(output_path), format="mp3")
        duration_minutes = len(combined) / 1000 / 60
        print(f"✅ Audio saved to {output_path}")
        print(f"   Duration: {duration_minutes:.1f} minutes ({segment_count} segments)")

    except Exception as e:
        print(f"❌ Error saving audio: {e}")
        sys.exit(1)


def main():
    """Main execution flow."""

    print("=" * 60)
    print("Italian Podcast Generator - MVP")
    print("=" * 60)

    # Check API keys
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        print("Please copy .env.example to .env and add your OpenAI API key")
        sys.exit(1)

    if not ELEVENLABS_API_KEY:
        print("❌ Error: ELEVENLABS_API_KEY not set in .env file")
        print("Please add your ElevenLabs API key to .env")
        print("Get one at: https://elevenlabs.io/")
        sys.exit(1)

    if not TEACHER_VOICE_ID or not STUDENT_VOICE_ID:
        print("❌ Error: Voice IDs not set in .env file")
        print("Please set TEACHER_VOICE_ID and STUDENT_VOICE_ID")
        print("Browse voices at: https://elevenlabs.io/voice-library")
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

    # Step 2: Save script FIRST (so we can inspect if parsing fails)
    script_file = episodes_dir / f"episode-{episode_num:03d}-script.txt"
    with open(script_file, 'w') as f:
        f.write(script)
    print(f"📄 Script saved to {script_file}")

    # Step 3: Parse dialogue
    dialogue = parse_dialogue(script)

    # If parsing failed, fall back to using entire script as one block
    if len(dialogue) == 0:
        print("⚠️  Falling back to using entire script for audio generation")
        dialogue = [('TEACHER', script)]

    # Step 4: Generate audio
    output_file = episodes_dir / f"episode-{episode_num:03d}.mp3"
    generate_audio(dialogue, output_file)

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
