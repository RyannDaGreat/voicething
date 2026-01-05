# PyQt6 Retro Aesthetic Implementation Guide

## Quick Start

### 1. Apply the QSS Stylesheet

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QFile, QTextStream

# Load the stylesheet
def load_stylesheet(app, stylesheet_path):
    style_file = QFile(stylesheet_path)
    style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    style = QTextStream(style_file).readAll()
    style_file.close()
    app.setStyleSheet(style)

# In your main window setup:
app = QApplication(sys.argv)
load_stylesheet(app, "retro_aesthetic.qss")
window = YourMainWindow()
window.show()
app.exec()
```

### 2. Apply Stylesheet at Runtime (Dynamic Loading)

```python
import os

def apply_retro_theme(widget):
    """Apply the retro aesthetic QSS to any QWidget or QApplication"""
    stylesheet_path = os.path.join(
        os.path.dirname(__file__),
        "retro_aesthetic.qss"
    )

    with open(stylesheet_path, "r") as f:
        stylesheet = f.read()

    widget.setStyleSheet(stylesheet)

# Usage
apply_retro_theme(app)  # For entire application
# or
apply_retro_theme(main_window)  # For specific window
```

---

## Creating Visualization Widgets

### Spectrum Analyzer Widget

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QTimer
import numpy as np

class SpectrumAnalyzer(QWidget):
    """
    Real-time spectrum analyzer with vaporwave gradient colors.

    Colors: Cyan (#01CDFE) to Purple (#B967FF) gradient
    """

    def __init__(self, parent=None, num_bands=64):
        super().__init__(parent)
        self.num_bands = num_bands
        self.levels = np.zeros(num_bands)
        self.setMinimumHeight(120)
        self.setObjectName("spectrumPanel")

        # Color gradient: Cyan → Purple
        self.color_cyan = QColor(0x01, 0xCD, 0xFE)    # #01CDFE
        self.color_purple = QColor(0xB9, 0x67, 0xFF)  # #B967FF

        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(33)  # ~30 FPS

    def set_spectrum_data(self, frequencies):
        """
        Update spectrum data.

        Args:
            frequencies: array of float values 0.0-1.0 for each frequency band
        """
        if len(frequencies) == self.num_bands:
            # Smooth decay (falloff)
            decay_factor = 0.85
            self.levels = self.levels * decay_factor
            # Update with new data
            self.levels = np.maximum(self.levels, np.array(frequencies))
        self.update()

    def animate(self):
        """Gradual falloff animation"""
        self.levels *= 0.95  # Smooth decay
        self.update()

    def paintEvent(self, event):
        """Draw spectrum analyzer bars with gradient coloring"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0x12, 0x12, 0x12))  # #121212

        width = self.width()
        height = self.height()
        bar_width = max(1, width // (self.num_bands + 1))
        gap = max(1, width // (self.num_bands * 2))

        for i, level in enumerate(self.levels):
            # Interpolate color between cyan and purple based on frequency
            t = i / max(1, self.num_bands - 1)

            # Linear interpolation: cyan to purple
            r = int(self.color_cyan.red() + t * (self.color_purple.red() - self.color_cyan.red()))
            g = int(self.color_cyan.green() + t * (self.color_purple.green() - self.color_cyan.green()))
            b = int(self.color_cyan.blue() + t * (self.color_purple.blue() - self.color_cyan.blue()))

            color = QColor(r, g, b)

            # Draw bar
            x = i * (bar_width + gap)
            bar_height = int(height * level)
            y = height - bar_height

            painter.fillRect(x, y, bar_width, bar_height, color)

            # Optional: add glow/bright top edge
            if bar_height > 2:
                painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
                painter.drawLine(x, y, x + bar_width, y)

        painter.end()
```

### Waveform Display Widget

```python
class WaveformDisplay(QWidget):
    """
    Real-time waveform display in Winamp lime green (#00FF00).

    Displays raw audio samples as a connected line.
    """

    def __init__(self, parent=None, sample_count=1024):
        super().__init__(parent)
        self.sample_count = sample_count
        self.samples = np.zeros(sample_count)
        self.setMinimumHeight(80)
        self.setObjectName("waveformPanel")

        # Winamp classic lime green
        self.waveform_color = QColor(0x00, 0xFF, 0x00)  # #00FF00
        self.bg_color = QColor(0x1a, 0x1a, 0x1a)        # #1a1a1a

    def set_waveform_data(self, samples):
        """
        Update waveform with new audio samples.

        Args:
            samples: array of float values -1.0 to 1.0
        """
        if len(samples) <= self.sample_count:
            # Shift old samples and add new ones
            shift = len(samples)
            self.samples[:-shift] = self.samples[shift:]
            self.samples[-shift:] = samples
        else:
            # Downsample if too many samples
            indices = np.linspace(0, len(samples) - 1, self.sample_count, dtype=int)
            self.samples = samples[indices]
        self.update()

    def paintEvent(self, event):
        """Draw waveform as connected line"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color)

        width = self.width()
        height = self.height()
        center_y = height / 2

        # Draw center line
        painter.setPen(QPen(QColor(0x33, 0x33, 0x33), 1))  # #333333
        painter.drawLine(0, int(center_y), width, int(center_y))

        # Draw waveform
        painter.setPen(QPen(self.waveform_color, 2))

        if len(self.samples) > 1:
            path = []
            for i, sample in enumerate(self.samples):
                x = i * width / len(self.samples)
                # Sample range: -1.0 to 1.0 maps to full height
                y = center_y - (sample * center_y * 0.9)
                path.append((int(x), int(y)))

            # Draw connected line
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                painter.drawLine(x1, y1, x2, y2)

        painter.end()
```

### Level Meter Widget

```python
class LevelMeter(QWidget):
    """
    Dual-channel level meter (L/R) with cyan gradient bars.
    Shows current level and peak indicator.
    """

    def __init__(self, parent=None, channels=2):
        super().__init__(parent)
        self.channels = channels
        self.levels = np.zeros(channels)
        self.peaks = np.zeros(channels)
        self.peak_decay = 0.95

        self.setMinimumHeight(40 * channels)
        self.setObjectName("levelPanel")

        # Colors: mint green to warn/peak colors
        self.level_color = QColor(0x01, 0xCD, 0xFE)    # #01CDFE cyan
        self.peak_color = QColor(0xFF, 0x71, 0xCE)     # #FF71CE hot pink
        self.bg_color = QColor(0x1a, 0x1a, 0x1a)       # #1a1a1a

        # Animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(33)  # ~30 FPS

    def set_level(self, channel, level):
        """
        Set level for a channel (0.0 to 1.0).

        Args:
            channel: channel index (0=L, 1=R)
            level: float 0.0-1.0
        """
        if 0 <= channel < self.channels:
            self.levels[channel] = min(1.0, max(0.0, level))
            # Update peaks
            if self.levels[channel] > self.peaks[channel]:
                self.peaks[channel] = self.levels[channel]
        self.update()

    def animate(self):
        """Decay peaks"""
        self.peaks *= self.peak_decay
        self.update()

    def paintEvent(self, event):
        """Draw level meters"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color)

        width = self.width()
        height = self.height()
        meter_height = height / self.channels
        margin = 4

        for ch in range(self.channels):
            y = ch * meter_height + margin
            h = meter_height - 2 * margin

            # Background bar
            painter.fillRect(margin, y, width - 2*margin, h, QColor(0x00, 0x00, 0x00))

            # Level bar
            bar_width = (width - 2*margin) * self.levels[ch]
            painter.fillRect(margin, y, bar_width, h, self.level_color)

            # Peak indicator
            peak_x = margin + (width - 2*margin) * self.peaks[ch]
            painter.setPen(QPen(self.peak_color, 2))
            painter.drawLine(int(peak_x), int(y), int(peak_x), int(y + h))

            # Channel label
            label = "L" if ch == 0 else "R"
            painter.setPen(QPen(QColor(0xFF, 0xFF, 0xFF)))
            painter.drawText(4, int(y + h/2 + 4), label)

        painter.end()
```

---

## Applying Custom Properties to Widgets

### Setting Widget Properties for Stylesheet Selectors

```python
from PyQt6.QtWidgets import QPushButton, QFrame, QLabel

# Accent button (gold)
record_button = QPushButton("Record")
record_button.setProperty("accent", "true")

# Recording indicator (red)
# Update in real-time
record_button.setProperty("recording", "true" if is_recording else "false")

# Vaporwave button (pink/purple)
settings_button = QPushButton("Settings")
settings_button.setProperty("vaporwave", "true")

# Dark panel
spectrum_panel = QFrame()
spectrum_panel.setProperty("spectrumPanel", "true")

# Waveform panel
waveform_panel = QFrame()
waveform_panel.setProperty("waveformPanel", "true")

# Level meter panel
level_panel = QFrame()
level_panel.setProperty("levelPanel", "true")

# Dark text (green on black)
tech_label = QLabel("24-bit, 48kHz, Stereo")
tech_label.setProperty("darkLabel", "true")
tech_label.setObjectName("techLabel")

# Title/header text (gold on dark)
title_label = QLabel("Audio Recording")
title_label.setObjectName("headerText")

# Monospace tech text
time_label = QLabel("00:23:45")
time_label.setObjectName("monoText")
```

### Dynamic Property Update (Style Refresh)

```python
def update_record_state(button, is_recording):
    """Update button appearance based on recording state"""
    button.setProperty("recording", "true" if is_recording else "false")
    # Force stylesheet update
    button.style().unpolish(button)
    button.style().polish(button)
    button.update()
```

---

## Color Constants (Python)

```python
class RetroColors:
    """Color constants for the retro aesthetic"""

    # Winamp colors
    WINAMP_GREEN = "#00FF00"      # Waveform green
    WINAMP_DARK = "#1a1a1a"       # Dark panels
    WINAMP_MED_DARK = "#333333"   # Medium-dark panels

    # Windows 95 colors
    WIN95_BUTTON = "#C0C0C0"       # Main button/background gray
    WIN95_HIGHLIGHT = "#FFFFFF"    # Highlight/bright edge
    WIN95_SHADOW = "#808080"       # Shadow edge
    WIN95_DARK_SHADOW = "#000000"  # Deep shadow

    # Vaporwave colors
    VAPOR_PINK = "#FF71CE"         # Hot pink
    VAPOR_CYAN = "#01CDFE"         # Cyan
    VAPOR_MINT = "#05FFA1"         # Mint green
    VAPOR_PURPLE = "#B967FF"       # Purple
    VAPOR_YELLOW = "#FFFB96"       # Pale yellow
    VAPOR_DARK_PURPLE = "#94167F"  # Dark purple

    # Y2K colors
    Y2K_GOLD = "#FFD700"           # Gold accent
    Y2K_BRIGHT_SILVER = "#E8E8E8"  # Bright silver
    Y2K_CHROME = "#C0C0C0"         # Chrome/metallic base
```

---

## Example: Complete Main Window Layout

```python
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt

class AudioRecorderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retro Audio Recorder")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(6)
        layout.setContentsMargins(6, 6, 6, 6)

        # Title
        title = QLabel("AUDIO RECORDING")
        title.setObjectName("headerText")
        layout.addWidget(title)

        # Spectrum analyzer
        self.spectrum = SpectrumAnalyzer()
        layout.addWidget(self.spectrum, 2)

        # Waveform
        self.waveform = WaveformDisplay()
        layout.addWidget(self.waveform, 1)

        # Level meters
        self.levels = LevelMeter(channels=2)
        layout.addWidget(self.levels)

        # Control buttons
        button_layout = QHBoxLayout()

        self.record_btn = QPushButton("● RECORD")
        self.record_btn.setProperty("accent", "true")
        self.record_btn.clicked.connect(self.toggle_recording)
        button_layout.addWidget(self.record_btn)

        self.play_btn = QPushButton("▶ PLAY")
        self.play_btn.setProperty("accent", "true")
        button_layout.addWidget(self.play_btn)

        self.stop_btn = QPushButton("⏹ STOP")
        button_layout.addWidget(self.stop_btn)

        layout.addLayout(button_layout)

        # Info panel
        info_frame = QFrame()
        info_frame.setProperty("darkPanel", "true")
        info_layout = QVBoxLayout(info_frame)

        self.file_label = QLabel("File: new_recording.wav")
        self.file_label.setObjectName("monoTextDark")
        info_layout.addWidget(self.file_label)

        self.format_label = QLabel("Format: WAV 48kHz 24-bit Stereo")
        self.format_label.setObjectName("monoTextDark")
        info_layout.addWidget(self.format_label)

        layout.addWidget(info_frame)

        # Apply theme
        apply_retro_theme(self)

        self.is_recording = False

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        update_record_state(self.record_btn, self.is_recording)

        if self.is_recording:
            self.record_btn.setText("● STOP REC")
        else:
            self.record_btn.setText("● RECORD")

# Usage
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AudioRecorderWindow()
    window.show()
    sys.exit(app.exec())
```

---

## Integration with your voice_thing.py

1. **Add to imports:**
   ```python
   from retro_aesthetic import apply_retro_theme, RetroColors, SpectrumAnalyzer, WaveformDisplay, LevelMeter
   ```

2. **Apply theme in your main window setup:**
   ```python
   class VoiceThingWindow(QMainWindow):
       def __init__(self):
           super().__init__()
           # ... your existing setup ...
           apply_retro_theme(self)  # Apply retro theme
   ```

3. **Use color constants:**
   ```python
   spectrum_widget.setStyleSheet(f"background-color: {RetroColors.WINAMP_DARK}")
   ```

4. **Integrate visualization widgets:**
   ```python
   self.spectrum = SpectrumAnalyzer(num_bands=64)
   self.waveform = WaveformDisplay(sample_count=1024)
   self.levels = LevelMeter(channels=2)
   # Connect to audio input...
   ```

---

## Testing & Refinement

### Enable QSS Debugging

```python
# Add this before creating the window to see stylesheet errors
import logging
logging.basicConfig(level=logging.DEBUG)

# Check stylesheet has been loaded
print(app.styleSheet()[:100])
```

### Test Color Contrast

```python
# Ensure text is readable
# Dark backgrounds (#1a1a1a, #121212): Use #FFFFFF, #FFD700, or #00FF00
# Light backgrounds (#C0C0C0): Use #000000 or #800000

# Example verification
dark_bg = "#1a1a1a"  # RGB: 26, 26, 26
good_text_colors = ["#FFFFFF", "#FFD700", "#00FF00"]  # All have high contrast

light_bg = "#C0C0C0"  # RGB: 192, 192, 192
good_text_colors = ["#000000", "#800000"]  # Dark colors for readability
```

### Performance Tips

- Update visualizations at 30-60 FPS (not higher)
- Use numpy for fast array operations
- Cache QColor objects instead of creating new ones
- Use `update()` instead of `repaint()` for performance

---

## Next Steps

1. Copy `retro_aesthetic.qss` to your project directory
2. Implement visualization widgets from this guide
3. Integrate with your audio engine
4. Test on your target platform (macOS)
5. Fine-tune colors and layout as needed
6. Collect user feedback on readability and appeal

The aesthetic is now complete and ready for implementation!
