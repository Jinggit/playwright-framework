import json
import os

def load_config(env="qa"):
    config_path = os.path.join(os.path.dirname(__file__), "..", "configs", f"{env}.json")
    with open(config_path, "r") as f:
        return json.load(f)
