# detect_keylogger.py
import psutil, time, os

SUSPICIOUS = ["keyboard", "pynput", "pyhook"]   # common key-log libs
LOG_FILES   = ["keylog.txt"]

def check():
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = " ".join(p.info['cmdline'] or [])
            if any(lib in cmd.lower() for lib in SUSPICIOUS):
                print(f"[!] Suspicious: {p.info['pid']} {cmd}")
            if any(log in cmd for log in LOG_FILES):
                print(f"[!] Log file creation: {cmd}")
        except Exception:
            pass

    for f in LOG_FILES:
        if os.path.exists(f):
            print(f"[!] Found suspicious file: {f}")

if __name__ == "__main__":
    print("Scanning… (Ctrl+C to stop)")
    try:
        while True:
            check()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopped.")