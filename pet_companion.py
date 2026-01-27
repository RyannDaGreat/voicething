"""Pet companion widget system - animated pixel art pets for VoiceThing.

Supports multiple pet types with animation states tied to app behavior:
- Idle: relaxed pose, occasional idle animations
- Listening: alert pose when recording
- Sleeping: snoozing animation when app is inactive
- Petting: happy animation when clicked
- Copy: celebrates when text is copied

Includes LPC Cats & Dogs (CC-BY 3.0) with sleep/eat animations.
"""

import os
import random
import subprocess
from enum import Enum, auto
from typing import Optional

from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap, QMovie, QPainter, QColor, QImage
from PyQt6.QtWidgets import QWidget


# Background colors to key out (make transparent) for each pet type
BG_COLORS_TO_KEY = {
    "dog": QColor(164, 117, 160),
    "cat": QColor(164, 117, 160),
    "mouse": None,  # PNG has proper alpha
    # LPC pets have proper alpha in PNGs/GIFs
    "lpc_dog_white": None, "lpc_dog_tan": None,
    "lpc_dog_golden": None, "lpc_dog_black": None,
    "lpc_cat_white": None, "lpc_cat_orange": None,
    "lpc_cat_gray": None, "lpc_cat_black": None,
    # Emmy has proper alpha
    "emmy": None,
}


def apply_color_key(pixmap: QPixmap, key_color: QColor, tolerance: int = 15) -> QPixmap:
    """Apply color keying to make background color transparent."""
    if pixmap.isNull() or key_color is None:
        return pixmap
    image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    kr, kg, kb = key_color.red(), key_color.green(), key_color.blue()
    for y in range(image.height()):
        for x in range(image.width()):
            pixel = image.pixelColor(x, y)
            if (abs(pixel.red() - kr) <= tolerance and
                abs(pixel.green() - kg) <= tolerance and
                abs(pixel.blue() - kb) <= tolerance):
                image.setPixelColor(x, y, QColor(0, 0, 0, 0))
    return QPixmap.fromImage(image)


_MODULE_DIR = os.path.dirname(__file__)
PETS_DIR = os.path.join(_MODULE_DIR, "assets", "pets")
SOUNDS_DIR = os.path.join(_MODULE_DIR, "assets", "sounds")

# Sound files for each pet type category
PET_SOUNDS = {
    "dog": os.path.join(SOUNDS_DIR, "dog_bark.wav"),
    "cat": os.path.join(SOUNDS_DIR, "cat_meow.mp3"),
    "mouse": os.path.join(SOUNDS_DIR, "mouse_squeak.mp3"),
}


class PetState(Enum):
    """Animation states for pets."""
    IDLE = auto()
    LISTENING = auto()
    SLEEPING = auto()
    PETTING = auto()
    COPY = auto()
    BARK = auto()
    EATING = auto()
    HOVER = auto()       # Mouse hover (blink/tilt for Emmy)
    # Emmy-specific states
    RECORD = auto()      # Spinning on vinyl record
    GRAMOPHONE = auto()  # Listening to gramophone
    ROLLING = auto()     # Belly rub / rolling
    BUTTON = auto()      # Pushing red button
    TOAST = auto()       # Eating toast


class PetType(Enum):
    """Available pet types."""
    # Original pets
    DOG = "dog"
    CAT = "cat"
    MOUSE = "mouse"
    # LPC dogs (cute, with sleep/eat animations)
    LPC_DOG_WHITE = "lpc_dog_white"
    LPC_DOG_TAN = "lpc_dog_tan"
    LPC_DOG_GOLDEN = "lpc_dog_golden"
    LPC_DOG_BLACK = "lpc_dog_black"
    # LPC cats
    LPC_CAT_WHITE = "lpc_cat_white"
    LPC_CAT_ORANGE = "lpc_cat_orange"
    LPC_CAT_GRAY = "lpc_cat_gray"
    LPC_CAT_BLACK = "lpc_cat_black"
    # Emmy - special dog with unique animations
    EMMY = "emmy"


# Animation mappings: (PetType, PetState) -> (filename, loop_count)
# loop_count: -1 = infinite, positive = play N times then stop
PET_ANIMATIONS = {
    # Original Dog
    (PetType.DOG, PetState.IDLE): ("dog_sitx2.gif", -1),
    (PetType.DOG, PetState.LISTENING): ("dog_sit_lookx2.gif", -1),
    (PetType.DOG, PetState.SLEEPING): ("dog_sitx2.gif", -1),
    (PetType.DOG, PetState.PETTING): ("dog_sit_lookx2.gif", 2),
    (PetType.DOG, PetState.COPY): ("dog_sit_barkx2.gif", 1),
    (PetType.DOG, PetState.BARK): ("dog_sit_barkx2.gif", 1),
    (PetType.DOG, PetState.EATING): ("dog_sitx2.gif", -1),

    # Original Cat
    (PetType.CAT, PetState.IDLE): ("catwalkx2.gif", -1),
    (PetType.CAT, PetState.LISTENING): ("catrunx2.gif", -1),
    (PetType.CAT, PetState.SLEEPING): ("catwalkx2.gif", -1),
    (PetType.CAT, PetState.PETTING): ("catrunx2.gif", 2),
    (PetType.CAT, PetState.COPY): ("catrunx2.gif", 1),
    (PetType.CAT, PetState.BARK): ("catrunx2.gif", 1),
    (PetType.CAT, PetState.EATING): ("catwalkx2.gif", -1),

    # Mouse
    (PetType.MOUSE, PetState.IDLE): ("mouse.png", -1),
    (PetType.MOUSE, PetState.LISTENING): ("mouse.png", -1),
    (PetType.MOUSE, PetState.SLEEPING): ("mouse.png", -1),
    (PetType.MOUSE, PetState.PETTING): ("mouse.png", 2),
    (PetType.MOUSE, PetState.COPY): ("mouse.png", 1),
    (PetType.MOUSE, PetState.BARK): ("mouse.png", 1),
    (PetType.MOUSE, PetState.EATING): ("mouse.png", -1),
}

# Add LPC dog animations for all color variants
for color in ["white", "tan", "golden", "black"]:
    pt = PetType(f"lpc_dog_{color}")
    PET_ANIMATIONS[(pt, PetState.IDLE)] = ("idle.png", -1)
    PET_ANIMATIONS[(pt, PetState.LISTENING)] = ("walk_down.gif", -1)
    PET_ANIMATIONS[(pt, PetState.SLEEPING)] = ("sleep.gif", -1)
    PET_ANIMATIONS[(pt, PetState.PETTING)] = ("walk_down.gif", 2)
    PET_ANIMATIONS[(pt, PetState.COPY)] = ("walk_right.gif", 1)
    PET_ANIMATIONS[(pt, PetState.BARK)] = ("walk_left.gif", 1)
    PET_ANIMATIONS[(pt, PetState.EATING)] = ("eat.gif", -1)

# Add LPC cat animations for all color variants
for color in ["white", "orange", "gray", "black"]:
    pt = PetType(f"lpc_cat_{color}")
    PET_ANIMATIONS[(pt, PetState.IDLE)] = ("idle.png", -1)
    PET_ANIMATIONS[(pt, PetState.LISTENING)] = ("walk_down.gif", -1)
    PET_ANIMATIONS[(pt, PetState.SLEEPING)] = ("sleep.gif", -1)
    PET_ANIMATIONS[(pt, PetState.PETTING)] = ("walk_down.gif", 2)
    PET_ANIMATIONS[(pt, PetState.COPY)] = ("walk_right.gif", 1)
    PET_ANIMATIONS[(pt, PetState.BARK)] = ("walk_left.gif", 1)
    PET_ANIMATIONS[(pt, PetState.EATING)] = ("eat.gif", -1)

# Emmy animations - special dog with unique behaviors
# See assets/pets/emmy2/create_gifs.py for sprite documentation
PET_ANIMATIONS[(PetType.EMMY, PetState.IDLE)] = ("idle.png", -1)        # STILL image, not animated
PET_ANIMATIONS[(PetType.EMMY, PetState.HOVER)] = ("hover.gif", -1)      # Blink/tilt on mouse hover
PET_ANIMATIONS[(PetType.EMMY, PetState.LISTENING)] = ("record.gif", -1) # or gramophone (50/50)
PET_ANIMATIONS[(PetType.EMMY, PetState.SLEEPING)] = ("idle.png", -1)
PET_ANIMATIONS[(PetType.EMMY, PetState.PETTING)] = ("rolling.gif", 2)   # or toast (50/50)
PET_ANIMATIONS[(PetType.EMMY, PetState.COPY)] = ("bark.gif", 1)
PET_ANIMATIONS[(PetType.EMMY, PetState.BARK)] = ("bark.gif", 1)         # or button (50/50)
PET_ANIMATIONS[(PetType.EMMY, PetState.EATING)] = ("toast.gif", -1)
# Emmy-specific states
PET_ANIMATIONS[(PetType.EMMY, PetState.RECORD)] = ("record.gif", -1)
PET_ANIMATIONS[(PetType.EMMY, PetState.GRAMOPHONE)] = ("gramophone.gif", -1)
PET_ANIMATIONS[(PetType.EMMY, PetState.ROLLING)] = ("rolling.gif", 2)
PET_ANIMATIONS[(PetType.EMMY, PetState.BUTTON)] = ("button.gif", 1)
PET_ANIMATIONS[(PetType.EMMY, PetState.TOAST)] = ("toast.gif", 2)


def _get_pet_sound_category(pet_type: PetType) -> str:
    """Get the sound category (dog/cat/mouse) for a pet type."""
    if pet_type in (PetType.DOG, PetType.LPC_DOG_WHITE, PetType.LPC_DOG_TAN,
                    PetType.LPC_DOG_GOLDEN, PetType.LPC_DOG_BLACK, PetType.EMMY):
        return "dog"
    elif pet_type in (PetType.CAT, PetType.LPC_CAT_WHITE, PetType.LPC_CAT_ORANGE,
                      PetType.LPC_CAT_GRAY, PetType.LPC_CAT_BLACK):
        return "cat"
    return "mouse"


def _play_sound(sound_path: str) -> None:
    """Play a sound file using macOS afplay (non-blocking)."""
    if os.path.exists(sound_path):
        subprocess.Popen(["afplay", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_pet_asset_path(pet_type: PetType, filename: str) -> str:
    """Get the full path to a pet asset file."""
    if pet_type == PetType.DOG:
        return os.path.join(PETS_DIR, "dog", filename)
    elif pet_type == PetType.CAT:
        return os.path.join(PETS_DIR, "cat", "cat sprite", filename)
    elif pet_type == PetType.MOUSE:
        return os.path.join(PETS_DIR, "rodent", "PNG", "32x32", filename)
    elif pet_type == PetType.EMMY:
        return os.path.join(PETS_DIR, "emmy2", filename)
    elif pet_type.value.startswith("lpc_"):
        # LPC pets are in lpc/{pet_type.value}/
        return os.path.join(PETS_DIR, "lpc", pet_type.value, filename)
    raise ValueError(f"Unknown pet type: {pet_type}")


class PetCompanionWidget(QWidget):
    """Animated pet companion widget."""

    clicked = pyqtSignal()

    def __init__(self, pet_type: PetType = PetType.LPC_DOG_GOLDEN, parent=None):
        super().__init__(parent)
        self.pet_type = pet_type
        self._state = PetState.IDLE
        self._movie: Optional[QMovie] = None
        self._pixmap: Optional[QPixmap] = None
        self._is_gif = False
        self._key_color: Optional[QColor] = BG_COLORS_TO_KEY.get(pet_type.value)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._sprite_size = (64, 64)  # Will be updated when sprite loads

        self._return_timer = QTimer(self)
        self._return_timer.setSingleShot(True)
        self._return_timer.timeout.connect(self._return_to_idle)

        self._load_animation(PetState.IDLE)

    @property
    def state(self) -> PetState:
        return self._state

    def set_state(self, state: PetState, duration_ms: int = 0):
        """Set the pet's animation state."""
        if state == self._state:
            return
        self._state = state
        self._load_animation(state)
        if duration_ms > 0:
            self._return_timer.start(duration_ms)
        else:
            self._return_timer.stop()

    def set_listening(self, is_listening: bool):
        """Set whether the app is recording.

        Emmy behavior: gramophone when recording (listening to you speak)
        """
        if is_listening:
            if self.pet_type == PetType.EMMY:
                # Emmy: gramophone while recording (listening)
                self.set_state(PetState.GRAMOPHONE)
            else:
                self.set_state(PetState.LISTENING)
        elif self._state in (PetState.LISTENING, PetState.RECORD, PetState.GRAMOPHONE):
            self.set_state(PetState.IDLE)

    def set_processing(self, is_processing: bool):
        """Set whether the app is transcribing/processing.

        Emmy behavior: record spin while processing/transcribing
        Does NOT interrupt bark/button/copy animations.
        """
        if is_processing:
            if self.pet_type == PetType.EMMY:
                self.set_state(PetState.RECORD)
            else:
                # Other pets could have a processing animation here
                pass
        elif self._state == PetState.RECORD:
            # Only return to idle if still in RECORD state
            # Don't interrupt bark/button/copy animations
            self.set_state(PetState.IDLE)

    def set_sleeping(self, is_sleeping: bool):
        """Set whether the pet should be sleeping."""
        if is_sleeping:
            self.set_state(PetState.SLEEPING)
        elif self._state == PetState.SLEEPING:
            self.set_state(PetState.IDLE)

    def trigger_copy(self):
        """Trigger copy celebration animation.

        Emmy behavior: 50% bark, 50% push red button (same as done)
        """
        if self.pet_type == PetType.EMMY:
            state = random.choice([PetState.BARK, PetState.BUTTON])
            self.set_state(state, duration_ms=1500)
        else:
            self.set_state(PetState.COPY, duration_ms=1500)

    def trigger_bark(self, play_sound: bool = True):
        """Trigger bark/meow/squeak animation with optional sound.

        Emmy behavior: 50% bark, 50% push red button
        """
        if self.pet_type == PetType.EMMY:
            state = random.choice([PetState.BARK, PetState.BUTTON])
            self.set_state(state, duration_ms=1500)
        else:
            self.set_state(PetState.BARK, duration_ms=1000)
        if play_sound:
            category = _get_pet_sound_category(self.pet_type)
            sound_path = PET_SOUNDS.get(category)
            if sound_path:
                _play_sound(sound_path)

    def trigger_eating(self):
        """Trigger eating animation (LPC pets only)."""
        self.set_state(PetState.EATING, duration_ms=2000)

    def set_pet_type(self, pet_type: PetType):
        """Change the pet type and reload animations."""
        self.pet_type = pet_type
        self._load_animation(self._state)

    def _return_to_idle(self):
        """Return to idle state after temporary animation."""
        self._state = PetState.IDLE
        self._load_animation(PetState.IDLE)

    def _load_animation(self, state: PetState):
        """Load the animation for the given state.

        PIXEL ART RULES (TOP PRIORITY, NO EXCEPTIONS):
        - ALL pixels must be used (no cropping)
        - ALL pixels must be square (integer scaling only: 1x, 2x, 3x, 4x)
        - NEVER scale to non-integer multiples (1.5x, 2.7x, etc.)
        - If it doesn't fit, fix the container, not the sprite
        """
        key = (self.pet_type, state)
        if key not in PET_ANIMATIONS:
            key = (self.pet_type, PetState.IDLE)

        filename, _ = PET_ANIMATIONS[key]
        filepath = get_pet_asset_path(self.pet_type, filename)

        if not os.path.exists(filepath):
            return

        if self._movie:
            self._movie.stop()
            self._movie.frameChanged.disconnect()
            self._movie.deleteLater()
            self._movie = None

        if filename.endswith(".gif"):
            self._is_gif = True
            self._movie = QMovie(filepath)
            self._movie.setParent(self)  # Parent to widget so it's deleted together
            self._movie.setCacheMode(QMovie.CacheMode.CacheAll)  # Cache frames for smooth playback
            # Get size before starting (non-blocking)
            self._movie.jumpToFrame(0)
            frame = self._movie.currentPixmap()
            if not frame.isNull():
                self._sprite_size = (frame.width(), frame.height())
            # Connect directly to update slot (no lambda)
            self._movie.frameChanged.connect(self.update)
            self._movie.start()
        else:
            self._is_gif = False
            self._pixmap = QPixmap(filepath)
            if not self._pixmap.isNull():
                self._sprite_size = (self._pixmap.width(), self._pixmap.height())

        # Resize widget to fit sprite (no clipping!)
        self.setFixedSize(self._sprite_size[0], self._sprite_size[1])
        self.update()

        # Tell parent to re-arrange (sizes may have changed)
        if self.parent():
            parent = self.parent()
            if hasattr(parent, '_arrange_pets'):
                parent._arrange_pets()

    def paintEvent(self, event):
        """Render the pet sprite.

        PIXEL ART RULES (TOP PRIORITY, NO EXCEPTIONS):
        - ALL pixels must be used (no cropping)
        - ALL pixels must be square (integer scaling only: 1x, 2x, 3x, 4x)
        - NEVER scale to non-integer multiples - this makes pixels different sizes
        - If it doesn't fit, fix the container, not the sprite
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        pixmap = None
        if self._is_gif and self._movie:
            pixmap = self._movie.currentPixmap()
        elif self._pixmap:
            pixmap = self._pixmap

        if pixmap is None or pixmap.isNull():
            return

        # Apply color keying if needed
        if self._key_color is not None:
            pixmap = apply_color_key(pixmap, self._key_color)

        # Calculate largest INTEGER scale that fits (1x, 2x, 3x, etc.)
        # NEVER use fractional scaling - it makes pixels different sizes
        src_w, src_h = pixmap.width(), pixmap.height()
        scale_x = self.width() // src_w
        scale_y = self.height() // src_h
        scale = max(1, min(scale_x, scale_y))  # At least 1x, largest integer that fits

        # Scale ONLY by integer multiple using nearest neighbor
        if scale > 1:
            pixmap = pixmap.scaled(
                src_w * scale, src_h * scale,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )

        # Center in widget
        x = (self.width() - pixmap.width()) // 2
        y = (self.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)

    def mousePressEvent(self, event):
        """Handle click - trigger petting animation.

        Emmy behavior: 50% rolling (belly rub), 50% toast (fed bread)
        """
        if event.button() == Qt.MouseButton.LeftButton:
            if self.pet_type == PetType.EMMY:
                state = random.choice([PetState.ROLLING, PetState.TOAST])
                self.set_state(state, duration_ms=2000)
            else:
                self.set_state(PetState.PETTING, duration_ms=1200)
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Mouse entered - Emmy shows blink/tilt animation on hover."""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.pet_type == PetType.EMMY and self._state == PetState.IDLE:
            self.set_state(PetState.HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse left - Emmy returns to still idle."""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        if self.pet_type == PetType.EMMY and self._state == PetState.HOVER:
            self.set_state(PetState.IDLE)
        super().leaveEvent(event)


class PetContainer(QWidget):
    """Container widget that holds one or more pets."""

    pet_clicked = pyqtSignal(PetType)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pets: dict[PetType, PetCompanionWidget] = {}
        self._raise_by = 0  # How much pets are raised above container bottom
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setMinimumSize(64, 64)

    def add_pet(self, pet_type: PetType) -> PetCompanionWidget:
        """Add a pet of the given type."""
        if pet_type in self._pets:
            return self._pets[pet_type]

        pet = PetCompanionWidget(pet_type, self)
        pet.clicked.connect(lambda pt=pet_type: self.pet_clicked.emit(pt))
        self._pets[pet_type] = pet
        self._arrange_pets()
        return pet

    def remove_pet(self, pet_type: PetType):
        """Remove a pet."""
        if pet_type in self._pets:
            self._pets[pet_type].deleteLater()
            del self._pets[pet_type]
            self._arrange_pets()

    def get_pet(self, pet_type: PetType) -> Optional[PetCompanionWidget]:
        """Get a pet widget by type."""
        return self._pets.get(pet_type)

    def set_pets(self, pet_types: list[PetType]):
        """Set which pets are active."""
        for pt in list(self._pets.keys()):
            if pt not in pet_types:
                self.remove_pet(pt)
        for pt in pet_types:
            self.add_pet(pt)

    def _arrange_pets(self):
        """Arrange pets horizontally, raised by 1/3 of max height.

        Container is made taller to accommodate raised pets without clipping.
        Pets are positioned at y=0 (top of container), and container height
        includes extra space at bottom so pets appear to float above.
        """
        if not self._pets:
            self._raise_by = 0
            self.setFixedSize(0, 0)
            return

        # Find max height and total width
        max_h = max(pet.height() for pet in self._pets.values())
        total_w = sum(pet.width() for pet in self._pets.values()) + 4 * (len(self._pets) - 1)

        # Raise all pets by 1/3 of max height
        self._raise_by = max_h // 3

        # Container height = max_h + raise_by to fit raised pets without clipping
        # Pets at y=0 means they occupy top portion, bottom portion is empty space
        self.setFixedSize(total_w, max_h + self._raise_by)

        # Position pets at y=0 (top of container), so they appear raised
        x = 0
        for pet in self._pets.values():
            pet.move(x, 0)
            pet.show()
            x += pet.width() + 4

    @property
    def raise_amount(self) -> int:
        """How many pixels pets are raised above the container's layout baseline."""
        return self._raise_by

    def set_listening(self, is_listening: bool):
        for pet in self._pets.values():
            pet.set_listening(is_listening)

    def set_processing(self, is_processing: bool):
        for pet in self._pets.values():
            pet.set_processing(is_processing)

    def set_sleeping(self, is_sleeping: bool):
        for pet in self._pets.values():
            pet.set_sleeping(is_sleeping)

    def trigger_copy(self):
        for pet in self._pets.values():
            pet.trigger_copy()

    def trigger_bark(self, pet_type: Optional[PetType] = None, play_sound: bool = True):
        if pet_type and pet_type in self._pets:
            self._pets[pet_type].trigger_bark(play_sound=play_sound)
        else:
            # Only play sound once even if multiple pets
            first = True
            for pet in self._pets.values():
                pet.trigger_bark(play_sound=play_sound and first)
                first = False


def get_pet_icon(pet_type: PetType, size: int = 24) -> QPixmap:
    """Get a small icon pixmap for a pet type."""
    # Determine icon path based on pet type
    if pet_type == PetType.DOG:
        path = get_pet_asset_path(PetType.DOG, "dog_sitx1.gif")
    elif pet_type == PetType.CAT:
        path = get_pet_asset_path(PetType.CAT, "catwalkx2.gif")
    elif pet_type == PetType.MOUSE:
        path = get_pet_asset_path(PetType.MOUSE, "mouse.png")
    elif pet_type == PetType.EMMY:
        path = get_pet_asset_path(PetType.EMMY, "idle.png")  # Sitting still
    elif pet_type.value.startswith("lpc_"):
        path = get_pet_asset_path(pet_type, "idle.png")
    else:
        return QPixmap(size, size)

    if not os.path.exists(path):
        return QPixmap(size, size)

    if path.endswith(".gif"):
        movie = QMovie(path)
        movie.jumpToFrame(0)
        pixmap = movie.currentPixmap()
    else:
        pixmap = QPixmap(path)
        if pixmap.width() > 32:
            pixmap = pixmap.copy(0, 0, 32, 32)

    key_color = BG_COLORS_TO_KEY.get(pet_type.value)
    if key_color is not None:
        pixmap = apply_color_key(pixmap, key_color)

    return pixmap.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.FastTransformation
    )


# Convenience: group pet types by category
LPC_DOG_TYPES = [PetType.LPC_DOG_WHITE, PetType.LPC_DOG_TAN, PetType.LPC_DOG_GOLDEN, PetType.LPC_DOG_BLACK]
LPC_CAT_TYPES = [PetType.LPC_CAT_WHITE, PetType.LPC_CAT_ORANGE, PetType.LPC_CAT_GRAY, PetType.LPC_CAT_BLACK]
ORIGINAL_PET_TYPES = [PetType.DOG, PetType.CAT, PetType.MOUSE]
SPECIAL_PET_TYPES = [PetType.EMMY]
ALL_PET_TYPES = ORIGINAL_PET_TYPES + LPC_DOG_TYPES + LPC_CAT_TYPES + SPECIAL_PET_TYPES
