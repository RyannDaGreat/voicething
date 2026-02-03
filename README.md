# VoiceThing

A fast, keyboard-driven voice transcription app for macOS, powered by Whisper with Metal GPU acceleration.

![VoiceThing Main Window](screenshots/transcriptions_tab_with_content.png)

## Table of Contents

- [Getting Started](#getting-started)
- [Recording Your Voice](#recording-your-voice)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Whisper Models](#whisper-models)
- [Wake Word Detection](#wake-word-detection)
- [LLM Post-Processing](#llm-post-processing)
- [Tmux Integration](#tmux-integration)
- [Transcription History](#transcription-history)
- [Notification Chimes](#notification-chimes)
- [Pet Companions](#pet-companions)
- [Themes](#themes)
- [Settings Reference](#settings-reference)
- [Installation](#installation)

---

## Getting Started

VoiceThing lets you record your voice and transcribe it to text instantly. The transcribed text is automatically pasted into whatever app you're using.

### Basic Workflow

1. **Double-tap the Option key (⌥⌥)** from anywhere on your Mac
2. Speak your text
3. **Double-tap Option again** to stop recording
4. Your transcribed text is automatically pasted

That's it! VoiceThing works in fullscreen apps, terminals, and anywhere else on macOS.

### Requirements

- **macOS** with Apple Silicon (M1/M2/M3/M4)
- **Python 3.10**
- **Accessibility permissions** for global keyboard shortcuts

---

## Recording Your Voice

### Double-Tap Option (⌥⌥)

The primary way to record is double-tapping the Option key:

| Action | What Happens |
|--------|--------------|
| **Double-tap ⌥** | Start recording |
| **Double-tap ⌥ again** | Stop recording and transcribe |
| **Hold ⌥ for 0.5+ seconds** on the 2nd tap | Cancel recording (no paste) |
| **Cmd + double-tap ⌥** | Toggle window focus instead of recording |
| **Press Shift** while holding ⌥ | Abort the cancel action |

When you hold the Option key too long during the second tap, you'll hear a "pre-cancel" chime warning you're about to cancel instead of transcribe.

### Spacebar Recording

When VoiceThing has focus, you can also use:

| Key | Action |
|-----|--------|
| **Space** | Start/stop recording |
| **X** | Cancel recording |

### Recording States

VoiceThing displays different states:

1. **Idle** - "Double-tap ⌥" shown, ready to record
2. **Recording** - Timer counting up, waveform showing audio levels
3. **Transcribing** - Processing your audio with Whisper

---

## Keyboard Shortcuts

VoiceThing is 100% keyboard-driven. Here are all shortcuts organized by function:

### Global Shortcuts (Work Anywhere)

These work even when VoiceThing isn't focused:

| Shortcut | Action |
|----------|--------|
| **⌥⌥** (double-tap Option) | Start/stop recording |
| **⌘ + ⌥⌥** | Toggle window focus |
| **Hold ⌥** 0.5s on 2nd tap | Cancel recording |
| **Cmd+Q** | Quit VoiceThing |

### Main Window Shortcuts

When VoiceThing window has focus:

| Key | Action | Description |
|-----|--------|-------------|
| **Space** | Toggle recording | Start or stop recording |
| **X** | Cancel | Cancel current recording (only during recording) |
| **Z** | Retranscribe | Retranscribe latest audio with current model |
| **C** | Copy | Copy last transcription to clipboard |
| **L** | Load | Load and transcribe an audio file |
| **F** | Folder | Open recordings folder in Finder |
| **Esc** | Hide | Hide/minimize the window |

### Feature Toggles

| Key | Action | Description |
|-----|--------|-------------|
| **S** | Sound | Toggle notification chimes on/off |
| **H** | Auto-hide | Toggle automatic window hiding after transcription |
| **R** | LLM | Toggle LLM post-processing (Anti-Ramble mode) |
| **J** | Wake word | Toggle wake word detection |
| **N** | Auto-enter | Toggle automatic Enter key after paste |
| **W** | Simple mode | Hide advanced buttons, show only essentials |

### Window Modes

| Key | Action | Description |
|-----|--------|-------------|
| **E** | Small mode | Toggle compact window (yellow traffic light) |
| **G** | Maximize | Toggle maximized window (green traffic light) |
| **B** | Blue mode | Toggle tmux fullscreen with floating main window |

### Navigation

| Key | Action |
|-----|--------|
| **O** | Switch to Console/Output tab |
| **T** | Switch to Transcriptions tab |
| **M** | Open Whisper model selector (disabled during recording) |
| **P** | Open Preferences dialog |
| **U** | Open Tmux Pane Manager |
| **I** | Open Chime Editor |
| **?** | Show Help dialog |
| **Ctrl+L** | Dump chime log to console (debug) |

---

## Whisper Models

Press **M** to select which Whisper model to use for transcription:

| Key | Model | Speed | Accuracy | VRAM |
|-----|-------|-------|----------|------|
| **T** | tiny | Fastest | Lowest | ~1GB |
| **B** | base | Fast | Basic | ~1GB |
| **S** | small | Balanced | Good | ~2GB |
| **M** | medium | Slower | Better | ~5GB |
| **L** | large-v3 | Slowest | Best | ~10GB |

Start with **base** for everyday use. Switch to **large-v3** when accuracy matters more than speed.

### Retranscribing

Press **Z** to retranscribe your latest recording with the current model. This lets you try different models on the same audio.

---

## Wake Word Detection

Instead of double-tapping Option, you can say a wake word to start recording. Press **J** to toggle wake word detection.

### OpenWakeWord Engine (Fast)

ML-based detection with pre-trained models. Lower CPU usage and faster response.

**Featured models:**
- alexa, computer, jarvis, hey_jarvis, hey_friday
- glados, hal, tars, hey_marvin, terminator
- 100+ community models available

**How to configure:**
1. Open Preferences (**P**)
2. Go to Wake Word section
3. Select "OpenWakeWord" engine
4. Choose your model and adjust sensitivity

### macOS Native Engine (Flexible)

Uses macOS's built-in speech recognition. Supports custom phrases.

**Features:**
- **Custom phrases** - use any words you want
- **Cancel phrases** - say "cancel" or "never mind" to abort
- **Tmux phrases** - use pane magic phrases as wake words

**How to configure:**
1. Open Preferences (**P**)
2. Go to Wake Word section
3. Select "macOS Native" engine
4. Enter your custom phrases (comma-separated)

### Using Wake Words

1. Say your wake word (e.g., "Hey Jarvis")
2. Recording starts automatically
3. Speak your text
4. Say the wake word again OR press Space to stop

---

## LLM Post-Processing

Press **R** to enable LLM post-processing (Anti-Ramble mode). This uses a local Ollama model to clean up your transcriptions.

### What It Does

| Before | After |
|--------|-------|
| "So, um, I was thinking, you know, that we should, uh, probably..." | "I was thinking that we should probably..." |
| "Set the- set the- set the deadline for Friday" | "Set the deadline for Friday" |
| "Actually wait, change that to Monday" | "Monday" |

### Cleanup Rules

1. **Remove filler words** - um, uh, "you know", filler "like"
2. **Collapse stutters** - "set the- set the-" → "set the"
3. **Apply self-corrections** - "actually change X to Y" uses Y
4. **Preserve exact words** - grammar and tense are never altered

### Special Commands

Say "VoiceThing, ..." followed by instructions to give the LLM custom directions:

- "VoiceThing, format as bullet points"
- "VoiceThing, make this more formal"

### De-ramble After Recording

You can apply LLM processing to any transcription after the fact:
1. Go to Transcriptions tab (**T**)
2. Click the hamburger menu (⋯) on any transcription
3. Press **L** for "Run LLM"

### Configuration

In Preferences (**P**), you can:
- Choose the LLM model (Ollama or OpenAI)
- Edit the prompt prefix
- Select preset prompts (Light Derambling, Few Word Do Trick)

---

## Tmux Integration

VoiceThing can send transcriptions directly to tmux panes instead of using ⌘V paste.

### Enabling Tmux Mode

1. Press **U** to open the Tmux Pane Manager
2. Click the "Enable Tmux Mode" toggle
3. Transcriptions now go to your selected tmux pane

### Tmux Pane Manager

Press **U** to open the manager. It shows:

- **Table** of all tmux sessions, windows, and panes
- **Live preview** of the selected pane's terminal output
- **Magic phrase** column for voice routing

#### Manager Shortcuts

| Key | Action |
|-----|--------|
| **U** | Toggle tmux mode on/off |
| **D** | Toggle dark/light preview theme |
| **A** | Toggle ANSI color rendering |
| **I** | Zoom in (increase font) |
| **O** | Zoom out (decrease font) |
| **S** | Toggle unlimited/limited scrollback |
| **B** | Toggle auto-scroll to bottom |
| **M** | Maximize window |
| **F** | Toggle true fullscreen (blue mode) |
| **R** | Refresh pane list |
| **Esc** | Close dialog |

#### Keyboard Passthrough

Click in the preview area to focus it, then type directly into the tmux pane. Special keys like arrows, Enter, and function keys are forwarded correctly.

### Magic Phrases

Magic phrases let you route transcriptions to specific panes by saying the phrase.

**Setting up a magic phrase:**
1. Open Tmux Pane Manager (**U**)
2. Click in the "Magic Phrase" column for a pane
3. Type a word (e.g., "chicken")
4. Press Enter

**Using magic phrases:**
- Say "chicken, run the tests"
- VoiceThing detects "chicken" and routes to that pane
- The pane receives "run the tests" (phrase stripped)

**Rules:**
- Each phrase can only be assigned to ONE pane
- Duplicate phrases are automatically removed from other panes
- First matching phrase in your transcription wins

### Stale Panes

After restarting tmux, old panes may no longer exist but their magic phrases remain. These appear with ❌ Invalid address. To remove: click the phrase, clear it, press Enter.

### Blue Mode

Press **B** to enter blue mode:
- Tmux Pane Manager goes fullscreen
- VoiceThing main window floats on top
- Great for terminal-focused workflow

---

## Transcription History

Press **T** to view your transcription history.

### Viewing Transcriptions

Each transcription shows:
- **Raw text** (dimmed) - original Whisper output
- **Processed text** (bright) - LLM-cleaned version (if LLM was enabled)

Hover over a transcription to see diff highlighting between raw and processed versions.

### Transcription Actions

Click the hamburger menu (⋯) on any transcription:

| Key | Action | Description |
|-----|--------|-------------|
| **C** | Copy | Copy to clipboard |
| **T** | Send to Tmux | Route to a tmux pane |
| **P** | Play Audio | Play original recording |
| **R** | Re-transcribe | Transcribe again with current model |
| **L** | Run LLM | Apply LLM post-processing |
| **A** | Open Audio File | Show audio file in Finder |
| **O** | Open Transcript | Show transcript file in Finder |

### Quick Copy

Click directly on any transcription text to copy it immediately.

### File Storage

- **Recordings folder** - Audio files (.wav) and temporary transcripts
- **Transcriptions folder** - Permanent text archive

Both folders are configurable in Preferences.

---

## Notification Chimes

VoiceThing plays audio feedback chimes for various events.

### Toggle Sound

Press **S** to toggle all chimes on/off.

### Chime Events

| Event | When It Plays |
|-------|---------------|
| focus | Window gains focus |
| unfocus | Window loses focus |
| copy | Text copied to clipboard |
| delete | Transcription deleted |
| enter | Enter key pressed after paste |
| cancel | Recording cancelled |
| pre_cancel | Warning before cancel (holding Option too long) |
| wake_word_start | Wake word detection enabled |
| wake_word_stop | Wake word detection disabled |
| transcribe | Transcription complete |
| null_text | Empty transcription result |
| llm_start | LLM processing started |
| llm_done | LLM processing complete |
| tmux_send | Text sent to tmux pane |

### Chime Settings

In Preferences (**P**), find the "Notification Chimes" section:

- **Volume knob** - Adjust volume (0-100%)
- **Pitch knob** - Shift pitch (-24 to +24 semitones)
- **Reverb knob** - Add reverb effect
- **Chorus knob** - Add chorus/shimmer effect
- **Instrument grid** - Choose from 24 synth instruments
- **Chime Style dropdown** - Select musical theme

### Chime Themes

Available themes with different musical styles:
- **default** - Original VoiceThing chimes
- **minimal** - Clean single notes
- **blues** - Blues scale with blue notes
- **ethereal** - Sus2/Sus4 voicings
- **melancholy** - Natural minor scale
- **bright** - Major scale
- **jazzy** - Extended chords with 7ths

### Chime Editor

Press **I** to open the Chime Editor and create custom patterns:

| Shortcut | Action |
|----------|--------|
| **Space** | Play current pattern |
| **⌘Z** | Undo |
| **⌘Y** | Redo |
| **⌘P** | Pencil mode (click to place notes) |
| **⌘B** | Brush mode (paint notes) |
| **⌘S** | Save custom pattern |
| **⌘+** / **⌘-** | Zoom in/out |
| **G** | Maximize window |

Use the piano keyboard (QWERTY layout) to play notes while editing.

---

## Pet Companions

Optional animated pets that react to app activity.

### Enable Pets

In Preferences (**P**), find the "Pet Companions" section and click pet icons to enable/disable.

### Available Pets

**Original Pets:**
- Dog, Cat, Mouse

**LPC Dogs** (4 color variants):
- White, Tan, Golden, Black

**LPC Cats** (4 color variants):
- White, Orange, Gray, Black

**Special Pets:**
- **Emmy** - Interactive spider with unique animations

### Pet Behaviors

Pets react to what you're doing:

| Your Action | Pet Reaction |
|-------------|--------------|
| Recording | Listening animation (Emmy: gramophone) |
| Transcribing | Processing animation (Emmy: record spin) |
| Copy text | Celebration animation |
| Click pet | Petting animation (Emmy: rolling or toast) |

Emmy has special 50/50 random behaviors - sometimes she rolls over, sometimes she eats toast!

---

## Themes

VoiceThing includes multiple visual themes. Change them in Preferences (**P**).

### Available Themes

- Barbie Jelly
- Vaporwave
- Windows 95
- macOS 2005
- Rust Grunge (SBU Tunnels)
- Mahogany Wood
- Frutiger Aero
- Supervillain
- Dark Gradient
- Dark Minimal
- Y2K Winamp
- Cyberpunk Metal

Press number keys **1-9** in Preferences to quickly select themes.

---

## Settings Reference

All settings are saved automatically. Here's what each controls:

### Recording & Transcription

| Setting | Description | Default |
|---------|-------------|---------|
| WHISPER_MODEL | Transcription model (tiny/base/small/medium/large-v3) | base |
| SILENCE_SKIP_ENABLED | Pause recording during silence | OFF |
| SILENCE_THRESHOLD | Audio level for silence detection (-100 to -10 dB) | -65 dB |
| CUSTOM_WORDS | Context words to help Whisper recognize | (empty) |

### Paste Behavior

| Setting | Description | Default |
|---------|-------------|---------|
| AUTO_COPY | Copy transcription to clipboard | ON |
| AUTO_PASTE | Paste via ⌘V after copying | ON |
| AUTO_ENTER | Press Enter after pasting | OFF |
| ENTER_DELAY | Seconds to wait before Enter (0.0-2.0) | 0.1 |

### Wake Word

| Setting | Description | Default |
|---------|-------------|---------|
| WAKE_WORD_ENABLED | Enable always-listening detection | OFF |
| WAKEWORD_ENGINE | OpenWakeWord or macOS Native | openwakeword |

### LLM

| Setting | Description | Default |
|---------|-------------|---------|
| LLM_ENABLED | Enable post-processing | OFF |
| LLM_MODEL | Model to use (Ollama or OpenAI) | OLLAMA:qwen2.5:7b |
| LLM_PREFIX | System prompt for cleanup | (de-ramble prompt) |

### Tmux

| Setting | Description | Default |
|---------|-------------|---------|
| TMUX_MODE | Route to tmux instead of ⌘V | OFF |
| TMUX_TARGET | Default pane target | % (current) |
| TMUX_PANE_NAMES | Magic phrase assignments | {} |
| TMUX_PHRASES_AS_CONTEXT | Use phrases as Whisper context | ON |
| TMUX_ANNOUNCE_PANE | Speak pane name via TTS | OFF |

### Sound

| Setting | Description | Default |
|---------|-------------|---------|
| SOUND_ENABLED | Play notification chimes | ON |
| CHIME_VOLUME | Chime volume (0.0-1.0) | 0.5 |
| CHIME_PITCH | Pitch shift in semitones | 12 |
| CHIME_PROGRAM | MIDI instrument (0-127) | 127 |
| CHIME_THEME | Musical style | bright |

### Window

| Setting | Description | Default |
|---------|-------------|---------|
| AUTO_HIDE | Hide window after transcription | OFF |
| SIMPLE_MODE | Show only essential buttons | ON |
| ALWAYS_ON_TOP | Keep window above others | ON |
| RESTORE_WINDOW_GEOMETRY | Remember window positions | ON |
| THEME | Visual theme | macos_2005 |

### Storage

| Setting | Description |
|---------|-------------|
| RECORDINGS_DIR | Audio files and temporary transcripts |
| TRANSCRIPTIONS_DIR | Permanent text archive |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/RyannDaGreat/VoiceThing.git
cd VoiceThing

# Create a conda/mamba environment (recommended)
mamba create -n voicething python=3.10 -y
mamba activate voicething

# Install dependencies
pip install -r requirements.txt

# Run
python voice_thing.py
```

### First Run Setup

1. Grant Accessibility permissions when prompted
   - System Settings → Privacy & Security → Accessibility
   - Add your terminal app (Terminal.app, iTerm, etc.)
2. VoiceThing will download the base Whisper model automatically
3. Double-tap Option to test recording

### Optional: Local LLM

For LLM post-processing, install Ollama:

```bash
# Install Ollama
brew install ollama

# Start Ollama
ollama serve

# Pull a model (in another terminal)
ollama pull qwen2.5:7b
```

---

## Screenshots

| Idle State | Transcribing | Help Dialog |
|------------|--------------|-------------|
| ![Idle](screenshots/voicething_idle.png) | ![Transcribing](screenshots/voicething_transcribing_state.png) | ![Help](screenshots/help_dialog.png) |

---

## Author

By Clara Burgert
