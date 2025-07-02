#!/bin/bash
echo "🚀 INSTAGRAM BOT - GITHUB CODESPACES"
echo "===================================="
echo ""

# Get current directory and navigate to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Working in: $SCRIPT_DIR"
cd "$SCRIPT_DIR"

# List files for debugging
echo "📋 Files available:"
ls -la *.py *.txt 2>/dev/null

# Check if bot exists
if [ ! -f "instagram_bot.py" ]; then
    echo "❌ ERROR: instagram_bot.py not found!"
    echo "Available files:"
    ls -la
    exit 1
fi

# Check if cookies exist
if [ ! -f "cookies.txt" ]; then
    echo "❌ ERROR: cookies.txt not found!"
    echo "Please add your Instagram cookies to cookies.txt"
    exit 1
fi

echo "✅ All files found!"
echo ""

# Install packages
echo "📦 Installing packages..."
python3 -m pip install selenium chromedriver-autoinstaller requests --quiet

# Install Chrome for Codespaces
echo "🌐 Setting up Chrome for Codespaces..."
if ! command -v google-chrome &> /dev/null; then
    echo "Installing Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 2>/dev/null
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list >/dev/null
    sudo apt update -qq 2>/dev/null
    sudo apt install -y google-chrome-stable 2>/dev/null
    echo "✅ Chrome installed!"
else
    echo "✅ Chrome already available!"
fi

# Set environment for headless mode
export DISPLAY=:99

echo ""
echo "🚀 Starting Instagram Bot..."
echo "📊 Running in GitHub Codespaces mode"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Main bot loop
session=0
while true; do
    session=$((session + 1))
    echo "▶️  SESSION $session - $(date '+%H:%M:%S')"
    
    # Run the bot
    python3 "$SCRIPT_DIR/instagram_bot.py"
    result=$?
    
    echo ""
    if [ $result -eq 0 ]; then
        echo "✅ Session $session completed successfully!"
        echo "⏰ Waiting 30 minutes before next session..."
        sleep 1800
    else
        echo "⚠️  Session $session had errors (code: $result)"
        echo "🔄 Restarting in 2 minutes..."
        sleep 120
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
done
