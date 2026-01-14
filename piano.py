"""Piano widget with QWERTY keyboard input and mouse interaction."""

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtWidgets import QWidget


class PianoWidget(QWidget):
    """Interactive piano keyboard with mouse and keyboard input.

    Features:
    - Click/drag to play notes
    - QWERTY keyboard input when focused (with sustain)
    - Visual feedback for external chime playback
    """

    # Signal for thread-safe key triggering (from synth callback thread)
    _trigger_key_signal = pyqtSignal(int, float)  # semitone, duration

    # Which semitones in an octave are black keys (0=C, 1=C#, 2=D, etc.)
    BLACK_KEYS = {1, 3, 6, 8, 10}  # C#, D#, F#, G#, A#

    # Keyboard mapping: key -> semitone offset
    # Mac keyboard layout - black keys sit between white keys:
    #
    #  1 2 3 4 5 6 7 8 9 0 - =    <- black keys (number row)
    #   Q W E R T Y U I O P [ ] \  <- white keys (top row)
    #    A S D F G H J K L ; '     <- black keys (home row)
    #     Z X C V B N M , . /      <- white keys (bottom row)
    #
    # Piano notes (semitones from A4=0):
    # White: A  B  C  D  E  F  G  A  B  C  D  E  F  G  A  B  C  D  E  F
    #        0  2  3  5  7  8  10 12 14 15 17 19 20 ...
    # Black: A# C# D# F# G# A# C# D# F# G# ...
    #        1  4  6  9  11 13 16 18 21 23 ...
    # Keyboard mapping following piano layout on Mac QWERTY keyboard:
    #
    #   2 3   5 6 7   9 0   =       <- black keys (number row)
    #  Q W E R T Y U I O P [ ] \    <- white keys (QWERTY row)
    #   S D   G H J   L ;           <- black keys (home row)
    #  Z X C V B N M , . /          <- white keys (bottom row)
    #
    # Pattern: Q2W3E R5T6Y7U I9O0P [=] (like piano C C# D D# E F F# G G# A A# B C...)
    # Semitones: 0=A4, so C5=3, D5=5, E5=7, F5=8, G5=10, A5=12, B5=14, C6=15...
    KEYBOARD_MAP = {
        # Upper row white keys: C5 D5 E5 F5 G5 A5 B5 C6 D6 E6 F6 G6 A6
        Qt.Key.Key_Tab: -9,           # C4 (below Q)
        Qt.Key.Key_Q: 3,              # C5
        Qt.Key.Key_W: 5,              # D5
        Qt.Key.Key_E: 7,              # E5
        Qt.Key.Key_R: 8,              # F5
        Qt.Key.Key_T: 10,             # G5
        Qt.Key.Key_Y: 12,             # A5
        Qt.Key.Key_U: 14,             # B5
        Qt.Key.Key_I: 15,             # C6
        Qt.Key.Key_O: 17,             # D6
        Qt.Key.Key_P: 19,             # E6
        Qt.Key.Key_BracketLeft: 20,   # F6
        Qt.Key.Key_BracketRight: 22,  # G6
        Qt.Key.Key_Backslash: 24,     # A6
        # Upper row black keys (interleaved): C#5 D#5 F#5 G#5 A#5 C#6 D#6 F#6 G#6 A#6
        Qt.Key.Key_2: 4,              # C#5 (between Q and W)
        Qt.Key.Key_3: 6,              # D#5 (between W and E)
        # no 4 - no black key between E and R (E-F)
        Qt.Key.Key_5: 9,              # F#5 (between R and T)
        Qt.Key.Key_6: 11,             # G#5 (between T and Y)
        Qt.Key.Key_7: 13,             # A#5 (between Y and U)
        # no 8 - no black key between U and I (B-C)
        Qt.Key.Key_9: 16,             # C#6 (between I and O)
        Qt.Key.Key_0: 18,             # D#6 (between O and P)
        # no - - no black key between P and [ (E-F)
        Qt.Key.Key_Equal: 21,         # F#6 (between [ and ])
        # Lower row white keys (one octave below): C4 D4 E4 F4 G4 A4 B4 C5 D5 E5
        Qt.Key.Key_Z: -9,             # C4
        Qt.Key.Key_X: -7,             # D4
        Qt.Key.Key_C: -5,             # E4
        Qt.Key.Key_V: -4,             # F4
        Qt.Key.Key_B: -2,             # G4
        Qt.Key.Key_N: 0,              # A4
        Qt.Key.Key_M: 2,              # B4
        Qt.Key.Key_Comma: 3,          # C5
        Qt.Key.Key_Period: 5,         # D5
        Qt.Key.Key_Slash: 7,          # E5
        # Lower row black keys (home row, interleaved): C#4 D#4 F#4 G#4 A#4 C#5 D#5
        Qt.Key.Key_S: -8,             # C#4 (between Z and X)
        Qt.Key.Key_D: -6,             # D#4 (between X and C)
        # no F - no black key between C and V (E-F)
        Qt.Key.Key_G: -3,             # F#4 (between V and B)
        Qt.Key.Key_H: -1,             # G#4 (between B and N)
        Qt.Key.Key_J: 1,              # A#4 (between N and M)
        # no K - no black key between M and , (B-C)
        Qt.Key.Key_L: 4,              # C#5 (between , and .)
        Qt.Key.Key_Semicolon: 6,      # D#5 (between . and /)
    }

    # Global instance for note callbacks (set when preferences dialog opens)
    _instance = None

    def __init__(self, height=40, hint_label=None, pitch_getter=None,
                 settings_getter=None):
        """Create a piano widget.

        Args:
            height: Widget height in pixels
            hint_label: Optional QLabel to show keyboard hint when focused
            pitch_getter: Callable returning current pitch shift (semitones)
            settings_getter: Callable returning (pitch, volume, program) tuple
        """
        super().__init__()
        self.height_px = height
        self.hint_label = hint_label
        self.pitch_getter = pitch_getter or (lambda: 0)
        self.settings_getter = settings_getter or (lambda: (0, 0.5, 0))
        self.setFixedHeight(height)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self._hover_key = None
        self._pressed_keys = set()  # Visually pressed keys
        self._sustained_notes = {}  # semitone -> midi_note (for sustain)
        self._dragging = False
        self._last_drag_key = None
        self._trigger_key_signal.connect(self._do_trigger_key)
        PianoWidget._instance = self

    def _get_key_layout(self):
        """Calculate key positions that smoothly shift with pitch.

        The piano scrolls continuously based on pitch, centering the current
        pitch note in the middle of the widget.
        """
        pitch = self.pitch_getter()
        width = self.width()

        # Generate 5 octaves of keys (enough to fill view with margin)
        num_semitones = 60
        start_semitone = -30  # Start 2.5 octaves below A4

        # Fixed white key width based on fitting ~21 white keys in view
        white_width = width / 21
        black_width = white_width * 0.6
        black_height = self.height_px * 0.6

        # First pass: calculate positions relative to start_semitone
        white_keys = []
        black_keys = []
        key_centers = {}  # semitone -> x center position

        white_idx = 0
        for i in range(num_semitones):
            semitone = start_semitone + i
            note_in_octave = semitone % 12

            if note_in_octave in self.BLACK_KEYS:
                x = white_idx * white_width - black_width / 2
                black_keys.append([x, 0, black_width, black_height, semitone])
                key_centers[semitone] = x + black_width / 2
            else:
                x = white_idx * white_width
                white_keys.append([x, 0, white_width, self.height_px, semitone])
                key_centers[semitone] = x + white_width / 2
                white_idx += 1

        # Calculate offset to center the pitch note
        # Find where pitch=0 (A4) is, then offset based on pitch
        a4_center = key_centers.get(0, width / 2)
        # Each semitone shifts by approximately white_width * (7/12) on average
        semitone_shift = white_width * (7 / 12)
        target_center = a4_center + pitch * semitone_shift
        offset = width / 2 - target_center

        # Apply offset to all keys
        for key in white_keys:
            key[0] += offset
        for key in black_keys:
            key[0] += offset

        # Convert to tuples
        white_keys = [(k[0], k[1], k[2], k[3], k[4]) for k in white_keys]
        black_keys = [(k[0], k[1], k[2], k[3], k[4]) for k in black_keys]

        return white_keys, black_keys

    def _key_at_pos(self, pos):
        """Return semitone of key at position, or None."""
        white_keys, black_keys = self._get_key_layout()
        x, y = pos.x(), pos.y()

        # Check black keys first (they're on top)
        for kx, ky, kw, kh, semitone in black_keys:
            if kx <= x < kx + kw and ky <= y < ky + kh:
                return semitone
        # Then white keys
        for kx, ky, kw, kh, semitone in white_keys:
            if kx <= x < kx + kw and ky <= y < ky + kh:
                return semitone
        return None

    def focusInEvent(self, event):
        """Show keyboard hint when focused."""
        if self.hint_label:
            self.hint_label.setText("QWERTY to play, hold to sustain")
        self.update()

    def focusOutEvent(self, event):
        """Hide keyboard hint and release all sustained notes."""
        if self.hint_label:
            self.hint_label.setText("")
        self._release_all_sustained()
        self.update()

    def _key_to_semitone(self, key):
        """Convert keyboard key to semitone, adjusted for current pitch display."""
        if key not in self.KEYBOARD_MAP:
            return None
        # KEYBOARD_MAP values are relative to base display (pitch=0)
        # Round pitch to nearest octave so keyboard always plays "correct" notes
        base_semitone = self.KEYBOARD_MAP[key]
        pitch = self.pitch_getter()
        octave_shift = round(pitch / 12) * 12
        return base_semitone + octave_shift

    def keyPressEvent(self, event):
        """Handle keyboard input for playing notes with sustain."""
        if event.isAutoRepeat():
            return
        key = event.key()
        semitone = self._key_to_semitone(key)
        if semitone is not None:
            if semitone not in self._sustained_notes:
                self._start_sustained_note(semitone)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Stop sustained note when key released."""
        if event.isAutoRepeat():
            return
        key = event.key()
        semitone = self._key_to_semitone(key)
        if semitone is not None:
            self._stop_sustained_note(semitone)
        else:
            super().keyReleaseEvent(event)

    def _start_sustained_note(self, semitone):
        """Start a sustained note (keyboard input)."""
        from synth import note_on
        pitch, volume, program = self.settings_getter()
        midi_note = note_on(
            semitone,
            shift=-12 + pitch,
            volume=volume,
            program=program
        )
        self._sustained_notes[semitone] = midi_note
        self._pressed_keys.add(semitone)
        self.update()

    def _stop_sustained_note(self, semitone):
        """Stop a sustained note (keyboard input)."""
        if semitone in self._sustained_notes:
            from synth import note_off
            note_off(self._sustained_notes[semitone])
            del self._sustained_notes[semitone]
            self._pressed_keys.discard(semitone)
            self.update()

    def _release_all_sustained(self):
        """Release all sustained notes (e.g., on focus loss)."""
        from synth import note_off
        for midi_note in self._sustained_notes.values():
            note_off(midi_note)
        self._sustained_notes.clear()
        self._pressed_keys.clear()

    def mouseMoveEvent(self, event):
        key = self._key_at_pos(event.pos())
        if key != self._hover_key:
            self._hover_key = key
            self.update()
        # Handle dragging - sustain new key when dragged onto it
        if self._dragging and key is not None and key != self._last_drag_key:
            if self._last_drag_key is not None:
                self._stop_sustained_note(self._last_drag_key)
            self._last_drag_key = key
            self._start_sustained_note(key)

    def leaveEvent(self, event):
        self._hover_key = None
        if self._dragging:
            self._release_all_sustained()
        self._dragging = False
        self._last_drag_key = None
        self.update()

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == Qt.MouseButton.LeftButton:
            key = self._key_at_pos(event.pos())
            if key is not None:
                self._dragging = True
                self._last_drag_key = key
                self._start_sustained_note(key)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._last_drag_key is not None:
                self._stop_sustained_note(self._last_drag_key)
            self._dragging = False
            self._last_drag_key = None

    def trigger_key(self, semitone, duration=0.15):
        """Trigger a key visually (called when notes play externally).

        Thread-safe: emits signal to marshal to main Qt thread.
        """
        self._trigger_key_signal.emit(semitone, duration)

    def _do_trigger_key(self, semitone, duration):
        """Slot: actually trigger the key (runs on main thread)."""
        self._pressed_keys.add(semitone)
        self.update()
        QTimer.singleShot(int(duration * 1000), lambda s=semitone: self._release_key(s))

    def _release_key(self, semitone):
        """Release a key after external trigger (not sustained notes)."""
        if semitone not in self._sustained_notes:
            self._pressed_keys.discard(semitone)
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        white_keys, black_keys = self._get_key_layout()
        focused = self.hasFocus()

        # 50% opacity when unfocused
        if not focused:
            p.setOpacity(0.5)

        # Colors
        white_color = QColor(250, 250, 250)
        white_hover = QColor(230, 240, 255)
        white_pressed = QColor(200, 220, 255)
        black_color = QColor(30, 30, 30)
        black_hover = QColor(60, 60, 80)
        black_pressed = QColor(80, 80, 120)
        border_color = QColor(180, 180, 180)
        gap_color = QColor(160, 160, 160)

        # Draw white keys first
        for kx, ky, kw, kh, semitone in white_keys:
            if semitone in self._pressed_keys:
                p.setBrush(QBrush(white_pressed))
            elif semitone == self._hover_key:
                p.setBrush(QBrush(white_hover))
            else:
                p.setBrush(QBrush(white_color))
            p.setPen(QPen(border_color, 0.5))
            p.drawRect(QRectF(kx, ky, kw - 0.5, kh))
            p.setPen(QPen(gap_color, 0.5))
            p.drawLine(QPointF(kx + kw - 0.5, ky), QPointF(kx + kw - 0.5, kh))

        # Draw black keys on top
        for kx, ky, kw, kh, semitone in black_keys:
            if semitone in self._pressed_keys:
                p.setBrush(QBrush(black_pressed))
            elif semitone == self._hover_key:
                p.setBrush(QBrush(black_hover))
            else:
                p.setBrush(QBrush(black_color))
            p.setPen(QPen(QColor(20, 20, 20), 0.5))
            p.drawRoundedRect(QRectF(kx, ky, kw, kh), 1, 1)
