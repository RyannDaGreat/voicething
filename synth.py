"""Synthesizer module using rp.play_chords."""

import rp

SAMPLERATE = 44100
INSTRUMENTS = {}  # Kept for API compatibility

_note_callback = None

def set_note_callback(callback):
    global _note_callback
    _note_callback = callback

def get_preset_name(program):
    return f"Preset {program}"

def set_reverb(room_size=0.5, level=0.4):
    pass

def set_instrument(name='bells'):
    pass

def semitone_to_midi(semitone):
    return 69 + semitone

def synth_sequence(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells'):
    import numpy as np
    return np.zeros(int(0.1 * SAMPLERATE), dtype=np.float32)

def play_native(chords, duration=0.15, gap=0.0, shift=-12, volume=1.0, instrument='bells', program=None):
    if _note_callback is not None:
        for chord in chords:
            _note_callback(chord, duration, shift)
    shifted = [[n + shift for n in chord] for chord in chords]
    rp.play_chords(*shifted, t=duration, gap=gap, block=False)

def note_on(semitone, shift=-12, volume=1.0, program=None):
    rp.play_chord([semitone + shift], t=0.3, block=False)
    return semitone_to_midi(semitone + shift)

def note_off(midi_note):
    pass
