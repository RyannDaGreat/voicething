"""Synthesizer module using FluidSynth for beautiful instrument sounds."""

import os
import sys
import numpy as np
import fluidsynth
from pedalboard import Pedalboard, Reverb, Chorus, Compressor, Gain

SAMPLERATE = 44100
SOUNDFONT_PATH = "/opt/homebrew/Cellar/fluid-synth/2.4.7/share/fluid-synth/sf2/VintageDreamsWaves-v2.sf2"

# Instrument presets (bank 0)
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
_synth = None  # For rendering to buffer
_sfid = None
_native_synth = None  # For native audio playback (non-blocking)
_native_sfid = None

# Global note callback - called when notes are played (for piano visualization)
# Signature: callback(semitones: list[int], duration: float, shift: int)
_note_callback = None


def set_note_callback(callback):
    """Set a callback to be invoked when notes are played.

    Args:
        callback: Function(semitones, duration, shift) or None to clear.
                  semitones: list of semitone offsets from A4
                  duration: note duration in seconds
                  shift: pitch shift applied to notes
    """
    global _note_callback
    _note_callback = callback


def _suppress_stderr(func):
    """Suppress FluidSynth C-level warnings during function execution."""
    def wrapper(*args, **kwargs):
        stderr_fd = sys.stderr.fileno()
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(stderr_fd)
        os.dup2(devnull, stderr_fd)
        try:
            return func(*args, **kwargs)
        finally:
            os.dup2(old_stderr, stderr_fd)
            os.close(old_stderr)
            os.close(devnull)
    return wrapper


def _get_synth():
    """Get or create FluidSynth instance for buffer rendering."""
    global _synth, _sfid
    if _synth is None:
        @_suppress_stderr
        def init():
            global _synth, _sfid
            _synth = fluidsynth.Synth(samplerate=float(SAMPLERATE))
            _sfid = _synth.sfload(SOUNDFONT_PATH)
            _synth.program_select(0, _sfid, 0, INSTRUMENTS['bells'])
        init()
    return _synth, _sfid


def _get_native_synth():
    """Get or create FluidSynth with native audio driver (non-blocking)."""
    global _native_synth, _native_sfid
    if _native_synth is None:
        @_suppress_stderr
        def init():
            global _native_synth, _native_sfid
            _native_synth = fluidsynth.Synth(gain=0.5)
            _native_synth.start(driver='coreaudio')
            _native_sfid = _native_synth.sfload(SOUNDFONT_PATH)
            _native_synth.program_select(0, _native_sfid, 0, INSTRUMENTS['bells'])
            # Enable built-in reverb/chorus (replaces pedalboard effects)
            _native_synth.setting('synth.reverb.active', 1)
            _native_synth.setting('synth.chorus.active', 1)
            _native_synth.setting('synth.reverb.room-size', 0.5)
            _native_synth.setting('synth.reverb.level', 0.4)
        init()
    return _native_synth, _native_sfid


def get_preset_name(program):
    """Get the preset name from the soundfont for a given program number."""
    synth, sfid = _get_synth()
    try:
        return synth.sfpreset_name(sfid, 0, program)
    except:
        return f"Preset {program}"


def set_reverb(room_size=0.5, level=0.4, damping=0.5):
    """Set reverb parameters for decay control.

    Args:
        room_size: 0.0-1.0, larger = longer decay
        level: 0.0-1.0, reverb wet level
        damping: 0.0-1.0, high frequency damping (higher = warmer)
    """
    synth, _ = _get_native_synth()
    synth.setting('synth.reverb.room-size', room_size)
    synth.setting('synth.reverb.level', level)
    synth.setting('synth.reverb.damp', damping)


def set_chorus(level=0.5, speed=0.3, depth=8.0):
    """Set chorus parameters for width/shimmer.

    Args:
        level: 0.0-1.0, chorus wet level
        speed: 0.1-5.0, modulation rate in Hz
        depth: 0.0-21.0, modulation depth in ms
    """
    synth, _ = _get_native_synth()
    synth.setting('synth.chorus.level', level)
    synth.setting('synth.chorus.speed', speed)
    synth.setting('synth.chorus.depth', depth)


def set_instrument(name='bells'):
    """Set the instrument for chimes."""
    synth, sfid = _get_synth()
    prog = INSTRUMENTS.get(name, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)


def semitone_to_midi(semitone):
    """Convert semitone offset (0 = A4) to MIDI note number (A4 = 69)."""
    return 69 + semitone


def synth_sequence(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells'):
    """Generate beautiful audio for a sequence of chords using FluidSynth.

    Args:
        chords: List of chords, each chord is a list of semitone offsets
        duration: Duration per chord in seconds
        gap: Gap between chords in seconds
        shift: Semitone shift applied to all notes (default -12 = 1 octave down)
        volume: Volume multiplier (0.0 to 1.0)
        instrument: Instrument name (bells, carillon, christmas, delicate, etc.)

    Returns:
        numpy array of audio samples (float32)
    """
    synth, sfid = _get_synth()

    # Set instrument
    prog = INSTRUMENTS.get(instrument, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)

    velocity = int(80 * volume)  # MIDI velocity 0-127
    samples_per_chord = int(duration * SAMPLERATE)
    gap_samples = int(gap * SAMPLERATE)

    # Calculate total length needed
    total_chords = len(chords)
    # Add extra time for note release/reverb tail
    tail_time = 0.5
    total_samples = total_chords * (samples_per_chord + gap_samples) + int(tail_time * SAMPLERATE)

    # Render all notes
    all_audio = []

    for i, chord in enumerate(chords):
        # Note on for all notes in chord
        for note in chord:
            midi_note = semitone_to_midi(note + shift)
            midi_note = max(0, min(127, midi_note))  # Clamp to valid range
            synth.noteon(0, midi_note, velocity)

        # Render this chord's duration
        samples = synth.get_samples(samples_per_chord)
        all_audio.append(np.array(samples, dtype=np.float32))

        # Note off
        for note in chord:
            midi_note = semitone_to_midi(note + shift)
            midi_note = max(0, min(127, midi_note))
            synth.noteoff(0, midi_note)

        # Render gap
        if gap_samples > 0 and i < len(chords) - 1:
            samples = synth.get_samples(gap_samples)
            all_audio.append(np.array(samples, dtype=np.float32))

    # Render tail (let notes decay naturally)
    tail_samples = synth.get_samples(int(tail_time * SAMPLERATE))
    all_audio.append(np.array(tail_samples, dtype=np.float32))

    # Combine all audio
    audio = np.concatenate(all_audio)

    # FluidSynth returns interleaved stereo, convert to mono
    if len(audio) % 2 == 0:
        audio = (audio[0::2] + audio[1::2]) / 2

    # Normalize
    audio = audio / 32768.0  # FluidSynth returns int16 range

    # Apply effects
    audio = audio.astype(np.float32)
    audio_2d = audio.reshape(1, -1)
    processed = EFFECTS(audio_2d, SAMPLERATE)
    audio = processed.flatten()

    # Final normalize with headroom
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak * 0.7 * volume

    # Pad end to prevent crackle
    pad = np.zeros(int(0.05 * SAMPLERATE), dtype=np.float32)
    return np.concatenate([audio, pad])


def play_native(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells', program=None):
    """Play chords instantly using native FluidSynth audio (non-blocking).

    Sounds layer naturally - multiple calls overlap. No GIL issues.
    Uses FluidSynth's built-in reverb/chorus instead of pedalboard effects.

    Args:
        chords: List of chords, each chord is a list of semitone offsets
        duration: Duration per note in seconds (for scheduling note-offs)
        gap: Gap between chords in seconds
        shift: Semitone shift applied to all notes
        volume: Volume (0.0 to 1.0)
        instrument: Instrument name (ignored if program is set)
        program: Direct program number (0-135), overrides instrument name
    """
    import threading
    synth, sfid = _get_native_synth()

    # Set instrument - program number takes precedence
    if program is not None:
        prog = program
    else:
        prog = INSTRUMENTS.get(instrument, INSTRUMENTS['bells'])
    synth.program_select(0, sfid, 0, prog)

    velocity = int(100 * volume)  # MIDI velocity 0-127

    # Fire note callback for piano visualization (if registered)
    if _note_callback is not None:
        for chord in chords:
            _note_callback(chord, duration, shift)

    def play_chord_sequence():
        import time
        for i, chord in enumerate(chords):
            # Note on
            midi_notes = []
            for note in chord:
                midi_note = semitone_to_midi(note + shift)
                midi_note = max(0, min(127, midi_note))
                midi_notes.append(midi_note)
                synth.noteon(0, midi_note, velocity)

            time.sleep(duration)

            # Note off
            for midi_note in midi_notes:
                synth.noteoff(0, midi_note)

            if gap > 0 and i < len(chords) - 1:
                time.sleep(gap)

    # Run in background thread so it doesn't block
    t = threading.Thread(target=play_chord_sequence, daemon=True)
    t.start()


def note_on(semitone, shift=-12, volume=1.0, program=None):
    """Start a sustained note (call note_off to stop it).

    Args:
        semitone: Semitone offset from A4 (0 = A4)
        shift: Pitch shift in semitones
        volume: Volume (0.0 to 1.0)
        program: Program number (0-127)

    Returns:
        MIDI note number (for use with note_off)
    """
    synth, sfid = _get_native_synth()

    if program is not None:
        synth.program_select(0, sfid, 0, program)

    velocity = int(100 * volume)
    midi_note = semitone_to_midi(semitone + shift)
    midi_note = max(0, min(127, midi_note))
    synth.noteon(0, midi_note, velocity)
    return midi_note


def note_off(midi_note):
    """Stop a sustained note.

    Args:
        midi_note: MIDI note number returned by note_on
    """
    synth, _ = _get_native_synth()
    synth.noteoff(0, midi_note)
