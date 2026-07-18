from pathlib import Path

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

SUBREDDIT = "AskReddit"

REDDIT_URL = f"https://www.reddit.com/r/{SUBREDDIT}/hot/"

NUMBER_OF_COMMENTS = 8

MAX_COMMENT_CHAR = 150