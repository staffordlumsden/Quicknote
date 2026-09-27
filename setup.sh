#!/bin/bash

# A script to set up the QuickNote interactive CLI tool.

echo "🚀 Starting QuickNote setup..."

# Get the absolute path of the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
MAIN_SCRIPT="$SCRIPT_DIR/quick_note_interactive.py"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
LAUNCHER_PATH="$SCRIPT_DIR/bin/quicknote"

# 1. Create a virtual environment
echo "🐍 Creating a Python virtual environment..."
if python3 -m venv "$VENV_DIR"; then
    echo "✅ Virtual environment created successfully."
else
    echo "❌ Failed to create virtual environment. Aborting."
    exit 1
fi

# 2. Install dependencies into the virtual environment
echo "🐍 Installing Python dependencies from requirements.txt..."
if "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE"; then
    echo "✅ Dependencies installed successfully."
else
    echo "❌ Failed to install dependencies. Aborting."
    exit 1
fi

# 3. Make the main script executable
echo "🔑 Making the main script executable..."
chmod +x "$MAIN_SCRIPT"

# 4. Create a launcher script to avoid noexec issues
echo "🔗 Creating a launcher script at $LAUNCHER_PATH..."
# Create the bin directory if it doesn't exist
mkdir -p "$(dirname "$LAUNCHER_PATH")"

# Remove existing file/symlink to avoid errors
if [ -e "$LAUNCHER_PATH" ]; then
    echo "Launcher already exists. Removing it."
    rm "$LAUNCHER_PATH"
fi

# Create the launcher script using a heredoc
cat > "$LAUNCHER_PATH" << EOL
#!/bin/bash
# This script acts as a launcher to bypass noexec restrictions on /sdcard
"$VENV_DIR/bin/python" "$MAIN_SCRIPT" "$@"
EOL

# Make the launcher executable
chmod +x "$LAUNCHER_PATH"

echo -e "\n🎉 Setup complete!"
echo "To run the application, you need to add the project's bin directory to your PATH."
echo "You can do this by running: export PATH=\"$SCRIPT_DIR/bin:$PATH\""
echo "Then you can run the application by typing: quicknote"