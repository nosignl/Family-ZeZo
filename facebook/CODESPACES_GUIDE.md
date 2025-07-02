# 🚀 GITHUB CODESPACES SETUP GUIDE

## Quick Start (3 steps):

### 1. **Upload Your Bot Files**
   - Make sure `instagram_bot.py` and `cookies.txt` are in your Codespaces workspace
   - Your cookies should be in Netscape format (which you already have!)

### 2. **Run the Setup**
   ```bash
   chmod +x run_bot.sh
   ./run_bot.sh
   ```

### 3. **Alternative: Python Runner**
   ```bash
   python3 start_bot.py
   ```

## 🔧 What the script does:
- ✅ Auto-installs Chrome for Codespaces
- ✅ Installs Python packages (selenium, chromedriver-autoinstaller)
- ✅ Runs your bot in headless mode (perfect for 24/7)
- ✅ Auto-restarts on errors
- ✅ Runs continuous sessions with 30-minute breaks

## 💡 GitHub Codespaces Benefits:
- **FREE**: 60 hours/month (perfect for 24/7 for ~2.5 days)
- **Always-on**: Keep browser tab open = bot keeps running
- **Pre-configured**: Linux environment ready to go
- **No setup needed**: Everything works out of the box

## 🎯 Commands to run in Codespaces terminal:

```bash
# Method 1: Bash script (full featured)
chmod +x run_bot.sh
./run_bot.sh

# Method 2: Python runner (simpler)
python3 start_bot.py

# Method 3: One-time test
python3 instagram_bot.py
```

## 🛑 To stop the bot:
- Press `Ctrl + C` in the terminal
- Bot will finish current session and stop safely

## 📊 Expected output:
```
🚀 INSTAGRAM BOT - GITHUB CODESPACES
====================================
📁 Working in: /workspaces/your-repo
📋 Files available:
instagram_bot.py cookies.txt
✅ All files found!
📦 Installing packages...
🌐 Setting up Chrome for Codespaces...
✅ Chrome installed!
🚀 Starting Instagram Bot...
▶️  SESSION 1 - 14:30:25
```

Your bot is now ready to run 24/7 in GitHub Codespaces! 🎉
