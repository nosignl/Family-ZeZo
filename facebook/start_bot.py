#!/usr/bin/env python3
"""
Simple runner for GitHub Codespaces
Just run: python3 start_bot.py
"""
import subprocess
import sys
import os
import time
from datetime import datetime

def install_packages():
    """Install required packages"""
    packages = ['selenium', 'chromedriver-autoinstaller', 'requests']
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_files():
    """Check if required files exist"""
    if not os.path.exists('instagram_bot.py'):
        print("❌ ERROR: instagram_bot.py not found!")
        print("📂 Files in directory:")
        for file in os.listdir('.'):
            print(f"  - {file}")
        return False
    
    if not os.path.exists('cookies.txt'):
        print("❌ ERROR: cookies.txt not found!")
        print("📝 Please add your Instagram cookies to cookies.txt")
        return False
    
    return True

def run_bot():
    """Run the Instagram bot"""
    print("🚀 INSTAGRAM BOT - GITHUB CODESPACES")
    print("=" * 50)
    
    if not check_files():
        return
    
    print("📦 Installing packages...")
    install_packages()
    
    print("🤖 Starting Instagram bot...")
    print("📊 Press Ctrl+C to stop")
    print("")
    
    session_count = 0
    
    try:
        while True:
            session_count += 1
            print(f"🔄 SESSION #{session_count} - {datetime.now()}")
            
            try:
                # Run the bot
                result = subprocess.run([sys.executable, 'instagram_bot.py'], 
                                      capture_output=False, text=True)
                
                if result.returncode == 0:
                    print("✅ Bot session completed successfully!")
                    print("⏸️ Waiting 30 minutes before next session...")
                    time.sleep(1800)  # 30 minutes
                else:
                    print("⚠️ Bot encountered an error. Restarting in 2 minutes...")
                    time.sleep(120)   # 2 minutes
                    
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("🔄 Restarting in 2 minutes...")
                time.sleep(120)
                
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")

if __name__ == "__main__":
    run_bot()
