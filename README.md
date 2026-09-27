# QuickNote Interactive

A simple interactive CLI for taking daily notes in Termux.

## Features

- Interactive prompt for writing notes.
- Multi-line input support.
- Displays today's notes directly in the terminal.
- Saves notes with timestamps to daily markdown files (`/sdcard/Notes/Daily/YYYY-MM-DD.md`).
- Stylish and colorful interface.

## Requirements

- Python 3
- `rich`
- `prompt_toolkit`
- `pyfiglet`

## Installation

Install the required Python libraries using pip:

```bash
pip install rich prompt_toolkit pyfiglet
```

## Usage

Run the script from your terminal:

```bash
python quick_note_interactive.py
```

-   Type your note and press `Esc` + `Enter` to save.
-   Use the commands below for more actions.

## Commands

-   `/today`: Reads and displays the content of today's note file within the terminal.
-   `/exit` or `/quit`: Exits the application.
-   `Ctrl+D`: Exits the application.
