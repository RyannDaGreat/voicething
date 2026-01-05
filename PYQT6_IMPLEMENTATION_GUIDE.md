# PyQt6 Frutiger Aero Implementation Guide
## Practical Code Examples for Audio Recording App

---

## 1. COLOR CONSTANTS DEFINITION

Create a `colors.py` file for consistent color usage:

```python
from enum import Enum

class FrutigerAeroColors(Enum):
    """Frutiger Aero color palette for PyQt6 audio app"""

    # Primary Blues
    AZURE_DRAGON = "#003c78"
    PRINCESS_BLUE = "#0050a0"
    COBALT_STONE = "#0064b4"
    MYSTERY_OCEANS = "#003c8c"
    SCIENCE_BLUE = "#0078c8"
    RUSHING_STREAM = "#64c8dc"

    # Extended Colors
    ELECTRIC_BLUE = "#0689e4"
    GRASS_GREEN = "#71ab23"
    GOLDEN_YELLOW = "#fbb905"
    BURNT_ORANGE = "#d55e0f"
    DEEP_ELECTRIC = "#0032db"

    # Aqua Variants
    EASTERN_BLUE = "#1299ca"
    SCOOTER = "#35bcde"
    SKY_BLUE = "#6fd7ec"
    ICE_COLD = "#9ceff2"
    FANTASY = "#faefef"

    # Green Palette
    DARK_OLIVE = "#394e1b"
    MOSS_GREEN = "#6b8f25"
    LIME = "#9fe11d"
    LIGHT_LIME = "#ccff7c"
    PALE_LIME = "#f1ffcd"

    # Backgrounds
    WHITE = "#ffffff"
    ALICE_BLUE = "#f0f8ff"
    SOFT_CYAN = "#e8f4f8"

    # Dark Theme
    DARK_BACKGROUND = "#1a2a3a"
    DARK_SURFACE = "#2a3a4a"

    def __str__(self):
        return self.value

# Helper function to convert to QColor
from PyQt6.QtGui import QColor

def get_qcolor(color_enum):
    """Convert FrutigerAeroColors enum to QColor"""
    return QColor(str(color_enum))
```

---

## 2. GLOSSY BUTTON IMPLEMENTATION

```python
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QSize

class GlossyButton(QPushButton):
    """
    Custom glossy button with Frutiger Aero styling.
    Supports gradient fill, glass effect, and state variations.
    """

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(75, 23)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set font
        font = QFont("Frutiger, Segoe UI, sans-serif", 11)
        font.setBold(True)
        self.setFont(font)

        # Remove default styling
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create gradient based on state
        gradient = self._create_gradient()

        # Draw rounded rectangle with gradient
        painter.fillRect(self.rect(), gradient)

        # Draw border
        border_color = QColor(0, 120, 200, 128)
        painter.setPen(QPen(border_color, 1))
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 3, 3)

        # Draw inset highlight (glossy effect)
        highlight_gradient = QLinearGradient(0, 0, 0, 4)
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 80))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(1, 1, self.width() - 2, 4, highlight_gradient)

        # Draw text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()

    def _create_gradient(self):
        """Create gradient based on button state"""
        gradient = QLinearGradient(0, 0, 0, self.height())

        if self.isDown() or self.isChecked():
            # Pressed state - darker blue
            gradient.setColorAt(0.0, QColor(0, 100, 180))
            gradient.setColorAt(0.5, QColor(0, 60, 120))
            gradient.setColorAt(1.0, QColor(26, 42, 58))
        elif self.underMouse():
            # Hover state - bright blue
            gradient.setColorAt(0.0, QColor(232, 244, 248))
            gradient.setColorAt(0.1, QColor(176, 208, 224))
            gradient.setColorAt(0.5, QColor(0, 120, 200))
            gradient.setColorAt(0.9, QColor(0, 80, 160))
            gradient.setColorAt(1.0, QColor(0, 60, 120))
        else:
            # Normal state
            gradient.setColorAt(0.0, QColor(176, 208, 224))
            gradient.setColorAt(0.5, QColor(0, 120, 200))
            gradient.setColorAt(1.0, QColor(0, 60, 120))

        return gradient

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.update()
```

---

## 3. GLASS PANEL IMPLEMENTATION

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen
from PyQt6.QtCore import Qt

class GlassPanel(QWidget):
    """
    Translucent glass effect panel with Frutiger Aero styling.
    Creates that characteristic Windows Aero glass appearance.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create gradient for glass effect
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(255, 255, 255, 70))    # White semi-transparent
        gradient.setColorAt(0.2, QColor(176, 208, 224, 120))   # Light cyan
        gradient.setColorAt(0.5, QColor(100, 200, 220, 100))   # Cyan semi-transparent
        gradient.setColorAt(1.0, QColor(0, 120, 200, 80))      # Blue semi-transparent

        # Draw background with gradient
        painter.fillRect(self.rect(), gradient)

        # Draw border
        border_color = QColor(0, 120, 200, 128)
        painter.setPen(QPen(border_color, 1))
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 4, 4)

        # Draw inset shadow for depth
        shadow_gradient = QLinearGradient(0, 0, 0, 10)
        shadow_gradient.setColorAt(0, QColor(135, 135, 135, 25))
        shadow_gradient.setColorAt(1, QColor(135, 135, 135, 0))
        painter.fillRect(1, 1, self.width() - 2, 10, shadow_gradient)

        painter.end()
```

---

## 4. CUSTOM SLIDER WITH GLOSSY HANDLE

```python
from PyQt6.QtWidgets import QSlider
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen
from PyQt6.QtCore import Qt

class GlossySlider(QSlider):
    """
    Custom slider with glossy Frutiger Aero styling.
    Vertical or horizontal with gradient handle.
    """

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setMinimumHeight(30) if orientation == Qt.Orientation.Horizontal else self.setMinimumWidth(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw groove (track)
        if self.orientation() == Qt.Orientation.Horizontal:
            groove_rect = self.rect()
            groove_rect.setTop(groove_rect.center().y() - 3)
            groove_rect.setHeight(6)

            # Groove gradient
            groove_gradient = QLinearGradient(0, groove_rect.top(), 0, groove_rect.bottom())
            groove_gradient.setColorAt(0.0, QColor(232, 244, 248))  # Light cyan
            groove_gradient.setColorAt(1.0, QColor(100, 200, 220))  # Cyan

            painter.fillRect(groove_rect, groove_gradient)

            # Groove border
            painter.setPen(QPen(QColor(0, 120, 200, 100), 1))
            painter.drawRoundedRect(groove_rect, 3, 3)

            # Draw slider handle
            handle_x = int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (self.width() - 18))
            handle_rect = self.rect()
            handle_rect.setLeft(handle_x)
            handle_rect.setWidth(18)
            handle_rect.setTop(self.rect().center().y() - 9)
            handle_rect.setHeight(18)

            self._paint_handle(painter, handle_rect, self.isSliderDown())

        painter.end()

    def _paint_handle(self, painter, rect, pressed):
        """Paint the slider handle with glossy effect"""
        # Handle gradient
        handle_gradient = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        if pressed:
            handle_gradient.setColorAt(0.0, QColor(0, 100, 180))
            handle_gradient.setColorAt(0.5, QColor(0, 60, 120))
            handle_gradient.setColorAt(1.0, QColor(26, 42, 58))
        else:
            handle_gradient.setColorAt(0.0, QColor(255, 255, 255, 200))
            handle_gradient.setColorAt(0.1, QColor(176, 208, 224))
            handle_gradient.setColorAt(0.5, QColor(0, 120, 200))
            handle_gradient.setColorAt(0.9, QColor(0, 80, 160))
            handle_gradient.setColorAt(1.0, QColor(0, 60, 120))

        painter.fillRect(rect, handle_gradient)

        # Border
        painter.setPen(QPen(QColor(0, 80, 160), 1))
        painter.drawRoundedRect(rect, 4, 4)

        # Highlight for glossy effect
        highlight_gradient = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.top() + 4)
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 100))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(rect.left() + 1, rect.top() + 1, rect.width() - 2, 4, highlight_gradient)
```

---

## 5. WAVEFORM VISUALIZATION

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen
from PyQt6.QtCore import Qt
import numpy as np

class WaveformVisualization(QWidget):
    """
    Waveform display with Frutiger Aero gradient styling.
    Displays audio waveform data with glossy appearance.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.waveform_data = np.array([])
        self.setMinimumHeight(120)
        self.setStyleSheet("background-color: #f0f8ff;")  # Alice blue

    def set_waveform_data(self, data):
        """Update waveform data (normalized -1 to 1)"""
        self.waveform_data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background panel with subtle gradient
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        bg_gradient.setColorAt(0.0, QColor(240, 248, 255))    # Alice blue
        bg_gradient.setColorAt(1.0, QColor(232, 244, 248))    # Soft cyan
        painter.fillRect(self.rect(), bg_gradient)

        if len(self.waveform_data) == 0:
            painter.end()
            return

        # Draw center line
        center_y = self.height() / 2
        painter.setPen(QPen(QColor(100, 200, 220, 50), 1))
        painter.drawLine(0, int(center_y), self.width(), int(center_y))

        # Draw waveform
        self._draw_waveform(painter)

        # Draw border
        painter.setPen(QPen(QColor(0, 120, 200), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        painter.end()

    def _draw_waveform(self, painter):
        """Draw the waveform with gradient coloring"""
        if len(self.waveform_data) < 2:
            return

        center_y = self.height() / 2
        max_height = center_y - 5
        pixels_per_sample = self.width() / len(self.waveform_data)

        # Create gradient for waveform coloring
        wave_gradient = QLinearGradient(0, center_y - max_height, 0, center_y + max_height)
        wave_gradient.setColorAt(0.0, QColor(0, 60, 120))      # Azure (high)
        wave_gradient.setColorAt(0.3, QColor(0, 100, 180))     # Cobalt
        wave_gradient.setColorAt(0.5, QColor(0, 120, 200))     # Science blue
        wave_gradient.setColorAt(0.7, QColor(100, 200, 220))   # Cyan
        wave_gradient.setColorAt(1.0, QColor(100, 200, 220))   # Cyan (low)

        # Draw waveform as filled area
        path_points = []
        for i, sample in enumerate(self.waveform_data):
            x = i * pixels_per_sample
            y = center_y - (sample * max_height)
            path_points.append((x, y))

        # Draw upper waveform
        painter.setPen(QPen(QColor(0, 120, 200), 2))
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Draw lower waveform (mirror)
        painter.setPen(QPen(QColor(0, 100, 180), 2))
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            painter.drawLine(int(x1), int(2 * center_y - y1),
                           int(x2), int(2 * center_y - y2))

        # Optional: Draw semi-transparent fill
        painter.setOpacity(0.3)
        painter.setBrush(wave_gradient)
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            painter.drawPolygon(
                [int(x1), int(y1), int(x2), int(y2),
                 int(x2), int(2 * center_y - y2), int(x1), int(2 * center_y - y1)]
            )
        painter.setOpacity(1.0)
```

---

## 6. QSS STYLESHEET (COMPLETE THEME)

```css
/* Frutiger Aero Theme for PyQt6 - Complete QSS Stylesheet */

/* Global Style */
QWidget {
    background-color: #ffffff;
    color: #003c78;
    font-family: "Frutiger", "Segoe UI", sans-serif;
    font-size: 11px;
}

/* Main Window */
QMainWindow {
    background-color: #f0f8ff;
}

/* Push Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #b0d0e0, stop:0.5 #0078c8, stop:1 #003c78);
    color: white;
    border: 1px solid #0050a0;
    border-radius: 3px;
    padding: 4px 12px;
    font-weight: bold;
    min-width: 75px;
    min-height: 23px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e8f4f8, stop:0.5 #0078c8, stop:1 #0050a0);
    border-color: #003c78;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0064b4, stop:0.5 #003c78, stop:1 #1a2a3a);
    border-color: #003c78;
    padding: 5px 11px 3px 13px;
}

QPushButton:focus {
    outline: 2px solid #0078c8;
    outline-offset: 2px;
}

/* Line Edits */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 3px;
    padding: 4px;
    color: #003c78;
    selection-background-color: #0078c8;
    selection-color: white;
}

QLineEdit:focus {
    border: 2px solid #0078c8;
    padding: 3px;
}

/* Text Edits */
QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 3px;
    color: #003c78;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #0078c8;
}

/* Labels */
QLabel {
    color: #003c78;
    font-weight: normal;
}

QLabel[strong="true"] {
    font-weight: bold;
}

/* Group Box */
QGroupBox {
    border: 1px solid #64c8dc;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    color: #003c78;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px;
}

/* Sliders */
QSlider::groove:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e8f4f8, stop:1 #64c8dc);
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffffff, stop:0.1 #b0d0e0,
                                stop:0.5 #0078c8, stop:0.9 #0050a0, stop:1 #003c78);
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
    border: 1px solid #0050a0;
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e8f4f8, stop:0.5 #0078c8, stop:1 #0050a0);
}

QSlider::groove:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #e8f4f8, stop:1 #64c8dc);
    width: 6px;
    border-radius: 3px;
}

QSlider::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #ffffff, stop:0.5 #0078c8, stop:1 #003c78);
    height: 18px;
    margin: 0 -6px;
    border-radius: 9px;
    border: 1px solid #0050a0;
}

/* Progress Bar */
QProgressBar {
    background-color: #e8f4f8;
    border: 1px solid #64c8dc;
    border-radius: 3px;
    padding: 1px;
    color: #003c78;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0078c8, stop:1 #0050a0);
    border-radius: 2px;
}

/* Combo Box */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 3px;
    padding: 2px;
    color: #003c78;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border: none;
}

QComboBox:focus {
    border: 2px solid #0078c8;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #0078c8;
    color: #003c78;
    selection-background-color: #0078c8;
    selection-color: white;
}

/* Scroll Bars */
QScrollBar:horizontal {
    background-color: #e8f4f8;
    height: 12px;
    border: 1px solid #64c8dc;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #b0d0e0, stop:0.5 #0078c8, stop:1 #003c78);
    border-radius: 5px;
    min-width: 20px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e8f4f8, stop:0.5 #0078c8, stop:1 #0050a0);
}

QScrollBar:vertical {
    background-color: #e8f4f8;
    width: 12px;
    border: 1px solid #64c8dc;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #b0d0e0, stop:0.5 #0078c8, stop:1 #003c78);
    border-radius: 5px;
    min-height: 20px;
    margin: 2px;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #64c8dc;
}

QTabBar::tab {
    background-color: #e8f4f8;
    border: 1px solid #64c8dc;
    border-bottom: none;
    padding: 4px 12px;
    margin-right: 2px;
    color: #003c78;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffffff, stop:1 #e8f4f8);
    border-color: #0078c8;
    color: #003c78;
    font-weight: bold;
}

/* Menu Bar */
QMenuBar {
    background-color: #f0f8ff;
    border-bottom: 1px solid #64c8dc;
    color: #003c78;
}

QMenuBar::item:selected {
    background-color: #0078c8;
    color: white;
}

/* Menu */
QMenu {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    color: #003c78;
    padding: 2px 0px;
}

QMenu::item:selected {
    background-color: #0078c8;
    color: white;
}

QMenu::separator {
    height: 1px;
    background-color: #64c8dc;
    margin: 4px 0px;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 3px;
    padding: 2px;
    color: #003c78;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #0078c8;
}

/* Check Box & Radio Button */
QCheckBox, QRadioButton {
    color: #003c78;
    spacing: 5px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 2px;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0078c8, stop:1 #003c78);
    border: 1px solid #0050a0;
    border-radius: 2px;
    image: url(:/icons/check.png);
}

QRadioButton::indicator:unchecked {
    background-color: #ffffff;
    border: 1px solid #64c8dc;
    border-radius: 9px;
}

QRadioButton::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #0078c8, stop:1 #003c78);
    border: 1px solid #0050a0;
    border-radius: 9px;
}

/* Tooltips */
QToolTip {
    background-color: #003c78;
    color: #ffffff;
    border: 1px solid #0078c8;
    border-radius: 3px;
    padding: 3px;
}
```

---

## 7. COMPLETE AUDIO APP EXAMPLE

```python
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QSlider, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class FrutigerAeroAudioApp(QMainWindow):
    """
    Audio Recording/Playback application with Frutiger Aero theme.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Frutiger Aero Audio Recorder")
        self.setGeometry(100, 100, 600, 400)

        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title
        title_label = QLabel("Audio Recording Studio")
        title_font = QFont("Frutiger, Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Waveform display
        from waveform import WaveformVisualization
        self.waveform = WaveformVisualization()
        main_layout.addWidget(self.waveform)

        # Playback controls layout
        control_layout = QHBoxLayout()

        # Buttons
        play_button = GlossyButton("Play")
        record_button = GlossyButton("Record")
        stop_button = GlossyButton("Stop")
        open_button = GlossyButton("Open")

        control_layout.addWidget(record_button)
        control_layout.addWidget(play_button)
        control_layout.addWidget(stop_button)
        control_layout.addWidget(open_button)

        main_layout.addLayout(control_layout)

        # Volume slider
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        volume_slider = GlossySlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(70)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)
        main_layout.addLayout(volume_layout)

        # Progress slider
        progress_layout = QHBoxLayout()
        progress_label = QLabel("Progress:")
        progress_slider = GlossySlider(Qt.Orientation.Horizontal)
        progress_slider.setRange(0, 100)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(progress_slider)
        main_layout.addLayout(progress_layout)

        self.setCentralWidget(central_widget)

        # Apply stylesheet
        self.setStyleSheet(STYLESHEET)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FrutigerAeroAudioApp()
    window.show()
    sys.exit(app.exec())
```

---

## Implementation Checklist

- [ ] Create `colors.py` with color constants
- [ ] Implement `GlossyButton` class
- [ ] Implement `GlassPanel` class
- [ ] Implement `GlossySlider` class
- [ ] Implement `WaveformVisualization` class
- [ ] Apply QSS stylesheet to main window
- [ ] Test button states (normal, hover, pressed)
- [ ] Test waveform with sample audio data
- [ ] Adjust gradient stops for desired appearance
- [ ] Add animations (fade in/out) for polish
- [ ] Create Dark Aero variant theme
- [ ] Test on different screen resolutions

---

## Performance Tips

1. **Cache Gradients**: Pre-create gradients if they don't change
2. **Reduce Repaints**: Update only affected regions
3. **Use QPixmapCache**: Cache rendered waveforms if drawing is expensive
4. **Profile**: Use Qt profiler to identify bottlenecks
5. **Antialiasing**: Balance quality vs. performance

---

## Troubleshooting

**Gradients look flat:**
- Increase color stops between transitions
- Use more distinct color values
- Ensure opacity values vary

**Performance lag with waveform:**
- Reduce waveform detail (downsampling)
- Use OpenGL rendering for complex visualizations
- Cache pre-rendered waveforms

**Colors not matching reference:**
- Verify hex codes are exactly correct
- Account for display calibration
- Test on different monitors

