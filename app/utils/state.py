import json
import os

STATE_FILE = "state.json"

def load_state():
    """Загружает состояние из файла."""
    try:
        with open(STATE_FILE, "r") as file:
            return json.load(file).get("enabled", False)
    except FileNotFoundError:
        return False

def save_state(enabled):
    """Сохраняет состояние в файл."""
    with open(STATE_FILE, "w") as file:
        json.dump({"enabled": enabled}, file)
