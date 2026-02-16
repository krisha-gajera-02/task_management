import json
import os
from config import DATA_FILE


class JSONStorage:
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


    def load(self):
        try:
            
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []

    def save(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
