import os
import sys
from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent
WINDOWS = sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")
AM_I_RUNNING_IN_DOCKER = os.environ.get("AM_I_RUNNING_IN_DOCKER", False)

# DEFAULT SETTINGS
# ================
# PROJECT_NAME = "my_awessome_project_name"
PROJECT_NAME = BASE_DIR.stem
DEBUG = False
MODE = "prod"  # prod, dev, test, stage


# LOGGING DEFAULT SETTINGS
# ========================
USE_LOGGING = True
LOGS_DIR = "logs"
# DEFAULT_LOGGER_NAME = PROJECT_NAME
CREATE_LOG_FILES = True
ROOT_LOGGER = PROJECT_NAME

# DATABASE DEFAULT SETTINGS
# =========================
DB_TYPE = None
DB_ASYNC = None
# DB_MODE = "default"
ECHO_SQL = False
