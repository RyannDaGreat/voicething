"""Synthesizer module for VoiceThing.

This module provides a silent dummy synthesizer. FluidSynth has been removed.
The public API (`synth_sequence`, `play_native`, etc.) returns silence but
allows the rest of the application to run without crashing.
"""

import os
import sys
import numpy as np

try:
    from pedalboard import Pedalboard, Reverb, Chorus, Compressor, Gain
except Exception:
    # Very simple stand‑in that passes audio through unchanged.
    class _DummyEffect:
        def __init__(self, *args, **kwargs):
            pass

    class Pedalboard(list):
        def __init__(self, effects):
            super().__init__(effects)
        def __call__(self, audio, sample_rate):
            return audio

    Reverb = Chorus = Compressor = Gain = _DummyEffect

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------
SAMPLERATE = 44100

# ---------------------------------------------------------------------------
# Instrument preset mapping
# ---------------------------------------------------------------------------
INSTRUMENTS = {
    'bells': 0,           # FM Bells 1
    'carillon': 1,        # FM Carillion
    'christmas': 10,      # FM Christmas Bells
    'delicate': 119,      # Delicate Bells
    'marimba': 120,       # Delicate Marimba
    'xylophone': 68,      # Xylophone
    'vibraphone': 32,     # Cosmic Vibraphone
    'flute': 17,          # Smooth Flute
    'strings': 18,        # Smooth Strings 1
    'organ': 5,           # El Cheapo Organ
    'harp': 86,           # Sustained Harp
    'choir': 48,          # Faerie Chorale
    'fantasy': 29,        # Fantasy
    'calliope': 25,       # Breezy Calliope
}

# Effects chain for polish
EFFECTS = Pedalboard([
    Chorus(rate_hz=0.8, depth=0.1, mix=0.2),
    Reverb(room_size=0.5, damping=0.6, wet_level=0.3, dry_level=0.7),
    Compressor(threshold_db=-15, ratio=2.5),
    Gain(gain_db=-2),
])

# Global synth instances (lazy init)
_synth = None
_sfid = None
_native_synth = None
_native_sfid = None

# Note callback for piano visualization
_note_callback = None

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def set_note_callback(callback):
    """Set a callback to be invoked when notes are played.

    The callback receives ``(semitones, duration, shift)``.
    """
    global _note_callback
    _note_callback = callback

# ---------------------------------------------------------------------------
# Synthesiser creation
# ---------------------------------------------------------------------------
class _DummySynth:
    def __init__(self, *args, **kwargs):
        pass
    def sfload(self, path):
        return 0
    def program_select(self, *args, **kwargs):
        pass
    def noteon(self, *args, **kwargs):
        pass
    def noteoff(self, *args, **kwargs):
        pass
    def get_samples(self, n):
        return [0.0] * n
    def start(self, *args, **kwargs):
        pass
    def setting(self, *args, **kwargs):
        pass


def _get_synth():
    """Return a dummy synth instance for buffer rendering."""
    global _synth, _sfid
    if _synth is None:
        _synth = _DummySynth()
        _sfid = 0
    return _synth, _sfid


def _get_native_synth():
    """Return a dummy synth instance (no audio output)."""
    global _native_synth, _native_sfid
    if _native_synth is None:
        _native_synth = _DummySynth()
        _native_sfid = 0
    return _native_synth, _native_sfid

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_preset_name(program):
    """Get the preset name for *program*.

    This helper is rarely used in non‑debug builds.  For safety we
    catch any exception and fall back to a simple string.
    """
    synth, sfid = _get_synth()
    try:
        return synth.sfpreset_name(sfid, 0, program)
    except Exception:
        return f"Preset {program}"


def set_reverb(room_size=0.5, level=0.4):
    """Set reverb parameters for decay control."""
    synth, _ = _get_native_synth()
    synth.setting('synth.reverb.room-size', room_size)
    synth.setting('synth.reverb.level', level)


def set_instrument(name='bells'):
    """Set the instrument for chimes."""
    synth, sfid = _get_synth()
    prog = INSTRUMENTS.get(name, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)


def semitone_to_midi(semitone):
    return 69 + semitone


def synth_sequence(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells'):
    synth, sfid = _get_synth()
    prog = INSTRUMENTS.get(instrument, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)
    velocity = int(80 * volume)
    samples_per_chord = int(duration * SAMPLERATE)
    gap_samples = int(gap * SAMPLERATE)
    total_chords = len(chords)
    tail_time = 0.5
    total_samples = total_chords * (samples_per_chord + gap_samples) + int(tail_time * SAMPLERATE)
    all_audio = []
    for i, chord in enumerate(chords):
        for note in chord:
            midi_note = semitone_to_midi(note + shift)
            midi_note = max(0, min(127, midi_note))
            synth.noteon(0, midi_note, velocity)
        samples = synth.get_samples(samples_per_chord)
        all_audio.append(np.array(samples, dtype=np.float32))
        for note in chord:
            midi_note = semitone_to_midi(note + shift)
            midi_note = max(0, min(127, midi_note))
            synth.noteoff(0, midi_note)
        if gap_samples > 0 and i < len(chords) - 1:
            samples = synth.get_samples(gap_samples)
            all_audio.append(np.array(samples, dtype=np.float32))
    tail_samples = synth.get_samples(int(tail_time * SAMPLERATE))
    all_audio.append(np.array(tail_samples, dtype=np.float32))
    audio = np.concatenate(all_audio)
    if len(audio) % 2 == 0:
        audio = (audio[0::2] + audio[1::2]) / 2
    audio = audio / 32768.0
    audio = audio.astype(np.float32)
    audio_2d = audio.reshape(1, -1)
    processed = EFFECTS(audio_2d, SAMPLERATE)
    audio = processed.flatten()
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak * 0.7 * volume
    pad = np.zeros(int(0.05 * SAMPLERATE), dtype=np.float32)
    return np.concatenate([audio, pad])


def play_native(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells', program=None):
    import threading
    synth, sfid = _get_native_synth()
    if program is not None:
        prog = program
    else:
        prog = INSTRUMENTS.get(instrument, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)
    velocity = int(100 * volume)
    if _note_callback is not None:
        for chord in chords:
            _note_callback(chord, duration, shift)
    def play_chord_sequence():
        import time
        for i, chord in enumerate(chords):
            midi_notes = []
            for note in chord:
                midi_note = semitone_to_midi(note + shift)
                midi_note = max(0, min(127, midi_note))
                midi_notes.append(midi_note)
                synth.noteon(0, midi_note, velocity)
            time.sleep(duration)
            for midi_note in midi_notes:
                synth.noteoff(0, midi_note)
            if gap > 0 and i < len(chords) - 1:
                time.sleep(gap)
    t = threading.Thread(target=play_chord_sequence, daemon=True)
    t.start()

def note_on(semitone, shift=-12, volume=1.0, program=None):
    """Start a note (silent - returns dummy midi_note for tracking)."""
    return semitone_to_midi(semitone + shift)


def note_off(midi_note):
    """Stop a note (silent - no-op)."""
    pass