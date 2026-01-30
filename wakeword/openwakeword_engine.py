"""OpenWakeWord engine - ML-based wake word detection with pre-trained models."""

import collections
import os
import time
from typing import Optional

import numpy as np
import rp

from .base import WakeWordEngine, WakeWordCallback, StopCallback

# Audio constants
SAMPLE_RATE = 16000
FRAME_SAMPLES = 1280  # 80ms chunks for OpenWakeWord (16kHz * 0.08)
BUFFER_SECONDS = 2  # Seconds of audio to capture before wake word
COOLDOWN_SECONDS = 2.0  # Seconds to ignore wake word after triggering

# Cache directory for downloaded models
_VOICETHING_DIR = os.path.dirname(os.path.dirname(__file__))
CACHE_DIR = os.path.join(_VOICETHING_DIR, ".wake_word_cache")

# Built-in openWakeWord models (no download needed)
BUILTIN_MODELS = ["alexa", "hey_mycroft", "hey_jarvis", "hey_rhasspy"]

# Community wake word models from home-assistant-wakewords-collection
_COMMUNITY_BASE = "https://raw.githubusercontent.com/RyannDaGreat/home-assistant-wakewords-collection/main/en"
COMMUNITY_MODELS = {
    # A
    "ae_ttuddae": "ae-ttuddae/ae-ttuddae.onnx",
    "alfred": "alfred/alfred.onnx",
    "alice": "Alice/Alice.onnx",
    "andromeda": "andromeda/andromeda.onnx",
    # B
    "barclay": "barclay/Barclay.onnx",
    "bartolo": "bartolo/Bartolo.onnx",
    # C
    "choo_choo_homie": "choo_choo_homie/choo_choo_homie.onnx",
    "computer": "computer/computer_v2.onnx",
    # D
    "darth_vader": "darth_vader/Darth_Vader.onnx",
    "do_you_read_me_hal": "do_you_read_me__hal/do_you_read_me__hal.onnx",
    "dumbledore": "Dumbledore/Dumbledore.onnx",
    # E
    "edna": "edna/edna.onnx",
    "em_oi": "em__oi/em__oi.onnx",
    # G
    "glados": "glados/glados.onnx",
    # H
    "hal": "hal/hal_v2.onnx",
    "hey_hal": "hey__hal/hey__hal.onnx",
    "hey_alba": "hey_alba/hey_alba.onnx",
    "hey_anna": "hey_anna/hey_anna.onnx",
    "hey_barabas": "hey_barabas/hey_barabas.onnx",
    "hey_billy": "hey_billy/hey_billy.onnx",
    "hey_chatterbox": "hey_chatterbox/hey_chatterbox.onnx",
    "hey_chewbacca": "hey_chewbacca/Hey_Chewbacca.onnx",
    "hey_cj": "hey_cj/Hey_CJ.onnx",
    "hey_dick_head": "hey_dick_head/hey_dick_head.onnx",
    "hey_esp": "hey_esp/hey_esp.onnx",
    "hey_frenck": "hey_frenck/hey_frenck.onnx",
    "hey_friday": "hey_friday/hey_Friday!.onnx",
    "hey_gerty": "hey_GERTY/hey_GERTY.onnx",
    "hey_guillermo": "hey_guillermo/hey_guillermo.onnx",
    "hey_home_free": "hey_home_free/hey_home_free.onnx",
    "hey_homer": "hey_homer/Hey_Homer.onnx",
    "hey_honey": "hey_honey/Hey_Honey.onnx",
    "hey_house": "hey_house/hey_house.onnx",
    "hey_kitt": "hey_kitt/hey_kitt.onnx",
    "hey_konstantin": "hey_konstantin/hey_konstantin.onnx",
    "hey_kratos": "hey_kratos/Hey_Kreitos.onnx",
    "hey_lara": "Hey Lara/lara.onnx",
    "hey_lisa": "hey_lisa/hey_lisa.onnx",
    "hey_luna": "Hey Luna/hey_luna.onnx",
    "hey_marvin": "hey_Marvin/hey_Marvin.onnx",
    "hey_mcqueen": "hey_mcqueen/Hey_McQueen.onnx",
    "hey_megan": "hey_megan/hey_megan.onnx",
    "hey_miriel": "hey_miriel/hey_miriel.onnx",
    "hey_nabu": "hey_nabu/hey_nabu_v2.onnx",
    "hey_ozzy": "hey_ozzy/hey_ozzy.onnx",
    "hey_potato": "hey_potato/hey_potato.onnx",
    "hey_rick": "hey_rick/hey_rick.onnx",
    "hey_santa": "hey_santa/hey_santa.onnx",
    "hey_skelly": "hey_skelly/Hey_Skelly.onnx",
    "hey_snips": "hey_snips/hey_snips.onnx",
    "hey_spock": "hey_spock/hey_spock.onnx",
    "hey_wire_tap": "hey_wire_tap/hey_wire_tap.onnx",
    "hey_zelda": "hey_zelda/hey_zelda.onnx",
    "hi_xiaowen": "hi_xiaowen/hi_xiaowen_v2.onnx",
    "hola_casita": "hola_casita/Hola_casita.onnx",
    "home_assistant": "home_assistant/Home_assistant.onnx",
    # J
    "janet": "janet/Janet.onnx",
    "jarvis": "jarvis/jarvis_v2.onnx",
    "johnny_five": "johnny_five/johnny_five.onnx",
    "jupiter": "jupiter/jupiter-50-50-700.onnx",
    # K
    "kelsey": "kelsey/kelsey.onnx",
    # L
    "lisa": "lisa/Lisa.onnx",
    # M
    "marvin": "marvin/marvin_v2.onnx",
    "mirror_mirror_on_the_wall": "mirror_mirror_on_the_wall/mirror_mirror_on_the_wall.onnx",
    "mr_anderson": "mr_anderson/Mr._Anderson.onnx",
    "mr_smith": "mr_smith/mr_smith.onnx",
    "mr_wick": "mr_wick/Mr._Wick.onnx",
    # N
    "nihao_mia": "nihao_mia/nihao_mia_v2.onnx",
    "nihao_wenwen": "nihao_wenwen/nihao_wenwen.onnx",
    # O
    "oi_fuckwhit": "oi_fuckwhit/oi_fuckwhit_v2.onnx",
    "ok_bender": "ok_bender/ok_bender.onnx",
    "ok_boss": "ok_boss/ok_boss.onnx",
    "ok_casita": "ok_casita/ok_casita.onnx",
    "ok_computer": "ok_computer/ok_computer.onnx",
    "ok_home": "ok_home/ok_home.onnx",
    "ok_jarvis": "ok_jarvis/ok_jarvis.onnx",
    "ok_nabu": "ok_nabu/ok_nabu.onnx",
    "ok_neo": "ok_neo/ok_neo.onnx",
    "ok_paulus": "ok_paulus/ok_paulus.onnx",
    "ok_tau": "ok_tau/ok_tau.onnx",
    "ok_trevor": "ok_trevor/ok_trevor.onnx",
    "ok_wire_tap": "ok_wire_tap/ok_wire_tap.onnx",
    # P
    "pandora": "pandora/Pandora.onnx",
    "polly": "polly/polly.onnx",
    # Q
    "queen_of_lights": "Queen_of_lights/Queen_of_lights.onnx",
    # R
    "r2d2": "r2d2/r2d2.onnx",
    "ronaldo": "ronaldo/Ronaldo.onnx",
    "rubber_duck": "rubber_duck/rubber_duck.onnx",
    # S
    "santana": "santana/Santana.onnx",
    "scarlett": "scarlett/Scarlett.onnx",
    "scooby": "scooby/Scooby.onnx",
    "sheila": "sheila/sheila_v2.onnx",
    "skynet": "skynet/Skynet.onnx",
    # T
    "tars": "TARS/TARS.onnx",
    "terminator": "terminator/Terminator.onnx",
    # U
    "ultra_house": "ultra_house/ultra_house.onnx",
    # V
    "veronica": "veronica/veronica.onnx",
    # W
    "wall_e": "wall-e/wall-e.onnx",
    "wheatley": "wheatley/wheatley.onnx",
    "winston": "winston/Winston.onnx",
    # Y
    "yo_bitch": "yo_bitch/yo_bitch.onnx",
    "yo_homie": "yo_homie/yo_homie.onnx",
}

# Featured models to show at top of dropdown
FEATURED_MODELS = [
    "alexa",          # Built-in (Amazon style)
    "computer",       # Star Trek classic (community)
    "jarvis",         # Iron Man (community)
    "hey_jarvis",     # Built-in
    "hey_friday",     # Iron Man (community)
    "glados",         # Portal (community)
    "hal",            # 2001: A Space Odyssey (community)
    "tars",           # Interstellar (community)
    "hey_marvin",     # Hitchhiker's Guide (community)
    "terminator",     # Classic (community)
]

# Alternate transcriptions Whisper produces (for filtering from transcripts)
ALTERNATES = {
    "wally": "wall_e",
    "wall e": "wall_e",
    "walle": "wall_e",
}


def download_model(name: str) -> str:
    """Download a community model. Returns path to .onnx file."""
    if name not in COMMUNITY_MODELS:
        raise ValueError(f"Unknown community model: {name}")
    url = f"{_COMMUNITY_BASE}/{COMMUNITY_MODELS[name]}"
    os.makedirs(CACHE_DIR, exist_ok=True)
    return rp.download_url(url, CACHE_DIR, skip_existing=True, show_progress=True)


def get_models_ordered() -> list:
    """Get all models with featured ones first, then rest alphabetically."""
    all_models = set(COMMUNITY_MODELS.keys()) | set(BUILTIN_MODELS)
    featured = [m for m in FEATURED_MODELS if m in all_models]
    rest = sorted(m for m in all_models if m not in featured)
    return featured + rest


def get_model_display_name(name: str) -> str:
    """Get display name for a model (e.g. 'hey_marvin' -> 'Hey Marvin')."""
    return name.replace("_", " ").title()


def get_all_normalized() -> set:
    """Get all wake words in normalized form for blacklist matching."""
    result = set()
    for name in COMMUNITY_MODELS:
        result.add(name.replace("_", " ").lower())
    for name in BUILTIN_MODELS:
        result.add(name.replace("_", " ").lower())
    result.update(ALTERNATES.keys())
    return result


class OpenWakeWordEngine(WakeWordEngine):
    """OpenWakeWord ML-based wake word detection."""

    name = "openwakeword"
    display_name = "OpenWakeWord"

    def __init__(
        self,
        on_wake: WakeWordCallback,
        on_stop: Optional[StopCallback] = None,
        model: str = 'computer',
        sensitivity: float = 0.2,
    ):
        super().__init__(on_wake, on_stop)
        self.model_name = model
        self.sensitivity = sensitivity
        self._oww_model = None
        self._stream = None
        self._buffer = collections.deque(maxlen=SAMPLE_RATE * BUFFER_SECONDS)
        self._last_trigger = 0
        self._is_recording = False

    def _load_model(self) -> bool:
        """Lazy load the OpenWakeWord model."""
        if self._oww_model is not None:
            return True
        try:
            from openwakeword.model import Model
            if self.model_name in BUILTIN_MODELS:
                model_path = self.model_name
            elif self.model_name in COMMUNITY_MODELS:
                model_path = download_model(self.model_name)
            else:
                raise ValueError(f"Unknown wake word model: {self.model_name}")
            self._oww_model = Model(
                wakeword_models=[model_path],
                inference_framework='onnx',
            )
            print(f"[wakeword] OpenWakeWord model loaded: {self.model_name}")
            return True
        except Exception as e:
            print(f"[wakeword] Failed to load model: {e}")
            return False

    def start(self) -> None:
        """Start listening for wake words."""
        if self._running:
            return
        if not self._load_model():
            raise RuntimeError("Failed to load wake word model")

        import sounddevice as sd
        self._buffer.clear()

        def callback(indata, frames, time_info, status):
            if status:
                print(f"[wakeword] Audio status: {status}")
            audio = (indata[:, 0] * 32767).astype(np.int16)
            self._buffer.extend(audio)

            prediction = self._oww_model.predict(audio)
            for model_name, score in prediction.items():
                if score > self.sensitivity:
                    now = time.time()
                    if now - self._last_trigger < COOLDOWN_SECONDS:
                        continue
                    self._last_trigger = now

                    if self._is_recording:
                        print(f"[wakeword] {model_name} ({score:.2f}) -> STOP")
                        if self.on_stop:
                            self.on_stop()
                    else:
                        print(f"[wakeword] {model_name} ({score:.2f}) -> START")
                        pre_buffer = np.array(self._buffer, dtype=np.float32) / 32767.0
                        self.on_wake(pre_buffer)

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            callback=callback,
            blocksize=FRAME_SAMPLES,
        )
        self._stream.start()
        self._running = True
        print(f"[wakeword] OpenWakeWord listening (say '{self.model_name}')")

    def stop(self) -> None:
        """Stop listening."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._running = False
        print("[wakeword] OpenWakeWord stopped")

    def pause(self) -> None:
        """Pause during recording - keeps listening to detect stop command."""
        self._is_recording = True
        # Don't stop the stream - keep listening so wake word can stop recording

    def resume(self) -> None:
        """Resume after recording."""
        self._is_recording = False

    def reset(self) -> None:
        """Reset model state."""
        if self._oww_model is not None:
            self._oww_model.reset()

    def set_model(self, model: str) -> None:
        """Change wake word model (restarts if running)."""
        was_running = self._running
        if was_running:
            self.stop()
        self.model_name = model
        self._oww_model = None
        if was_running:
            self.start()

    def set_sensitivity(self, sensitivity: float) -> None:
        """Update sensitivity threshold."""
        self.sensitivity = sensitivity

    @classmethod
    def get_available_models(cls) -> list:
        """Get all available wake word models."""
        return get_models_ordered()

    @classmethod
    def get_model_display_name(cls, model: str) -> str:
        """Get display name for a model."""
        return get_model_display_name(model)

    @classmethod
    def get_all_normalized(cls) -> set:
        """Get all wake words in normalized form."""
        return get_all_normalized()
