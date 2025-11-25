# Keylogger & Keylogger Detector

A dual-tool Python project consisting of:
1. **Keylogger** — records keystrokes using `pynput` and logs them to a timestamped text file.
2. **Keylogger Detector** — scans active processes to detect suspicious executables or scripts resembling keyloggers and alerts the user.

This project was built to understand how keylogging tools function internally, and how detection mechanisms identify them based on process behavior and execution parameters.

---

## 🔍 Overview

Keyloggers are commonly used in both security testing and malware.  
This project demonstrates:
- How keystroke capturing works at a low level using Python hooks.
- How defenders can detect running keyloggers by inspecting system process arguments and behavior.

The detector was tested against the keylogger built in this repository to validate accurate detection.

---

## 🧠 Features

### 🖥 Keylogger
- Captures keystrokes in real time
- Logs all keystrokes to `key_logs.txt` for later analysis
- Includes timestamps & readable formatting
- Runs silently in the background

### 🛡 Keylogger Detector
- Scans currently running processes
- Searches for suspicious patterns such as:
  - References to `pynput` or logging arguments
  - File or process names matching known keylogger behavior
- Alerts user if a possible keylogger is running

---

## 🧱 Tech Stack

- **Language:** Python 3.x
- **Libraries:** `pynput`, `psutil` (or whichever is used for process scanning)
- **Domain concepts:** process inspection, OS monitoring, input capture, behavior analysis

---

## 📦 Installation

```bash
git clone https://github.com/ezhilan404/Keylogger-and-detection.git
cd keylogger-and-detector

