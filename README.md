# VoiceThing

A fast, keyboard-driven voice transcription app for macOS, powered by Whisper with Metal GPU acceleration.

![VoiceThing Main Window](screenshots/transcriptions_tab_with_content.png)

## Features

- **Double-tap ⌥ (Option)** to start/stop recording from anywhere - works in fullscreen apps and terminals
- **Instant transcription** using Whisper with Apple Silicon Metal GPU acceleration
- **Auto-paste** - transcription is automatically copied and pasted via ⌘V
- **100% keyboard-driven** - no mouse needed
- **Wake word detection** - say "Hey Jarvis" (or other wake words) to start recording hands-free
- **Tmux mode** - paste transcriptions directly into your active tmux pane
- **LLM post-processing** (Anti-Ramble mode) - clean up filler words and self-corrections with a local Ollama model
- **De-ramble after the fact** - click the pen button on any transcription to apply LLM processing
- **Menu bar access** - always available from macOS menu bar
- **Drag & drop** audio files to transcribe

## Screenshots

| Idle State | Transcribing | Help Dialog |
|------------|--------------|-------------|
| ![Idle](screenshots/voicething_idle.png) | ![Transcribing](screenshots/voicething_transcribing_state.png) | ![Help](screenshots/help_dialog.png) |

## Requirements

- **macOS** with Apple Silicon (M1/M2/M3/M4)
- **Python 3.10**
- **Accessibility permissions** for global keyboard shortcuts

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

On first run, you'll need to grant Accessibility permissions to your terminal app (System Settings → Privacy & Security → Accessibility).

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start/stop recording |
| `X` | Cancel recording |
| `Esc` | Minimize window |
| `E` | Toggle small mode |
| `C` | Copy last transcription |
| `L` | Load audio file |
| `F` | Open recordings folder |
| `S` | Toggle sound effects |
| `V` | Toggle auto-minimize |
| `R` | Toggle LLM post-processing |
| `J` | Toggle wake word detection |
| `K` | Change wake word model |
| `U` | Toggle tmux paste mode |
| `N` | Toggle auto-enter |
| `M` | Change Whisper model |
| `?` | Show help |
| `O` | Output tab |
| `T` | Transcriptions tab |

**Global shortcuts:**
- `⌥⌥` (double-tap Option) - Start/stop recording from anywhere
- `⌘ + ⌥⌥` - Toggle window focus

## Whisper Models

| Key | Model | Description |
|-----|-------|-------------|
| `T` | tiny | Fastest, least accurate (~1GB VRAM) |
| `B` | base | Fast, basic accuracy (~1GB VRAM) |
| `S` | small | Balanced speed/accuracy (~2GB VRAM) |
| `M` | medium | Good accuracy, slower (~5GB VRAM) |
| `L` | large-v3 | Best accuracy, slowest (~10GB VRAM) |

## LLM Post-Processing (Anti-Ramble Mode)

Press `R` to enable LLM post-processing. This uses a local Ollama model to:
- Remove filler words (um, uh, "you know")
- Collapse stutters ("set the- set the-" → "set the")
- Apply self-corrections ("actually change X to Y")
- Clean up rambling while preserving your exact words

Say "VoiceThing, ..." in your recording to give formatting instructions directly to the LLM.

## Wake Word Detection

Press `J` to enable wake word detection. This lets you start recording hands-free by saying a wake word like "Hey Jarvis".

- **Always listening** (when enabled) - the app listens for the wake word in the background
- **Pre-buffer capture** - captures 2 seconds of audio *before* you say the wake word, so you don't lose any words
- **Configurable sensitivity** - adjust in Preferences to reduce false triggers
- **Multiple wake words** - press `K` or use Preferences to choose from options like "Hey Jarvis", "Alexa", "OK Google", "Computer", etc.
- **Battery efficient** - the audio stream is completely stopped when wake word is disabled

When you say the wake word, recording starts automatically. Say the wake word again (or press Space) to stop recording and transcribe.

## Tmux Mode

Press `U` to enable tmux mode. Instead of pasting via ⌘V, transcriptions are sent directly to your active tmux pane using `tmux send-keys`.

This is useful for:
- **Terminal workflows** - dictate commands or text directly into terminal sessions
- **Remote sessions** - works even when the terminal isn't the frontmost app
- **Auto-enter** - combine with `N` (auto-enter) to automatically execute commands after transcription

Requires tmux to be installed and running.

## Author

By Clara Burgert
