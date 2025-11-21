import psutil
import os
import time
from pathlib import Path

SUSPICIOUS_NAME_KEYWORDS = [
    "keylog", "key_log", "keystroke", "pynput", "keyboard",
    "hook", "inputlogger", "logger"
]

SUSPICIOUS_DIR_KEYWORDS = [
    r"\\AppData\\Local\\Temp",
    r"\\AppData\\Roaming",
    r"\\Users\\Public",
]

NETWORK_CONNECTION_THRESHOLD = 5

SCAN_INTERVAL = 10

def is_path_suspicious(path_str: str) -> bool:
    """Return True if the executable path looks suspicious."""
    if not path_str:
        return False
    path_lower = path_str.lower()
    for keyword in SUSPICIOUS_DIR_KEYWORDS:
        if keyword.lower() in path_lower:
            return True
    return False


def has_suspicious_name(name: str) -> bool:
    """Return True if process name/command line looks suspicious."""
    if not name:
        return False
    name_lower = name.lower()
    for keyword in SUSPICIOUS_NAME_KEYWORDS:
        if keyword in name_lower:
            return True
    return False


def get_process_info(proc: psutil.Process) -> dict:
    """Safely collect info about a process, handling access issues."""
    info = {
        "pid": proc.pid,
        "name": None,
        "exe": None,
        "cmdline": "",
        "num_remote_conns": 0,
        "suspicious_reasons": [],
    }

    try:
        info["name"] = proc.name()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    try:
        exe = proc.exe()
        info["exe"] = exe
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        exe = None

    try:
        cmdline_list = proc.cmdline()
        info["cmdline"] = " ".join(cmdline_list)
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    try:
        conns = proc.connections(kind="inet")
        remote_conns = [c for c in conns if c.raddr]  # has remote address
        info["num_remote_conns"] = len(remote_conns)
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    if has_suspicious_name(info["name"] or ""):
        info["suspicious_reasons"].append(
            f"suspicious process name: {info['name']}"
        )

    if has_suspicious_name(info["cmdline"]):
        info["suspicious_reasons"].append(
            "suspicious keywords in command line"
        )

    if exe and is_path_suspicious(exe):
        info["suspicious_reasons"].append(
            f"executable in suspicious directory: {exe}"
        )

    if info["num_remote_conns"] >= NETWORK_CONNECTION_THRESHOLD:
        info["suspicious_reasons"].append(
            f"many remote connections ({info['num_remote_conns']})"
        )

    return info


def scan_once():
    """Scan all running processes and print any suspicious ones."""
    suspicious_processes = []

    for proc in psutil.process_iter(attrs=[]):
        try:
            info = get_process_info(proc)
        except psutil.NoSuchProcess:
            continue

        if info["suspicious_reasons"]:
            suspicious_processes.append(info)

    if not suspicious_processes:
        print("[+] No suspicious processes detected in this scan.")
        return

    print("\n[!] Suspicious processes detected:")
    print("-" * 80)
    for info in suspicious_processes:
        print(f"PID: {info['pid']}")
        print(f"Name: {info['name']}")
        print(f"Executable: {info['exe']}")
        print(f"Command line: {info['cmdline']}")
        print(f"Remote connections: {info['num_remote_conns']}")
        print("Reasons:")
        for r in info["suspicious_reasons"]:
            print(f"  - {r}")
        print("-" * 80)


def monitor_loop():
    """Continuously scan every SCAN_INTERVAL seconds."""
    print("[*] Starting keylogger heuristic monitor.")
    print(f"[*] Scan interval: {SCAN_INTERVAL} seconds.")
    print("[*] Press Ctrl+C to stop.\n")

    try:
        while True:
            print(f"[*] Running scan at {time.ctime()}...")
            scan_once()
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        print("\n[+] Monitor stopped by user.")


if __name__ == "__main__":
    # Run one immediate scan, then enter a monitoring loop.
    scan_once()
    print("\n--------------------------------------------")
    monitor_loop()
