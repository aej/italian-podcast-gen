# Changelog

## 2026-01-24 - Switch to ElevenLabs TTS

### Major Change: Replaced OpenAI TTS with ElevenLabs

#### Why?
- **Better Italian pronunciation** - ElevenLabs has native Italian voices
- **Multilingual support** - Seamless switching between Italian and English
- **Higher quality** - More natural-sounding speech for language learning
- **Voice variety** - Access to 100+ voices including authentic Italian speakers

#### Technical Changes

**Dependencies:**
- Added `elevenlabs>=1.0.0` to pyproject.toml
- Kept `openai` for script generation (GPT-4o-mini)

**Configuration:**
- New env vars: `ELEVENLABS_API_KEY`, `TEACHER_VOICE_ID`, `STUDENT_VOICE_ID`
- Removed: `TEACHER_VOICE`, `STUDENT_VOICE` (OpenAI voice names)

**Code Changes:**
- `generate.py`: Updated `generate_audio()` function to use ElevenLabs API
- Using `eleven_multilingual_v2` model for best Italian/English handling
- Voice settings optimized for language learning (stability, clarity, neutral style)

**Documentation:**
- Updated README with ElevenLabs setup instructions
- Created `ELEVENLABS-SETUP.md` with detailed guide
- Updated `.env.example` with voice ID examples

#### Migration Steps

For users upgrading from OpenAI TTS:

```bash
# 1. Update dependencies
uv sync

# 2. Get ElevenLabs API key from elevenlabs.io

# 3. Choose voices from voice library
# Visit: https://elevenlabs.io/voice-library

# 4. Update .env file with:
ELEVENLABS_API_KEY=your_key
TEACHER_VOICE_ID=voice_id_here
STUDENT_VOICE_ID=voice_id_here

# 5. Generate new episode
uv run generate.py
```

#### Recommended Voices

- **Teacher**: Valentino, Gianni, or Luca (native Italian)
- **Student**: Adam, Domi, or Chris (multilingual, sounds like learner)

See `ELEVENLABS-SETUP.md` for detailed voice selection guide.

---

## 2026-01-24 - Major Improvements Based on Episode 001 Feedback

### Fixed Issues

#### 🔴 Critical: Script Language Mixing
- **Problem:** Student was translating Italian to English instead of practicing Italian
- **Fix:** Updated prompt with explicit language rules:
  - Teacher speaks English for instruction, Italian for demonstration
  - Student speaks ITALIAN when practicing (not English translations)
  - No code-switching allowed
  - Added examples of correct vs incorrect dialogue format

#### 🔴 Critical: Missing Pauses
- **Problem:** No thinking time for listeners between questions and answers
- **Fix:**
  - Updated prompt to require `[PAUSE X seconds]` markers
  - Updated parser to recognize pause markers
  - Updated audio generation to insert actual silence:
    - 7 seconds after construction questions
    - 4 seconds after repetition requests
    - 3 seconds after student responses
  - Now uses separate TTS calls per dialogue line to insert pauses
  - Uses different voices for teacher vs student

#### 🟡 Major: Episode Too Short
- **Problem:** Episode was shorter than 15 minute target
- **Fix:**
  - Increased word count target from 150 words/min to 200 words/min
  - Added longer pause durations which extend total time
  - Increased vocabulary introduction section to 8-10 minutes

#### 🟡 Major: Too Much Vocabulary at Once
- **Problem:** Listed all 8 words upfront, overwhelming
- **Fix:**
  - Limited to 4 words maximum per episode
  - Removed upfront vocabulary list
  - Introduce words one at a time
  - Focus on depth over breadth

#### 🟢 Minor: Missing Grammar Explanations
- **Problem:** No explanation of -are verb conjugation pattern
- **Fix:** Added explicit grammar instruction to prompt:
  - Explain "-are verbs: drop -are, add -o for 'I'"
  - Have student discover patterns
  - Build understanding progressively

### Technical Changes

#### Audio Generation
- **New:** Multi-segment audio generation with pydub
- **New:** Pause marker parsing and silence insertion
- **New:** Separate voices for teacher (alloy) and student (nova)
- **New:** Duration reporting after generation

#### Dependencies
- **Added:** pydub for audio manipulation
- **Required:** ffmpeg for pydub backend
- **Updated:** README with installation instructions

#### Prompt Engineering
- **Major rewrite** of GPT prompt with:
  - Explicit language rules section
  - INCORRECT/CORRECT examples
  - Pause marker requirements
  - Grammar teaching instructions
  - No bold formatting instruction

### Known Issues / Future Work

#### Voice Accent (Not Fixed Yet)
- **Issue:** OpenAI voices are English-trained, sound American
- **Status:** Added documentation about alternative TTS providers
- **Options to explore:**
  - Test all 6 OpenAI voices for best Italian pronunciation
  - Integrate ElevenLabs API (better multilingual)
  - Integrate Google Cloud TTS (native Italian voices)
  - Integrate Azure TTS (native Italian voices)

### Files Modified

- `generate.py` - Major updates to prompt, parser, and audio generation
- `README.md` - Added ffmpeg requirement and voice testing instructions
- `FEEDBACK-2026-01-24.md` - Created
- `EPISODE-001-ANALYSIS.md` - Created
- `CHANGELOG.md` - Created (this file)

### Testing Needed

Before generating Episode 002:
1. ✅ Install ffmpeg: `brew install ffmpeg`
2. ✅ Install pydub: `uv pip install pydub`
3. ⏳ Run: `uv run generate.py`
4. ⏳ Verify episode-002.mp3 has:
   - Pauses between dialogue
   - Student speaking Italian (not English)
   - Different voices for teacher/student
   - ~15 minute duration
   - Only 4 vocabulary words
   - Grammar pattern explanation

### Success Criteria for Episode 002

- [x] Prompt updated with language rules
- [x] Pause markers in generated script
- [x] Audio generation handles pauses
- [x] Separate voices for teacher/student
- [ ] Episode duration ~15 minutes
- [ ] Student speaks Italian, not English
- [ ] No code-switching
- [ ] Grammar explanation included
- [ ] Max 4 vocabulary items
- [ ] Natural pacing with thinking time
