#!/usr/bin/env python3
import sys
import io
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import pyfiglet
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition

# --- Setup for Rich and Prompt Toolkit ---
console = Console()
session = PromptSession()
bindings = KeyBindings()

# --- Keybindings for multiline input and exit ---
@bindings.add('c-d')
def _(event):
    """ Exit when `c-d` is pressed. """
    event.app.exit()

submit_on_empty_line = Condition(lambda: get_app().current_buffer.document.current_line == '')

@bindings.add('enter', filter=submit_on_empty_line)
def _(event):
    """ Submit input when Enter is pressed on an empty line. """
    event.current_buffer.validate_and_handle()

@bindings.add('escape', 'enter')
def _(event):
    """ Submit input on Option+Enter or Esc+Enter. """
    event.current_buffer.validate_and_handle()

# --- Banner ---
def print_banner():
    """Prints a colorful, responsive Figlet banner."""
    console.print("\n")
    width = console.width
    if width < 80:
        banner_text = "QuickNote"
    else:
        banner_text = pyfiglet.figlet_format("QuickNote", font="standard")
    
    console.print(Align.center(f"[bold blue]{banner_text}[/bold blue]"))
    console.print(Align.center("v1.2 (24 October 2025)"))
    console.print("\n")
    console.print(Panel("A simple interactive CLI for taking daily notes.",
                        title="Welcome", border_style="green"))
    console.print("Type [bold cyan]/today[/bold cyan] to display today's note. Type [bold red]/exit[/bold red] to quit.\n")


# --- Core Note-Taking Logic ---
NOTES_DIR = Path.home() / ".quicknote" / "Notes" / "Daily"
NOTES_DIR.mkdir(parents=True, exist_ok=True)

def get_today_note_path():
    """Returns the Path object for today's note file."""
    today = datetime.now().strftime("%Y-%m-%d")
    return NOTES_DIR / f"{today}.md"

def save_note(text: str):
    """Appends a timestamped note to today's note file."""
    now = datetime.now()
    timestamp = now.strftime("%H:%M")
    path = get_today_note_path()

    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(f"- {timestamp} {text}\n")
        console.print(Panel(f"✅ Note saved to: [bold green]{path}[/bold green]"))
    except PermissionError:
        console.print(Panel("❌ [bold red]Permission denied.[/bold red] Run `termux-setup-storage` first to allow /sdcard access."))
    except Exception as e:
        console.print(Panel(f"❌ [bold red]Error writing note:[/bold red] {e}"))

def display_note(path: Path):
    """Reads and displays the note content in a panel."""
    if not path.exists():
        console.print(Panel(f"🤷 No note file found for today at [yellow]{path}[/yellow]. Write a note first!", title="[bold yellow]Not Found[/bold yellow]"))
        return
    
    try:
        content = path.read_text(encoding="utf-8")
        console.print(Panel(content, title=f"📝 {path.stem}", border_style="cyan"))
    except Exception as e:
        console.print(Panel(f"❌ [bold red]An unexpected error occurred while reading the file:[/bold red] {e}"))


def get_multiline_input():
    """Gets multi-line input from the user."""
    return session.prompt(
        "> ",
        placeholder="Enter your note...",
        multiline=True,
        key_bindings=bindings,
        prompt_continuation="... "
    )

def main():
    """Main function to run the interactive note-taking CLI."""
    print_banner()

    while True:
        try:
            user_input = get_multiline_input()
            command = user_input.lower().strip()

            if not command:
                continue

            if command in ['/exit', '/quit']:
                break
            
            if command == '/today':
                note_path = get_today_note_path()
                display_note(note_path)
                continue

            save_note(user_input)

        except (KeyboardInterrupt, EOFError):
            break

    console.print(Panel("[bold]Goodbye![/bold]", border_style="blue"))

if __name__ == "__main__":
    # Ensure stdout is configured for UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    main()