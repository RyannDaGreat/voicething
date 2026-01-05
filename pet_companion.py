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


def _get_pet_sound_category(pet_type: PetType) -> str:
    """Get the sound category (dog/cat/mouse) for a pet type."""
    if pet_type in (PetType.DOG, PetType.LPC_DOG_WHITE, PetType.LPC_DOG_TAN,
                    PetType.LPC_DOG_GOLDEN, PetType.LPC_DOG_BLACK):
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

        self.setFixedSize(64, 64)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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
        """Set whether the app is recording."""
        if is_listening:
            self.set_state(PetState.LISTENING)
        elif self._state == PetState.LISTENING:
            self.set_state(PetState.IDLE)

    def set_sleeping(self, is_sleeping: bool):
        """Set whether the pet should be sleeping."""
        if is_sleeping:
            self.set_state(PetState.SLEEPING)
        elif self._state == PetState.SLEEPING:
            self.set_state(PetState.IDLE)

    def trigger_copy(self):
        """Trigger copy celebration animation."""
        self.set_state(PetState.COPY, duration_ms=1500)

    def trigger_bark(self, play_sound: bool = True):
        """Trigger bark/meow/squeak animation with optional sound."""
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
        """Load the animation for the given state."""
        key = (self.pet_type, state)
        if key not in PET_ANIMATIONS:
            key = (self.pet_type, PetState.IDLE)

        filename, _ = PET_ANIMATIONS[key]
        filepath = get_pet_asset_path(self.pet_type, filename)

        if not os.path.exists(filepath):
            return

        if self._movie:
            self._movie.stop()
            self._movie = None

        if filename.endswith(".gif"):
            self._is_gif = True
            self._movie = QMovie(filepath)
            # Don't use setScaledSize - it causes blurry interpolation
            # Scale manually in paintEvent with FastTransformation instead
            self._movie.frameChanged.connect(self.update)
            self._movie.start()
        else:
            self._is_gif = False
            self._pixmap = QPixmap(filepath)
            if self._pixmap.width() > 32:
                self._pixmap = self._pixmap.copy(0, 0, 32, 32)
            self._pixmap = self._pixmap.scaled(
                64, 64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation
            )

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        if self._is_gif and self._movie:
            pixmap = self._movie.currentPixmap()
            if not pixmap.isNull():
                if self._key_color is not None:
                    pixmap = apply_color_key(pixmap, self._key_color)
                # Scale manually with FastTransformation (no blur)
                if pixmap.width() != 48 or pixmap.height() != 48:
                    pixmap = pixmap.scaled(
                        48, 48,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.FastTransformation
                    )
                x = (self.width() - pixmap.width()) // 2
                y = (self.height() - pixmap.height()) // 2
                painter.drawPixmap(x, y, pixmap)
        elif self._pixmap and not self._pixmap.isNull():
            x = (self.width() - self._pixmap.width()) // 2
            y = (self.height() - self._pixmap.height()) // 2
            painter.drawPixmap(x, y, self._pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_state(PetState.PETTING, duration_ms=1200)
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


class PetContainer(QWidget):
    """Container widget that holds one or more pets."""

    pet_clicked = pyqtSignal(PetType)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pets: dict[PetType, PetCompanionWidget] = {}
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
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
        """Arrange pets horizontally."""
        x = 0
        for pet in self._pets.values():
            pet.move(x, 0)
            pet.show()
            x += pet.width() + 4

        if self._pets:
            self.setFixedSize(x - 4, 64)
        else:
            self.setFixedSize(0, 0)

    def set_listening(self, is_listening: bool):
        for pet in self._pets.values():
            pet.set_listening(is_listening)

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
ALL_PET_TYPES = ORIGINAL_PET_TYPES + LPC_DOG_TYPES + LPC_CAT_TYPES
