import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SELENIUM_REMOTE_EXECUTOR = os.getenv('SELENIUM_REMOTE_EXECUTOR')
