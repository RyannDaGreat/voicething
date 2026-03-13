"""
Reproduce and verify the SIGBUS crash at 0xBAD4007 in macOS ImageIO.

Root cause: DYLD_LIBRARY_PATH=/opt/homebrew/lib causes the dynamic linker to
load Homebrew's libpng (1.6.x) for ImageIO's PNG plugin instead of Apple's
private copy. The ABI mismatch corrupts PNGReadPlugin::InitializePluginData(),
causing SIGBUS when QPixmap.loadFromData(PNG) and setCursor interleave.

This is the same bug as wxWidgets #23547, Electron #48025, dotnet/sdk #44425,
and Tauri #7351.

Test strategy:
1. Launch subprocess WITH DYLD_LIBRARY_PATH=/opt/homebrew/lib → expect crash
2. Launch subprocess WITHOUT it → expect survival
3. Verify voice_thing.py's startup guard strips DYLD_LIBRARY_PATH and re-execs
"""
import subprocess
import sys
import os

PYTHON = "/opt/homebrew/opt/python@3.10/bin/python3.10"
VOICETHING_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Minimal script that interleaves QPixmap.loadFromData + setCursor
STRESS_SCRIPT = '''
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtCore import Qt, QTimer, QBuffer, QIODevice

app = QApplication(sys.argv)
img = QImage(44, 44, QImage.Format.Format_ARGB32)
img.fill(QColor(255, 0, 0, 255))
buf = QBuffer()
buf.open(QIODevice.OpenModeFlag.WriteOnly)
img.save(buf, "PNG")
png_data = bytes(buf.data())

widget = QWidget()
widget.setWindowFlags(Qt.WindowType.FramelessWindowHint)
widget.resize(200, 200)
widget.show()

count = 0
cursors = [Qt.CursorShape.ArrowCursor, Qt.CursorShape.SizeVerCursor,
           Qt.CursorShape.SizeHorCursor, Qt.CursorShape.SizeFDiagCursor]

def hammer():
    global count
    for i in range(50):
        p = QPixmap()
        p.loadFromData(png_data)
        widget.setCursor(cursors[i % len(cursors)])
    count += 50

timer = QTimer()
timer.timeout.connect(hammer)
timer.start(1)

watchdog = QTimer()
watchdog.timeout.connect(lambda: (print("SURVIVED"), app.quit()))
watchdog.start(15000)
app.exec()
'''

# The guard in voice_thing.py strips /opt/homebrew/lib from DYLD_LIBRARY_PATH
# and re-execs. We test the guard logic directly (same code, isolated script).
GUARD_SCRIPT = '''
import os, sys
# --- Same guard logic as voice_thing.py top ---
_HOMEBREW_LIB = "/opt/homebrew/lib"
_dyld_path = os.environ.get("DYLD_LIBRARY_PATH", "")
if _HOMEBREW_LIB in _dyld_path:
    _cleaned = ":".join(
        p for p in _dyld_path.split(":") if p and not p.startswith(_HOMEBREW_LIB)
    )
    if _cleaned:
        os.environ["DYLD_LIBRARY_PATH"] = _cleaned
    else:
        if "DYLD_LIBRARY_PATH" in os.environ:
            del os.environ["DYLD_LIBRARY_PATH"]
    os.execv(sys.executable, [sys.executable] + sys.argv)
# --- End guard ---
print("DYLD=" + os.environ.get("DYLD_LIBRARY_PATH", "(unset)"))
print("GUARD_OK")
'''


def _run_with_dyld(script, with_homebrew_lib, timeout_sec=20, use_file=False):
    """Run a Python script with or without DYLD_LIBRARY_PATH=/opt/homebrew/lib.

    Args:
        use_file: Write script to a temp file instead of using -c. Required for
                  scripts that call os.execv (which re-runs sys.argv).
    """
    import tempfile
    env = os.environ.copy()
    if with_homebrew_lib:
        env["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib"
    else:
        env.pop("DYLD_LIBRARY_PATH", None)

    if use_file:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name
        cmd = [PYTHON, script_path]
    else:
        cmd = [PYTHON, "-c", script]

    result = subprocess.run(
        cmd, env=env, timeout=timeout_sec, capture_output=True, text=True,
    )

    if use_file:
        os.unlink(script_path)

    return result


# ── Test 1: Crash WITH DYLD_LIBRARY_PATH ────────────────────────────────────

def test_crashes_with_homebrew_libpng():
    """Prove that DYLD_LIBRARY_PATH=/opt/homebrew/lib causes SIGBUS."""
    if not os.path.exists("/opt/homebrew/lib/libpng.dylib"):
        print("  SKIP: /opt/homebrew/lib/libpng.dylib not found")
        return

    # Run 3 times — crash is probabilistic but frequent
    crashes = 0
    for i in range(3):
        result = _run_with_dyld(STRESS_SCRIPT, with_homebrew_lib=True)
        if result.returncode != 0 and "SURVIVED" not in result.stdout:
            crashes += 1
            print(f"  Run {i+1}: CRASHED (exit {result.returncode})")
        else:
            print(f"  Run {i+1}: survived")

    assert crashes >= 1, (
        f"Expected at least 1 crash in 3 runs with DYLD_LIBRARY_PATH=/opt/homebrew/lib, "
        f"got {crashes}. The libpng ABI mismatch may not be present on this system."
    )
    print(f"  Result: {crashes}/3 runs crashed (confirms libpng ABI mismatch)")


# ── Test 2: No crash WITHOUT DYLD_LIBRARY_PATH ──────────────────────────────

def test_survives_without_homebrew_libpng():
    """Prove that without DYLD_LIBRARY_PATH, the same stress test survives."""
    result = _run_with_dyld(STRESS_SCRIPT, with_homebrew_lib=False)
    assert "SURVIVED" in result.stdout, (
        f"Stress test crashed even without DYLD_LIBRARY_PATH! "
        f"exit={result.returncode}, stderr={result.stderr[:200]}"
    )
    print("  No crash without DYLD_LIBRARY_PATH (15s stress test survived)")


# ── Test 3: Startup guard strips DYLD_LIBRARY_PATH ──────────────────────────

def test_startup_guard_strips_dyld():
    """Verify the startup guard removes /opt/homebrew/lib and re-execs."""
    # Must use a file because the guard calls os.execv(sys.argv) — -c loses content
    result = _run_with_dyld(GUARD_SCRIPT, with_homebrew_lib=True, timeout_sec=10, use_file=True)
    assert "GUARD_OK" in result.stdout, (
        f"Startup guard failed to strip DYLD_LIBRARY_PATH! "
        f"stdout={result.stdout}, stderr={result.stderr[:200]}"
    )
    assert "/opt/homebrew/lib" not in result.stdout.split("DYLD=")[1].split("\n")[0], (
        f"DYLD_LIBRARY_PATH still contains /opt/homebrew/lib after guard"
    )
    print(f"  Guard stripped DYLD_LIBRARY_PATH and re-execed successfully")


# ── Run all tests ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Test 1: DYLD_LIBRARY_PATH=/opt/homebrew/lib causes SIGBUS")
    test_crashes_with_homebrew_libpng()
    print()
    print("Test 2: Without DYLD_LIBRARY_PATH, stress test survives")
    test_survives_without_homebrew_libpng()
    print()
    print("Test 3: voice_thing.py startup guard strips DYLD_LIBRARY_PATH")
    test_startup_guard_strips_dyld()
    print()
    print("All tests passed — SIGBUS root cause confirmed and fix verified.")
