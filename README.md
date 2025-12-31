# VoiceThing

A fast, keyboard-driven voice transcription app for macOS, powered by Whisper with Metal GPU acceleration.

![VoiceThing Main Window](screenshots/transcriptions_tab_with_content.png)

## Features

- **Double-tap ⌥ (Option)** to start/stop recording from anywhere - works in fullscreen apps and terminals
- **Instant transcription** using Whisper with Apple Silicon Metal GPU acceleration
- **Auto-paste** - transcription is automatically copied and pasted via ⌘V
- **100% keyboard-driven** - no mouse needed
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

## Author

By Clara Burgert
