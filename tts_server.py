"""SuperTonic TTS server wrapper for VoiceThing.

This module wraps rp.libs.supertonic_tts_server for VoiceThing integration.
"""

from rp.libs.supertonic_tts_server import (
    ensure_server,
    run_server,
    set_defaults,
    get_defaults,
    VOICES,
    DEFAULT_PORT,
)

_port = None


def check_existing_server(port):
    """Check if a TTS server is already running on the given port."""
    import urllib.request
    import json
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=1) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "ok":
                return True
    except Exception:
        pass
    return False


def start_server(port=DEFAULT_PORT):
    """Start server, returns port."""
    global _port
    _port = ensure_server(port)
    return _port


def stop_server():
    """Stop server (kills tmux session)."""
    global _port
    import rp
    from rp.libs.supertonic_tts_server import TMUX_SESSION
    if TMUX_SESSION in rp.tmux_get_all_session_names():
        rp.tmux_kill_session(TMUX_SESSION)
    _port = None


def get_port():
    """Get current server port."""
    return _port


def is_running():
    """Check if server is running."""
    if _port is None:
        return False
    return check_existing_server(_port)


# CLI for standalone testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SuperTonic TTS Server")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, help=f"Port (default {DEFAULT_PORT})")
    args = parser.parse_args()

    run_server(args.port)
