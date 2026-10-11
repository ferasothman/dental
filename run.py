import sys, time, threading, webbrowser, socket, traceback
import uvicorn

from app.core.paths import data_dir

HOST, PORT = "127.0.0.1", 8000
LOG_FILE = data_dir() / "error.log"

# عند البناء بدون نافذة يكون stdout/stderr فارغين، فنحوّلهما إلى ملف
if sys.stdout is None or sys.stderr is None:
    _log = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
    sys.stdout = sys.stdout or _log
    sys.stderr = sys.stderr or _log


def port_in_use() -> bool:
    with socket.socket() as s:
        return s.connect_ex((HOST, PORT)) == 0


def open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    try:
        # إن كان البرنامج يعمل أصلاً: افتح المتصفح فقط
        if port_in_use():
            webbrowser.open(f"http://{HOST}:{PORT}")
            sys.exit(0)

        from main import app
        threading.Thread(target=open_browser, daemon=True).start()
        uvicorn.run(app, host=HOST, port=PORT, log_config=None)
    except SystemExit:
        raise
    except Exception:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
        raise