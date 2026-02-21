# ElevenLabs Setup Guide

This project uses ElevenLabs for high-quality Italian text-to-speech.

## Why ElevenLabs?

- **Native Italian voices** - Authentic pronunciation and accent
- **Multilingual models** - Seamless switching between Italian and English
- **High quality** - Natural-sounding speech ideal for language learning
- **Voice cloning** - Option to create custom voices in the future

## Getting Started

### 1. Create an Account

1. Visit [elevenlabs.io](https://elevenlabs.io/)
2. Sign up for a free account
   - Free tier: 10,000 characters/month
   - Starter plan: $5/month for 30,000 characters
   - For daily 15-minute episodes, recommend Starter plan or higher

### 2. Get Your API Key

1. Go to your [Profile Settings](https://elevenlabs.io/app/settings)
2. Click on "API Keys" tab
3. Copy your API key
4. Add to `.env`:
   ```bash
   ELEVENLABS_API_KEY=your_api_key_here
   ```

### 3. Choose Voices

#### Option A: Browse the Voice Library

1. Visit the [Voice Library](https://elevenlabs.io/voice-library)
2. Filter by language: Italian
3. Listen to samples
4. Click on a voice you like
5. Copy the voice ID from the page

#### Option B: Recommended Voices for Italian Learning

**For Teacher (Italian native speaker):**
- **Valentino** - Warm Italian male voice, clear pronunciation
- **Gianni** - Professional Italian male voice
- **Luca** - Younger Italian male voice

**For Student (learning Italian):**
- **Adam** - Clear multilingual voice (sounds like native English speaker)
- **Domi** - Female multilingual voice
- **Chris** - Male multilingual voice

### 4. Configure Your .env File

```bash
# ElevenLabs API Configuration
ELEVENLABS_API_KEY=sk_abc123...  # Your API key from step 2

# Voice IDs from step 3
TEACHER_VOICE_ID=XB0fDUnXU5powFXDhCwa  # Replace with your chosen teacher voice
STUDENT_VOICE_ID=pNInz6obpgDQGcFmaJgB  # Replace with your chosen student voice
```

## Finding the Right Voice ID

### Method 1: Voice Library

1. Go to [Voice Library](https://elevenlabs.io/voice-library)
2. Click on any voice
3. The voice ID is in the URL: `elevenlabs.io/voice-library/[VOICE_ID]`
4. Or click "Add to VoiceLab" and find ID in your VoiceLab

### Method 2: Using the Python Library

You can also list available voices programmatically:

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_api_key")
voices = client.voices.get_all()

for voice in voices.voices:
    print(f"{voice.name}: {voice.voice_id}")
    print(f"  Labels: {voice.labels}")
    print(f"  Category: {voice.category}")
    print()
```

## Testing Your Setup

After configuring your `.env`, test with:

```bash
cd ~/projects/italian-podcast-gen
uv run generate.py
```

The script will:
1. Check for your API keys
2. Generate an episode script
3. Convert it to speech using ElevenLabs
4. Save the audio file

## Cost Estimation

Episode costs (approximate):
- 15-minute episode ≈ 3,000-4,000 words ≈ 15,000-20,000 characters
- Free tier: ~1 episode every 2 months
- Starter ($5/month): ~1-2 episodes/month
- Creator ($22/month): ~7-10 episodes/month
- Pro ($99/month): ~33 episodes/month

For daily episodes, recommend Creator plan or higher.

## Troubleshooting

### "Invalid voice_id" error

- Double-check the voice ID in your `.env` file
- Make sure there are no extra spaces
- Verify the voice exists in your account's available voices

### "Quota exceeded" error

- Check your usage at [elevenlabs.io/app/usage](https://elevenlabs.io/app/usage)
- Upgrade your plan if needed
- Free tier resets monthly

### "API key invalid" error

- Regenerate your API key in profile settings
- Make sure you copied the entire key
- Check for extra spaces in `.env` file

## Advanced: Voice Settings

The generator uses these settings (in `generate.py`):

```python
VoiceSettings(
    stability=0.5,           # How stable/consistent (0-1)
    similarity_boost=0.75,   # How closely it matches the voice (0-1)
    style=0.0,               # Exaggeration level (0-1)
    use_speaker_boost=True   # Enhance clarity
)
```

You can adjust these in the code if needed:
- **Higher stability** (0.7-0.9) = more robotic but consistent
- **Lower stability** (0.3-0.5) = more natural but variable
- **Higher style** (0.3-0.5) = more expressive
- **Lower style** (0.0) = more neutral (better for learning)

## Custom Voices (Advanced)

ElevenLabs allows voice cloning:

1. Record 1-5 minutes of clean audio of your voice
2. Upload to ElevenLabs Voice Lab
3. Create a custom voice
4. Use its voice ID in your `.env`

This could be useful for:
- Using your own voice as the student
- Creating a consistent teacher voice
- Matching a specific accent or speaking style
