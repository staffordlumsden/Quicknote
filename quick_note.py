from pathlib import Path
import sys
from datetime import datetime

NOTES_DIR = Path("/sdcard/Notes/Daily")
NOTES_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # Require at least one argument
    if len(sys.argv) < 2:
        print("Usage: quick_note.py \"your note text\"")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%H:%M")

    # Make a safe filename and full path
    path = NOTES_DIR / f"{today}.md"

    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(f"- {timestamp} {text}\n")
        print(f"✅ Note saved to: {path}")
    except PermissionError:
        print("❌ Permission denied. Run `termux-setup-storage` first to allow /sdcard access.")
    except Exception as e:
        print(f"❌ Error writing note: {e}")

if __name__ == "__main__":
    main()

