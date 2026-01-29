"""SuperTonic TTS HTTP server for VoiceThing speak-back feature."""

import http.server
import json
import socketserver
import threading
import urllib.parse
from io import BytesIO

import numpy as np
import sounddevice as sd

_tts = None
_voice_style = None
_server = None
_server_thread = None
_port = None


def _ensure_tts():
    """Lazily initialize SuperTonic TTS engine."""
    global _tts, _voice_style
    if _tts is not None:
        return
    try:
        from supertonic import TTS
        print("Loading SuperTonic TTS model (~305MB on first run)...")
        _tts = TTS(auto_download=True)
        _voice_style = _tts.get_voice_style(voice_name="F1")  # Female voice default
        print(f"SuperTonic TTS loaded. Sample rate: {_tts.sample_rate}Hz")
        print(f"Available voices: {_tts.voice_style_names}")
    except ImportError as e:
        raise RuntimeError(
            "SuperTonic not installed. Run: pip install supertonic"
        ) from e


def speak(text, voice="F1", lang="en", speed=1.5):
    """Synthesize and play text via speakers.

    Args:
        text: Text to speak
        voice: Voice name (F1-F5 female, M1-M5 male)
        lang: Language code (en, ko, es, pt, fr)
        speed: Speech speed multiplier (0.5=slow, 1.0=normal, 2.0=fast)

    Returns:
        Duration in seconds
    """
    _ensure_tts()
    global _voice_style

    if voice != "F1":
        _voice_style = _tts.get_voice_style(voice_name=voice)

    wav, duration = _tts.synthesize(text, voice_style=_voice_style, lang=lang, speed=speed)

    # SuperTonic outputs (1, samples) - squeeze to 1D for sounddevice
    wav = np.squeeze(wav)
    sd.play(wav, samplerate=_tts.sample_rate)
    sd.wait()
    return float(duration[0]) if hasattr(duration, '__getitem__') else float(duration)


class TTSHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for TTS requests."""

    def log_message(self, format, *args):
        print(f"[TTS] {args[0]}")

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """Handle GET /speak?text=..."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/health":
            self._send_json({"status": "ok", "tts": "supertonic"})
            return

        if parsed.path != "/speak":
            self._send_json({"error": "Not found. Use GET /speak?text=..."}, 404)
            return

        params = urllib.parse.parse_qs(parsed.query)
        text = params.get("text", [""])[0]
        voice = params.get("voice", ["F1"])[0]
        lang = params.get("lang", ["en"])[0]
        speed = float(params.get("speed", ["1.5"])[0])

        if not text:
            self._send_json({"error": "Missing 'text' parameter"}, 400)
            return

        try:
            duration = speak(text, voice=voice, lang=lang, speed=speed)
            self._send_json({"ok": True, "duration": duration, "text": text, "speed": speed})
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_POST(self):
        """Handle POST /speak with JSON body."""
        if self.path != "/speak":
            self._send_json({"error": "Not found. Use POST /speak"}, 404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            # Treat as plain text
            data = {"text": body}

        text = data.get("text", "")
        voice = data.get("voice", "F1")
        lang = data.get("lang", "en")
        speed = float(data.get("speed", 1.5))

        if not text:
            self._send_json({"error": "Missing 'text' in body"}, 400)
            return

        try:
            duration = speak(text, voice=voice, lang=lang, speed=speed)
            self._send_json({"ok": True, "duration": duration, "text": text, "speed": speed})
        except Exception as e:
            self._send_json({"error": str(e)}, 500)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def start_server(port=7123):
    """Start the TTS HTTP server in a background thread.

    Args:
        port: Port to listen on (default 7123)

    Returns:
        Actual port the server is running on
    """
    global _server, _server_thread, _port

    if _server is not None:
        return _port

    # Pre-load TTS model so first request is fast
    _ensure_tts()

    _server = ThreadedTCPServer(("127.0.0.1", port), TTSHandler)
    _port = _server.server_address[1]

    _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _server_thread.start()

    print(f"TTS server running on http://localhost:{_port}")
    return _port


def stop_server():
    """Stop the TTS server if running."""
    global _server, _server_thread, _port
    if _server is not None:
        _server.shutdown()
        _server = None
        _server_thread = None
        _port = None
        print("TTS server stopped.")


def get_port():
    """Return current server port, or None if not running."""
    return _port


def is_running():
    """Return True if server is running."""
    return _server is not None


def check_existing_server(port):
    """Check if a TTS server is already running on the given port.

    Returns:
        True if server responds to /health, False otherwise
    """
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=1) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "ok":
                print(f"Found existing TTS server on port {port}")
                return True
    except Exception:
        pass
    return False


def ensure_server(port=7123):
    """Ensure a TTS server is running - reuse existing or start new.

    Args:
        port: Port to use (default 7123)

    Returns:
        Port number of running server
    """
    global _port

    # Check if we already started one
    if _server is not None:
        return _port

    # Check if external server exists on this port
    if check_existing_server(port):
        _port = port
        return port

    # Start our own
    return start_server(port)


def get_curl_instruction(port=None):
    """Return the curl instruction string for Claude to use."""
    p = port or _port or 7123
    return f'curl "http://localhost:{p}/speak?text=YOUR_MESSAGE_HERE"'


# CLI for standalone testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SuperTonic TTS Server")
    parser.add_argument("--port", "-p", type=int, default=7123, help="Port (default 7123)")
    parser.add_argument("--test", "-t", type=str, help="Test speak text and exit")
    args = parser.parse_args()

    if args.test:
        print(f"Speaking: {args.test}")
        speak(args.test)
    else:
        port = start_server(args.port)
        print(f"\nUsage:")
        print(f'  curl "http://localhost:{port}/speak?text=Hello%20world"')
        print(f'  curl -X POST http://localhost:{port}/speak -d \'{{"text": "Hello world"}}\' ')
        print(f"\nPress Ctrl+C to stop...")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            stop_server()
