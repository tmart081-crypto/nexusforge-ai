"""App-wide constants and metadata."""

import time

# Set once, at first import of this module (Streamlit reruns main.py per
# interaction but only imports each module once per server process), so
# this marks server start time, not per-user session time.
START_TIME = time.time()

APP_NAME = "NexusForge AI Platform"
APP_VERSION = "1.0.0"
CLIENT_NAME = "Aether Dynamics Global"
ENGAGEMENT_CODE = "NF-CAP-01"

LOG_DIR = "logs"
LOG_FILE = "nexusforge.log"

# Max upload size for images/documents, in MB
MAX_UPLOAD_MB = 20
