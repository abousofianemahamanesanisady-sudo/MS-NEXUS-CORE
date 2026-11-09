import os

ADMIN_KEY = os.getenv("NEXUS_ADMIN_KEY", "")
DB_PATH = os.getenv("NEXUS_DB_PATH", "nexus.db")
IMAGE_MODEL_ID = os.getenv("NEXUS_IMAGE_MODEL_ID", "")
OUTPUT_DIR = os.getenv("NEXUS_OUTPUT_DIR", "outputs")
