"""
siri_tts — Synthesize speech using macOS Siri voices via private SiriTTSService.framework.

Command, specific.

This module provides a simple interface to Apple's high-quality Siri neural TTS voices
(Aaron, Martha, Simone, Damon, Quinn, Nora, etc.) which are NOT accessible through the
standard `say` command or NSSpeechSynthesizer with explicit voice selection.

Requires:
    - macOS with Siri voices downloaded (System Settings > Accessibility > Spoken Content)
    - pyobjc (typically available in system Python; conda may need pyobjc-core)

Usage:
    from siri_tts import text_to_speech
    text_to_speech("Hello world", "Aaron")

Three known methods for Siri voice access on macOS (for future reference):

    Method 1 (XPC — IMPLEMENTED HERE):
        dlopen SiriTTSService.framework, use SiriTTSDaemonSession to send synthesis
        requests to the sirittsd daemon via XPC. Returns 48kHz 16-bit mono LPCM audio
        streamed via didGenerateAudio callbacks on SiriTTSSynthesisContext.
        Pros: Direct voice selection, no system state mutation, 48kHz quality,
              full control (rate/pitch/volume/whisper). No extra dependencies.
        Cons: Private API — could break on macOS updates.

    Method 2 (defaults write + say):
        Write desired voice ID to com.apple.Accessibility
        SpokenContentDefaultVoiceSelectionsByLanguage, then call `say` with no -v flag.
        The `say` command picks up the new default. Save/restore original pref around it.
        Pros: No private frameworks, simple subprocess call.
        Cons: Mutates system Accessibility preference — crash leaves bad state.
              Race condition if user changes voice concurrently.

    Method 3 (NSSpeechSynthesizer .premium):
        NSSpeechSynthesizer with voice IDs like "com.apple.voice.Aman.premium".
        Only works for 4 neuralAX voices (Aman, Aru, Ona, Tara) — NOT the main
        en-US natural voices (Aaron, Martha, Simone, Damon, Quinn).
        Pros: Clean API, no system mutation.
        Cons: Only 4 non-US voices work. Useless for en-US Siri voices.
"""

import ctypes
import threading
import time
import wave
import os
import tempfile
import subprocess


_SIRI_SAMPLE_RATE = 48000
_SIRI_CHANNELS = 1
_SIRI_SAMPLE_WIDTH = 2  # 16-bit


# ---------------------------------------------------------------------------
# SiriTTSService framework interface
# ---------------------------------------------------------------------------

_framework_loaded = False


def _ensure_framework():
    """
    Command, specific. Load SiriTTSService.framework and register ObjC block metadata.

    Idempotent — safe to call multiple times.

    Raises:
        OSError: if framework cannot be loaded
    """
    global _framework_loaded
    if _framework_loaded:
        return

    fw_path = (
        "/System/Library/PrivateFrameworks/"
        "SiriTTSService.framework/SiriTTSService"
    )
    ctypes.cdll.LoadLibrary(fw_path)

    import objc

    # Register block type metadata for the callback parameters.
    # Without this, pyobjc cannot create the ObjC blocks correctly.
    _block_meta = {
        "callable": {
            "retval": {"type": b"v"},
            "arguments": [{"type": b"@?"}, {"type": b"@"}],
        }
    }
    objc.registerMetaDataForSelector(
        b"SiriTTSDaemonSession",
        b"synthesizeWithRequest:didFinish:",
        {"arguments": {3: _block_meta}},
    )
    objc.registerMetaDataForSelector(
        b"SiriTTSSynthesisContext",
        b"setDidGenerateAudio:",
        {"arguments": {2: _block_meta}},
    )
    objc.registerMetaDataForSelector(
        b"SiriTTSDaemonSession",
        b"downloadedVoicesMatching:reply:",
        {"arguments": {3: _block_meta}},
    )

    _framework_loaded = True


def _pump_runloop(done_event, timeout_seconds):
    """
    Command, specific. Spin the NSRunLoop until done_event is set or timeout.

    Args:
        done_event (threading.Event): signals completion
        timeout_seconds (float): max wait time

    Raises:
        TimeoutError: if done_event not set within timeout
    """
    import Foundation

    run_loop = Foundation.NSRunLoop.currentRunLoop()
    deadline = time.time() + timeout_seconds
    while not done_event.is_set() and time.time() < deadline:
        run_loop.runUntilDate_(
            Foundation.NSDate.dateWithTimeIntervalSinceNow_(0.05)
        )
    if not done_event.is_set():
        raise TimeoutError(
            "Siri TTS timed out after %d seconds" % timeout_seconds
        )


def list_voices():
    """
    Query, specific. List all downloaded Siri voices on this machine.

    Returns:
        list of dict: each with keys 'name', 'language', 'type', 'gender'
            type is one of: 'natural' (6), 'neuralAX' (5), 'neural' (4)
            gender is one of: 'male' (1), 'female' (2), 'neutral' (3)

    Examples:
        >>> # Returns list of dicts like:
        >>> # [{'name': 'Aaron', 'language': 'en-US', 'type': 'natural', 'gender': 'male'}, ...]
    """
    _ensure_framework()

    import objc

    DaemonSession = objc.lookUpClass("SiriTTSDaemonSession")
    session = DaemonSession.alloc().init()

    voices = []
    done = threading.Event()

    _type_map = {4: "neural", 5: "neuralAX", 6: "natural"}
    _gender_map = {1: "male", 2: "female", 3: "neutral"}

    def on_reply(voice_list):
        if voice_list:
            for v in voice_list:
                voices.append({
                    "name": str(v.name()),
                    "language": str(v.language()),
                    "type": _type_map.get(v.type(), "unknown_%d" % v.type()),
                    "gender": _gender_map.get(v.gender(), "unknown_%d" % v.gender()),
                })
        done.set()

    session.downloadedVoicesMatching_reply_(None, on_reply)
    _pump_runloop(done, 5)
    return voices


def synthesize(text, voice_name, language="en-US", rate=1.0, pitch=1.0, volume=0.8):
    """
    Command, specific. Synthesize text to 48kHz 16-bit mono PCM bytes using a Siri voice.

    The sirittsd daemon streams LPCM audio via callbacks. This function collects
    all chunks and returns the concatenated raw PCM.

    Args:
        text (str): Text to speak
        voice_name (str): Capitalized voice name, e.g. "Aaron", "Martha", "Simone"
        language (str): BCP-47 language tag, e.g. "en-US", "en-GB"
        rate (float): Speech rate multiplier (default 1.0)
        pitch (float): Pitch multiplier (default 1.0)
        volume (float): Volume 0.0-1.0 (default 0.8)

    Returns:
        bytes: raw 16-bit signed LE mono PCM at 48kHz

    Raises:
        TimeoutError: if synthesis takes longer than 30 seconds
        RuntimeError: if sirittsd returns an error
    """
    _ensure_framework()

    import objc

    DaemonSession = objc.lookUpClass("SiriTTSDaemonSession")
    SynthVoice = objc.lookUpClass("SiriTTSSynthesisVoice")
    SynthRequest = objc.lookUpClass("SiriTTSSynthesisRequest")

    voice = SynthVoice.alloc().initWithLanguage_name_(language, voice_name)
    request = SynthRequest.alloc().initWithText_voice_(text, voice)
    ctx = request.synthesisContext()

    ctx.setRate_(rate)
    ctx.setPitch_(pitch)
    ctx.setVolume_(volume)

    pcm_parts = []
    done = threading.Event()
    error_ref = [None]

    def on_audio(audio_data):
        raw = audio_data.audioData()
        if raw and len(raw) > 0:
            pcm_parts.append(bytes(raw))

    ctx.setDidGenerateAudio_(on_audio)

    def on_done(error):
        if error is not None:
            error_ref[0] = str(error)
        done.set()

    session = DaemonSession.alloc().init()
    session.synthesizeWithRequest_didFinish_(request, on_done)

    _pump_runloop(done, 30)

    if error_ref[0] is not None:
        raise RuntimeError("Siri TTS error: %s" % error_ref[0])

    return b"".join(pcm_parts)


def text_to_speech(text, voice="Aaron", language="en-US", output_path=None):
    """
    Command, specific. Speak text using a Siri voice, or save to WAV file.

    If output_path is None, plays audio through the default output device via afplay.
    If output_path is given, saves a 48kHz 16-bit mono WAV file.

    Args:
        text (str): Text to speak
        voice (str): Capitalized voice name — "Aaron", "Martha", "Simone",
                     "Damon", "Quinn", "Nora", "Arthur", etc.
        language (str): BCP-47 language tag (default "en-US")
        output_path (str or None): Path to save WAV file, or None to play immediately

    Returns:
        str or None: output_path if saving, None if playing

    Raises:
        TimeoutError: if synthesis exceeds 30 seconds
        RuntimeError: if sirittsd returns an error or voice not downloaded
    """
    pcm = synthesize(text, voice, language=language)

    if not pcm:
        raise RuntimeError(
            "Siri TTS returned empty audio for voice '%s'. "
            "Is the voice downloaded in System Settings > Accessibility > Spoken Content?"
            % voice
        )

    if output_path is not None:
        wav_path = output_path
    else:
        wav_path = tempfile.mktemp(suffix=".wav", prefix="siri_tts_")

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(_SIRI_CHANNELS)
        wf.setsampwidth(_SIRI_SAMPLE_WIDTH)
        wf.setframerate(_SIRI_SAMPLE_RATE)
        wf.writeframes(pcm)

    if output_path is not None:
        return output_path

    # Play and clean up
    try:
        subprocess.run(["afplay", wav_path], check=True)
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)

    return None


# ---------------------------------------------------------------------------
# CLI — fire-based
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import fire

    def speak(text, voice="Aaron", language="en-US", output=None):
        """Speak text using a Siri voice, or save to WAV."""
        result = text_to_speech(text, voice=voice, language=language, output_path=output)
        if result:
            print("Saved: %s" % result)

    def voices():
        """List all downloaded Siri voices."""
        for v in list_voices():
            print("%-12s %-6s %-10s %s" % (v["name"], v["language"], v["type"], v["gender"]))

    fire.Fire({"speak": speak, "voices": voices})
