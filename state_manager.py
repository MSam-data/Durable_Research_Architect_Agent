import json
import os

STATE_FILE = "agent_state.json"

def save_state(step_name: str, data: dict):
    """Saves a specific phase's data to the JSON state file."""
    state = load_state()
    state[step_name] = data
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        # Fixed: the argument is ensure_ascii
        json.dump(state, f, indent=4, ensure_ascii=False)

def load_state():
    """Loads the current progress from the JSON state file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def clear_state():
    """Deletes the state file to start a completely fresh run."""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("🧹 State cleared. Starting fresh.")