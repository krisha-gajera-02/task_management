DATA_FILE = "data/tasks.json"

PRIORITIES = {"low", "medium", "high"}
STATUSES = {"pending", "completed"}

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tasks.json")

