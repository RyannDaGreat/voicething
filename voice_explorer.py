"""Voice Explorer: browse, preview, and select macOS TTS voices."""

import os
import subprocess
import tempfile
import threading
import rp


def _get_macos_voice_catalog():
    """
    Query, specific. Enumerates ALL macOS TTS voices (installed + downloadable).

    Parses the local AssetsV2 plist that macOS maintains for on-demand voice
    downloads. Cross-references with rp.get_macos_voices() to mark which are
    installed. No network access, no extra packages -- pure stdlib plistlib.

    Returns empty list if the catalog plist doesn't exist (older macOS versions
    or non-macOS platforms).

    Returns:
        list[dict]: Each dict has keys:
            name (str), languages (list[str]), footprint (str),
            download_size_mb (float), type (str), gender (str),
            installed (bool), voice_id (str), siri (bool)
    """
    import plistlib

    plist_path = (
        "/System/Library/AssetsV2/"
        "com_apple_MobileAsset_TTSAXResourceModelAssets/"
        "com_apple_MobileAsset_TTSAXResourceModelAssets.xml"
    )
    if not os.path.exists(plist_path):
        return []

    with open(plist_path, 'rb') as f:
        data = plistlib.load(f)

    installed_voices = set(rp.get_macos_voices())

    # Deduplicate by (name, footprint, first_language) -- the catalog has
    # multiple _ContentVersion entries per voice; keep the latest.
    seen = {}
    for asset in data.get('Assets', []):
        name = asset.get('Name', '')
        if not name:
            continue
        langs = asset.get('Languages', [])
        footprint = asset.get('Footprint', '')
        first_lang = langs[0] if langs else ''
        key = (name, footprint, first_lang)
        version = asset.get('_ContentVersion', 0)
        if key in seen and seen[key].get('_ContentVersion', 0) >= version:
            continue
        seen[key] = asset

    results = []
    for asset in seen.values():
        name = asset.get('Name', '')
        download_bytes = asset.get('_DownloadSize', 0)
        results.append({
            'name':             name,
            'languages':        asset.get('Languages', []),
            'footprint':        asset.get('Footprint', ''),
            'download_size_mb': round(download_bytes / (1024 * 1024), 1),
            'type':             asset.get('Type', ''),
            'gender':           asset.get('Gender', ''),
            'installed':        name in installed_voices,
            'voice_id':         asset.get('VoiceId', ''),
            'siri':             'premium' in asset.get('VoiceId', ''),
        })

    results.sort(key=lambda d: (d['name'].lower(), d['footprint']))
    return results

from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

# Import styling from voice_thing (same process, already initialized)
from voice_thing import (
    DraggableDialog,
    STYLE,
    PANEL_BG_FLAT_CSS,
    SCROLLBAR_CSS,
    BORDER_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    TOOLTIP_CSS,
    DIALOG_MARGIN,
    make_title,
    get_btn_css,
    get_lineedit_css,
    get_checkbox_css,
    set_tooltip,
)


# ── Constants ──────────────────────────────────────────────────────────────

# Column indices (Say mode — full catalog)
COL_NAME = 0
COL_SIRI = 1
COL_TIER = 2
COL_LANG = 3
COL_GENDER = 4
COL_SIZE = 5
COL_STATUS = 6
NUM_COLS_SAY = 7

# Column indices (Siri mode — name only)
NUM_COLS_SIRI = 1

# Preview debounce delay (ms) — prevents overwhelming TTS when arrowing fast
PREVIEW_DEBOUNCE_MS = 300

# Default test phrase
DEFAULT_PHRASE = "The quick brown fox jumps over the lazy dog."

# Tier display labels and filter order
TIER_LABELS = {
    'premium':  '★ Premium',
    'enhanced': '◆ Enhanced',
    'compact':  'Compact',
}


# ── VoiceExplorerDialog ───────────────────────────────────────────────────

class VoiceExplorerDialog(DraggableDialog):
    """
    Command, specific. Modal dialog for browsing and selecting TTS voices.

    Supports two backends:
    - 'say': Full macOS AssetsV2 catalog with tiers, filters, install status.
    - 'siri': Simple name-only list from rp.get_siri_voices().

    Both support live preview with debounce and keyboard nav.
    """
    window_name = "voice_explorer"

    def __init__(self, current_voice="", parent=None, backend='say'):
        self._backend = backend
        self._is_siri = (backend == 'siri')
        super().__init__(parent)
        self._current_voice = current_voice
        self.selected_voice = None   # Set on accept
        self._preview_proc = None    # Running preview subprocess (say or afplay)
        self._siri_synth_cancel = None  # threading.Event to cancel siri synthesis
        self._siri_temp_wav = None   # Temp WAV path for siri preview
        self._catalog = []           # Filtered view into _all_entries
        self._all_entries = []       # Full catalog
        self._build_ui()
        self._load_catalog()
        if self._is_siri:
            self.resize(360, 500)
        else:
            self.resize(720, 500)
        self.center_on_parent()

    # ── UI Construction ────────────────────────────────────────────────

    def _build_ui(self):
        """Command, specific. Builds all UI widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(DIALOG_MARGIN, DIALOG_MARGIN, DIALOG_MARGIN, DIALOG_MARGIN)
        layout.setSpacing(8)

        # Title row
        title_text = "Voice Explorer — Siri" if self._is_siri else "Voice Explorer"
        title_row = QHBoxLayout()
        title_row.addWidget(make_title(title_text), 1)
        layout.addLayout(title_row)

        # Test phrase input
        phrase_row = QHBoxLayout()
        phrase_row.setSpacing(6)
        phrase_label = QLabel("Phrase:")
        phrase_label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 12px;")
        phrase_row.addWidget(phrase_label)
        self._phrase_edit = QLineEdit(DEFAULT_PHRASE)
        self._phrase_edit.setStyleSheet(get_lineedit_css())
        set_tooltip(self._phrase_edit, "Test phrase for voice preview.\nSelect a voice or press Enter to hear it.")
        phrase_row.addWidget(self._phrase_edit, 1)
        layout.addLayout(phrase_row)

        # Filter row (Say only)
        self._filter_widgets = []
        if not self._is_siri:
            filter_row = QHBoxLayout()
            filter_row.setSpacing(8)
            self._tier_checks = {}
            for tier_key, tier_label in TIER_LABELS.items():
                cb = QCheckBox(tier_label)
                cb.setChecked(True)
                cb.setStyleSheet(get_checkbox_css())
                cb.stateChanged.connect(self._apply_filters)
                self._tier_checks[tier_key] = cb
                filter_row.addWidget(cb)
                self._filter_widgets.append(cb)

            filter_row.addStretch()

            self._siri_only = QCheckBox("Siri only")
            self._siri_only.setChecked(False)
            self._siri_only.setStyleSheet(get_checkbox_css())
            set_tooltip(self._siri_only, "Show only Siri neural voices (premium tier).")
            self._siri_only.stateChanged.connect(self._apply_filters)
            filter_row.addWidget(self._siri_only)
            self._filter_widgets.append(self._siri_only)

            self._show_not_installed = QCheckBox("Not installed")
            self._show_not_installed.setChecked(True)
            self._show_not_installed.setStyleSheet(get_checkbox_css())
            set_tooltip(self._show_not_installed, "Show voices that haven't been downloaded yet.\nThey can be installed via System Settings > Accessibility > Spoken Content.")
            self._show_not_installed.stateChanged.connect(self._apply_filters)
            filter_row.addWidget(self._show_not_installed)
            self._filter_widgets.append(self._show_not_installed)

            layout.addLayout(filter_row)

        # Table
        self._table = QTableWidget()
        if self._is_siri:
            self._table.setColumnCount(NUM_COLS_SIRI)
            self._table.setHorizontalHeaderLabels(["Name"])
        else:
            self._table.setColumnCount(NUM_COLS_SAY)
            self._table.setHorizontalHeaderLabels(["Name", "Siri", "Tier", "Language", "Gender", "Size", "Status"])
        self._table.setStyleSheet(
            f"QTableWidget {{ {PANEL_BG_FLAT_CSS} color: {TEXT_PRIMARY}; "
            f"border: 1px solid {BORDER_COLOR}; font-family: Menlo, monospace; font-size: 11px; }} "
            f"QTableWidget::item {{ padding: 1px 6px; color: {TEXT_PRIMARY}; }} "
            f"QTableWidget::item:hover {{ background: rgba({STYLE.accent.red()},{STYLE.accent.green()},{STYLE.accent.blue()},0.25); }} "
            f"QTableWidget::item:selected {{ background: rgba({STYLE.accent.red()},{STYLE.accent.green()},{STYLE.accent.blue()},0.5); color: {TEXT_PRIMARY}; }} "
            f"QHeaderView::section {{ background: {BORDER_COLOR}; color: {TEXT_PRIMARY}; padding: 2px 4px; "
            f"border: 1px solid {BORDER_COLOR}; font-weight: bold; }}"
            + SCROLLBAR_CSS
        )
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(22)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        self._table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._table, 1)

        # Footer buttons
        footer = QHBoxLayout()
        footer.setSpacing(8)

        btn_css = get_btn_css()

        # Download / install more voices button
        if self._is_siri:
            self._download_btn = QPushButton("Install More Voices…")
            set_tooltip(self._download_btn, "Open System Settings > Spoken Content\nto download additional Siri voices.")
        else:
            self._download_btn = QPushButton("Download Voices…")
            set_tooltip(self._download_btn, "Open System Settings to download additional voices.")
        self._download_btn.setStyleSheet(btn_css)
        self._download_btn.clicked.connect(self._open_voice_settings)
        footer.addWidget(self._download_btn)

        footer.addStretch()

        self._close_btn = QPushButton("Close")
        self._close_btn.setStyleSheet(btn_css)
        self._close_btn.clicked.connect(self.reject)
        footer.addWidget(self._close_btn)

        self._select_btn = QPushButton("Select")
        self._select_btn.setStyleSheet(btn_css)
        self._select_btn.clicked.connect(self._on_select)
        self._select_btn.setEnabled(False)
        footer.addWidget(self._select_btn)

        layout.addLayout(footer)

        # Preview debounce timer
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._do_preview)

    # ── Data Loading ───────────────────────────────────────────────────

    def _load_catalog(self):
        """Command, specific. Loads voice catalog and populates table."""
        if self._is_siri:
            self._all_entries = [
                {'name': name, 'installed': True}
                for name in rp.get_siri_voices()
            ]
            self._catalog = list(self._all_entries)
            self._populate_table()
        else:
            self._all_entries = _get_macos_voice_catalog()
            self._apply_filters()

        # Select current voice if present
        if self._current_voice:
            for row in range(self._table.rowCount()):
                item = self._table.item(row, COL_NAME)
                if item and item.data(Qt.ItemDataRole.UserRole) == self._current_voice:
                    self._table.selectRow(row)
                    self._table.scrollToItem(item)
                    break

    def _apply_filters(self):
        """Command, specific. Rebuilds table rows from _all_entries based on active filters."""
        active_tiers = {k for k, cb in self._tier_checks.items() if cb.isChecked()}
        show_not_installed = self._show_not_installed.isChecked()
        siri_only = self._siri_only.isChecked()

        self._catalog = []
        for entry in self._all_entries:
            if entry['footprint'] not in active_tiers:
                continue
            if not entry['installed'] and not show_not_installed:
                continue
            if siri_only and not entry['siri']:
                continue
            self._catalog.append(entry)

        self._populate_table()

    def _populate_table(self):
        """Command, specific. Fills QTableWidget from self._catalog."""
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(self._catalog))

        if self._is_siri:
            for row, entry in enumerate(self._catalog):
                name_item = QTableWidgetItem(entry['name'])
                name_item.setData(Qt.ItemDataRole.UserRole, entry['name'])
                self._table.setItem(row, COL_NAME, name_item)
        else:
            for row, entry in enumerate(self._catalog):
                name_item = QTableWidgetItem(entry['name'])
                name_item.setData(Qt.ItemDataRole.UserRole, entry['name'])
                self._table.setItem(row, COL_NAME, name_item)

                siri_text = "✓" if entry['siri'] else ""
                self._table.setItem(row, COL_SIRI, QTableWidgetItem(siri_text))

                tier_label = TIER_LABELS.get(entry['footprint'], entry['footprint'])
                self._table.setItem(row, COL_TIER, QTableWidgetItem(tier_label))

                lang_str = ', '.join(entry['languages'])
                self._table.setItem(row, COL_LANG, QTableWidgetItem(lang_str))

                gender = entry['gender'].capitalize() if entry['gender'] else ''
                self._table.setItem(row, COL_GENDER, QTableWidgetItem(gender))

                size_str = f"{entry['download_size_mb']:.0f} MB" if entry['download_size_mb'] >= 1 else f"{entry['download_size_mb']:.1f} MB"
                size_item = QTableWidgetItem(size_str)
                # Store numeric value for proper sorting
                size_item.setData(Qt.ItemDataRole.UserRole, entry['download_size_mb'])
                self._table.setItem(row, COL_SIZE, size_item)

                status = "Installed" if entry['installed'] else "Not Downloaded"
                status_item = QTableWidgetItem(status)
                self._table.setItem(row, COL_STATUS, status_item)

                # Dim not-installed rows
                if not entry['installed']:
                    for col in range(NUM_COLS_SAY):
                        item = self._table.item(row, col)
                        if item:
                            item.setForeground(STYLE.accent if col == COL_STATUS else _dim_color())

            # Column widths (Say mode)
            self._table.setColumnWidth(COL_NAME, 130)
            self._table.setColumnWidth(COL_SIRI, 40)
            self._table.setColumnWidth(COL_TIER, 95)
            self._table.setColumnWidth(COL_LANG, 65)
            self._table.setColumnWidth(COL_GENDER, 55)
            self._table.setColumnWidth(COL_SIZE, 60)
            # Status stretches via setStretchLastSection

        self._table.setSortingEnabled(True)

    # ── Selection & Preview ────────────────────────────────────────────

    def _on_selection_changed(self):
        """Command, specific. Handles table row selection — enables Select button, starts preview timer."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            self._select_btn.setEnabled(False)
            return

        row = rows[0].row()
        entry = self._entry_for_row(row)
        if not entry:
            self._select_btn.setEnabled(False)
            return

        self._select_btn.setEnabled(entry['installed'])

        # Debounced preview (only for installed voices)
        if entry['installed']:
            self._preview_timer.start(PREVIEW_DEBOUNCE_MS)

    def _entry_for_row(self, row):
        """Pure function, specific. Returns catalog entry for a table row, or None."""
        name_item = self._table.item(row, COL_NAME)
        if not name_item:
            return None
        name = name_item.data(Qt.ItemDataRole.UserRole)
        if self._is_siri:
            # Siri: match by name only (all entries are unique names)
            for entry in self._catalog:
                if entry['name'] == name:
                    return entry
            return None
        # Say: match by name + tier display label
        tier_item = self._table.item(row, COL_TIER)
        tier_text = tier_item.text() if tier_item else ''
        for entry in self._catalog:
            if entry['name'] == name and TIER_LABELS.get(entry['footprint'], entry['footprint']) == tier_text:
                return entry
        return None

    def _do_preview(self):
        """Command, specific. Speaks current selection using appropriate backend."""
        self._kill_preview()

        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        entry = self._entry_for_row(rows[0].row())
        if not entry or not entry['installed']:
            return

        phrase = self._phrase_edit.text().strip() or DEFAULT_PHRASE

        if self._is_siri:
            self._do_siri_preview(entry['name'], phrase)
        else:
            self._preview_proc = subprocess.Popen(
                ['say', '-v', entry['name'], phrase],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _do_siri_preview(self, voice_name, phrase):
        """Command, specific. Synthesizes via Siri XPC to temp WAV, then plays with afplay."""
        cancel_event = threading.Event()
        self._siri_synth_cancel = cancel_event
        temp_wav = tempfile.mktemp(suffix='.wav', prefix='siri_preview_')
        self._siri_temp_wav = temp_wav

        def _synth_and_play():
            rp.text_to_speech_via_siri(phrase, voice=voice_name, output_path=temp_wav)
            if cancel_event.is_set():
                _cleanup_temp(temp_wav)
                return
            self._preview_proc = subprocess.Popen(
                ['afplay', temp_wav],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        threading.Thread(target=_synth_and_play, daemon=True).start()

    def _kill_preview(self):
        """Command, specific. Kills any running preview subprocess and cancels pending Siri synthesis."""
        # Cancel pending Siri synthesis
        if self._siri_synth_cancel is not None:
            self._siri_synth_cancel.set()
            self._siri_synth_cancel = None
        # Kill afplay or say process
        if self._preview_proc and self._preview_proc.poll() is None:
            self._preview_proc.kill()
            self._preview_proc = None
        # Clean up temp WAV
        if self._siri_temp_wav is not None:
            _cleanup_temp(self._siri_temp_wav)
            self._siri_temp_wav = None

    # ── Actions ────────────────────────────────────────────────────────

    def _on_select(self):
        """Command, specific. Accepts dialog with the selected voice name."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        entry = self._entry_for_row(rows[0].row())
        if entry and entry['installed']:
            self.selected_voice = entry['name']
            self.accept()

    def _open_voice_settings(self):
        """Command, specific. Opens macOS System Settings > Spoken Content."""
        # Modern format (macOS Ventura+), falls back gracefully on older systems
        subprocess.Popen([
            'open', 'x-apple.systempreferences:com.apple.Accessibility-Settings.extension?SpokenContent',
        ])

    # ── Keyboard Navigation ───────────────────────────────────────────

    def keyPressEvent(self, event):
        """Command, specific. Enter accepts, Escape rejects."""
        key = event.key()
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            if self._select_btn.isEnabled():
                self._on_select()
            return
        if key == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)

    # ── Cleanup ────────────────────────────────────────────────────────

    def closeEvent(self, event):
        """Command, specific. Kills preview on close."""
        self._kill_preview()
        self._preview_timer.stop()
        super().closeEvent(event)

    def reject(self):
        """Command, specific. Kills preview on reject."""
        self._kill_preview()
        self._preview_timer.stop()
        super().reject()


# ── Helpers ────────────────────────────────────────────────────────────────

def _dim_color():
    """
    Pure function, specific. Returns a QColor for dimming not-installed rows.

    Uses TEXT_MUTED from the current theme.

    Examples:
        >>> # Returns a QColor
        >>> _dim_color()  # doctest: +SKIP
    """
    from PyQt6.QtGui import QColor
    return QColor(TEXT_MUTED)


def _cleanup_temp(path):
    """
    Command, specific. Silently removes a temp file if it exists.

    Args:
        path (str): File path to remove.

    Examples:
        >>> _cleanup_temp("/tmp/nonexistent_file.wav")  # no-op
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
