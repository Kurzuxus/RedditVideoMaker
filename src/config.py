from pathlib import Path
from json import load

# Root of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
# --------------------------------------
# PATHS
# --------------------------------------

ASSETS = ROOT_DIR / "assets"

GENERATED = ASSETS / "generated"

IMAGES = GENERATED / "images"

AUDIOS = GENERATED / "audios"

MINECRAFT_VIDEO = ASSETS / "minecraft" / "minecraft.mp4"

OUTPUT_PATH = ROOT_DIR / "output" / "output_video.mp4"

# --------------------------------------
# REDDIT
# --------------------------------------

USER_SETTINGS_PATH = ROOT_DIR / "src" / "user_settings.json"

def load_user_settings() -> dict:
    with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as file:
        return load(file)
