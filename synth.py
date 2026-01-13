"""Simple synthesizer module for chimes and notifications."""

import numpy as np

SAMPLERATE = 44100


def make_envelope(n_samples, attack=0.02, decay=0.05, sustain=0.7, release=0.08):
    """Build ADSR envelope array."""
    a_samp = int(attack * SAMPLERATE)
    d_samp = int(decay * SAMPLERATE)
    r_samp = int(release * SAMPLERATE)
    s_samp = max(0, n_samples - a_samp - d_samp - r_samp)

    parts = []
    if a_samp > 0:
        parts.append(np.linspace(0, 1, a_samp))  # Attack: 0 -> 1
    if d_samp > 0:
        parts.append(np.linspace(1, sustain, d_samp))  # Decay: 1 -> sustain
    if s_samp > 0:
        parts.append(np.full(s_samp, sustain))  # Sustain
    if r_samp > 0:
        parts.append(np.linspace(sustain, 0, r_samp))  # Release: sustain -> 0

    env = np.concatenate(parts) if parts else np.ones(n_samples)
    if len(env) < n_samples:
        env = np.concatenate([env, np.zeros(n_samples - len(env))])
    return env[:n_samples]


def semitone_to_hz(semitone, a4=440.0):
    """Convert semitone offset (0 = A4) to frequency in Hz."""
    return a4 * (2 ** (semitone / 12))


def triangle_wave(freq, duration):
    """Generate triangle wave samples."""
    n = int(duration * SAMPLERATE)
    t = np.linspace(0, duration, n, endpoint=False)
    return (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t))


def synth_tone(freq, duration, attack=0.02, decay=0.05, sustain=0.7, release=0.08):
    """Generate a single tone with triangle wave and ADSR envelope."""
    n = int(duration * SAMPLERATE)
    wave = triangle_wave(freq, duration)
    envelope = make_envelope(n, attack, decay, sustain, release)
    return wave * envelope


def synth_chord(notes, duration, shift=0, **envelope_args):
    """Generate a chord from semitone offsets."""
    samples = None
    for note in notes:
        freq = semitone_to_hz(note + shift)
        tone = synth_tone(freq, duration, **envelope_args)
        if samples is None:
            samples = tone.copy()
        else:
            samples = samples + tone
    if samples is not None:
        peak = np.abs(samples).max()
        if peak > 0:
            samples = samples / peak
    return samples


def synth_sequence(chords, duration=0.12, gap=0.0, shift=-12, volume=1.0, **envelope_args):
    """Generate audio for a sequence of chords.

    Args:
        chords: List of chords, each chord is a list of semitone offsets
        duration: Duration per chord in seconds
        gap: Gap between chords in seconds
        shift: Semitone shift applied to all notes (default -12 = 1 octave down)
        volume: Volume multiplier (0.0 to 1.0)
        **envelope_args: ADSR parameters (attack, decay, sustain, release)

    Returns:
        numpy array of audio samples
    """
    parts = []
    gap_samples = np.zeros(int(gap * SAMPLERATE))

    for i, chord in enumerate(chords):
        chord_samples = synth_chord(chord, duration, shift=shift, **envelope_args)
        if chord_samples is not None:
            chord_samples = chord_samples * 0.3 * volume
            parts.append(chord_samples)
        if i < len(chords) - 1 and gap > 0:
            parts.append(gap_samples)

    if not parts:
        return np.array([])
    return np.concatenate(parts) if len(parts) > 1 else parts[0]
