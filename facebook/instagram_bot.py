#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLE INSTAGRAM BOT - WORKS EVERYWHERE
=======================================
Follows people from Kurdish hashtag post likes
Sends "working perfect" message to @ze2ow
Super simple - just run and go!
"""

import time
import random
import os
import platform
from datetime import datetime

def install_packages():
    """Install required packages"""
    try:
        import selenium
        import chromedriver_autoinstaller
        print("Packages already installed")
    except ImportError:
        print("Installing packages...")
        os.system("pip install selenium chromedriver-autoinstaller")
        import selenium
        import chromedriver_autoinstaller

# Install packages first
install_packages()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SimpleBot:
    def __init__(self):
        self.driver = None
        self.follows = 0
        self.comments = 0
        self.likes = 0
        
        # Safe emoji comments for posts
        self.emoji_comments = [
            "🔥🔥🔥", "💪💪", "❤️❤️", "😍😍", "👏👏", "🙌🙌", 
            "✨✨", "💯💯", "🚀🚀", "⚡⚡", "🌟🌟", "💝💝",
            "🔥 Amazing!", "💪 Strong!", "❤️ Love it!", "😍 Beautiful!",
            "👏 Great work!", "🙌 Awesome!", "✨ Perfect!", "💯 Incredible!",
            "🚀 Fire!", "⚡ So good!", "🌟 Fantastic!", "💝 Love this!"
        ]
        
    def setup_browser(self):
        """Setup Chrome browser (works on Linux servers without sudo)"""
        print("Starting Chrome...")
        
        # Detect operating system
        is_linux = platform.system().lower() == 'linux'
        is_windows = platform.system().lower() == 'windows'
        
        if is_linux:
            print("🐧 Linux detected - configuring for server mode")
        elif is_windows:
            print("🪟 Windows detected - configuring for desktop mode")
        
        try:
            import chromedriver_autoinstaller
            chromedriver_autoinstaller.install()
        except:
            pass
        
        options = Options()
        
        # Essential for Linux servers without sudo
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Linux-specific settings for 24/7 operation
        if is_linux:
            options.add_argument('--headless')  # Run without GUI on Linux
            options.add_argument('--no-first-run')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--disable-hang-monitor')
            options.add_argument('--disable-prompt-on-repost')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-extensions-with-background-pages')
            
            # Memory optimization for 24/7 running
            options.add_argument('--memory-pressure-off')
            options.add_argument('--max_old_space_size=4096')
            
            # Linux user agent
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        else:
            # Windows settings - keep visual mode for debugging
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Hide automation
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable notifications and popups
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            
            if is_linux:
                print("✅ Chrome started successfully (headless mode for Linux 24/7)")
            else:
                print("✅ Chrome started successfully (visual mode for Windows)")
            return True
        except Exception as e:
            print(f"❌ Chrome failed: {e}")
            
            # Try alternative Chrome paths for Linux without sudo
            if is_linux:
                print("� Trying alternative Chrome setup...")
                try:
                    # Try with different Chrome binary paths
                    alt_chrome_paths = [
                        "/usr/bin/google-chrome",
                        "/usr/bin/google-chrome-stable", 
                        "/usr/bin/chromium-browser",
                        "/usr/bin/chromium",
                        "/snap/bin/chromium"
                    ]
                    
                    for chrome_path in alt_chrome_paths:
                        if os.path.exists(chrome_path):
                            print(f"🎯 Found Chrome at: {chrome_path}")
                            options.binary_location = chrome_path
                            self.driver = webdriver.Chrome(options=options)
                            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                            self.wait = WebDriverWait(self.driver, 10)
                            print("✅ Chrome started with alternative path!")
                            return True
                    
                    print("❌ Could not find Chrome. Please ask admin to install:")
                    print("   sudo apt install google-chrome-stable")
                    
                except Exception as e2:
                    print(f"❌ Alternative Chrome setup failed: {e2}")
            
            print("💡 On Linux without sudo, make sure Chrome is installed system-wide")
            return False
    
    def load_cookies(self):
        """Load Instagram cookies"""
        print("Loading cookies...")
        
        if not os.path.exists("cookies.txt"):
            print("ERROR: cookies.txt not found!")
            return False
        
        self.driver.get("https://www.instagram.com/")
        time.sleep(3)
        
        # Dismiss any notifications popup
        try:
            self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
            time.sleep(1)
        except:
            pass
        
        with open("cookies.txt", 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split('\t')
                    if len(parts) >= 7 and 'instagram.com' in parts[0]:
                        try:
                            cookie = {'name': parts[5], 'value': parts[6], 'domain': parts[0]}
                            self.driver.add_cookie(cookie)
                        except:
                            pass
        
        self.driver.refresh()
        time.sleep(4)
        
        # Dismiss notification popups after login
        try:
            not_now = self.driver.find_element(By.XPATH, "//button[text()='Not Now']")
            not_now.click()
            time.sleep(2)
        except:
            pass
        
        if "login" in self.driver.current_url.lower():
            print("Login failed!")
            return False
        
        print("Logged in")
        return True
    
    def send_message_to_ze2ow(self, message):
        """Send message to @ze2ow"""
        try:
            print("Sending message to @ze2ow...")
            
            # Go to user profile first
            self.driver.get("https://www.instagram.com/ze2ow/")
            time.sleep(5)
            
            # Handle popups
            try:
                self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
                time.sleep(2)
            except:
                pass
            
            # Click Message button
            try:
                message_btn = self.driver.find_element(By.XPATH, "//div[text()='Message']")
                message_btn.click()
                time.sleep(4)
            except:
                print("Could not find Message button")
                return False
            
            # Find message input
            try:
                msg_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
                )
                
                msg_input.click()
                time.sleep(1)
                msg_input.send_keys(message)
                time.sleep(2)
                
                # Send message
                try:
                    send_btn = self.driver.find_element(By.XPATH, "//div[text()='Send']")
                    send_btn.click()
                except:
                    msg_input.send_keys(Keys.ENTER)
                
                print("Message sent!")
                time.sleep(3)
                return True
                
            except Exception as e:
                print(f"Message input failed: {e}")
                return False
            
        except Exception as e:
            print(f"Message failed: {e}")
            return False
    
    def follow_from_hashtag(self, hashtag):
        """Follow people from hashtag likes"""
        try:
            print(f"Following from #{hashtag}...")
            
            # Go to hashtag with retry
            for attempt in range(3):
                self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
                time.sleep(6)
                
                # Handle notification popups
                try:
                    self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()
                    time.sleep(2)
                except:
                    pass
                
                # Check if posts loaded
                posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                if posts:
                    break
                print(f"Attempt {attempt + 1}: No posts found, retrying...")
                time.sleep(3)
            
            if not posts:
                print("No posts found after retries")
                return False
            
            # Click random post
            selected_post = random.choice(posts[:12])
            self.driver.execute_script("arguments[0].click();", selected_post)
            print("📱 Post opened, waiting for it to load...")
            time.sleep(8)  # Increased wait time for post to fully load
            
            # FIRST: Like the post (always try with multiple attempts)
            like_success = self.like_current_post()
            if like_success:
                print("✅ Post liked successfully")
            else:
                print("❌ FAILED to like post")
            time.sleep(2)
            
            # SECOND: Add a comment on EVERY post (always try with multiple attempts)
            comment_success = self.comment_on_current_post()
            if comment_success:
                print("✅ Comment posted successfully")
            else:
                print("❌ FAILED to comment on post")
            time.sleep(2)
            
            # Try multiple strategies to find and click likes
            likes_clicked = False
            likes_strategies = [
                # Strategy 1: Direct likes link
                "//a[contains(@href, '/liked_by/')]",
                # Strategy 2: Like count text (clickable)
                "//span[contains(text(), 'like')]",
                # Strategy 3: Button with like text
                "//button[contains(text(), 'like')]",
                # Strategy 4: Like count button
                "//button[contains(@aria-label, 'like')]",
                # Strategy 5: Generic approach - find like count
                "//*[contains(text(), 'like') and (contains(text(), '1') or contains(text(), '2') or contains(text(), '3') or contains(text(), '4') or contains(text(), '5') or contains(text(), '6') or contains(text(), '7') or contains(text(), '8') or contains(text(), '9'))]"
            ]
            
            for i, strategy in enumerate(likes_strategies):
                try:
                    print(f"Trying likes strategy {i + 1}...")
                    elements = self.driver.find_elements(By.XPATH, strategy)
                    
                    for element in elements:
                        if element.is_displayed():
                            # Try clicking the element directly
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                likes_clicked = True
                                print("Clicked on likes successfully!")
                                time.sleep(5)
                                break
                            except:
                                # If direct click fails, try clicking parent
                                try:
                                    parent = element.find_element(By.XPATH, "..")
                                    self.driver.execute_script("arguments[0].click();", parent)
                                    likes_clicked = True
                                    print("Clicked on likes (parent element)!")
                                    time.sleep(5)
                                    break
                                except:
                                    continue
                    
                    if likes_clicked:
                        break
                        
                except Exception as e:
                    print(f"Strategy {i + 1} failed: {e}")
                    continue
            
            if not likes_clicked:
                print("Could not find or click likes")
                return False
            
            # Wait for likes modal to load and look for follow buttons
            print("Looking for follow buttons...")
            followed_count = 0
            
            # Wait a bit for modal to fully load
            time.sleep(3)
            
            # Try multiple approaches to find follow buttons
            follow_attempts = 0
            max_attempts = 10
            
            while follow_attempts < max_attempts and followed_count < 12:  # Increased to 12 follows per hashtag
                follow_attempts += 1
                print(f"Follow attempt {follow_attempts}...")
                
                # Multiple selectors for follow buttons
                follow_selectors = [
                    "//button[text()='Follow']",
                    "//button[contains(text(), 'Follow')]",
                    "//div[text()='Follow']",
                    "//div[@role='button'][contains(text(), 'Follow')]",
                    "//button[@type='button'][contains(text(), 'Follow')]"
                ]
                
                found_buttons = []
                for selector in follow_selectors:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, selector)
                        for btn in buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                # Make sure it's not already following
                                if "Following" not in btn.text and "Requested" not in btn.text:
                                    found_buttons.append(btn)
                    except:
                        continue
                
                if found_buttons:
                    print(f"Found {len(found_buttons)} follow buttons")
                    
                    # Follow people
                    for button in found_buttons[:3]:  # Max 3 per attempt
                        try:
                            # Get username if possible
                            try:
                                username_elem = button.find_element(By.XPATH, "..//a[contains(@href, '/')]")
                                username = username_elem.get_attribute('href').split('/')[-2]
                            except:
                                username = f"user_{followed_count + 1}"
                            
                            # Click follow button
                            self.driver.execute_script("arguments[0].click();", button)
                            self.follows += 1
                            followed_count += 1
                            print(f"Followed @{username} ({self.follows} total)")
                            
                            # 🎯 IMMEDIATE NOTIFICATION WHEN 200 FOLLOWS REACHED
                            if self.follows == 200:
                                milestone_msg = f"""🎯 MILESTONE ACHIEVED!

✅ 200 FOLLOWERS REACHED!
Comments: {self.comments}/100
Likes: {self.likes}

Bot working perfect and continuing to completion!"""
                                self.send_message_to_ze2ow(milestone_msg)
                                print("🎉 200 FOLLOWS MILESTONE NOTIFICATION SENT!")
                            
                            time.sleep(random.randint(2, 4))
                            
                            if followed_count >= 5:
                                break
                                
                        except Exception as e:
                            print(f"Failed to follow: {e}")
                            continue
                    
                    if followed_count >= 12:  # Updated to match new target
                        break
                else:
                    # Scroll down in modal to find more users
                    try:
                        modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                        self.driver.execute_script("arguments[0].scrollTop += 200;", modal)
                        time.sleep(2)
                        print("Scrolled in modal to find more users...")
                    except:
                        # Try scrolling the page
                        self.driver.execute_script("window.scrollBy(0, 200);")
                        time.sleep(2)
                
                # If no buttons found after several attempts, break
                if follow_attempts > 5 and followed_count == 0:
                    print("No follow buttons found after multiple attempts")
                    break
            
            # Close modal/popup
            try:
                # Try multiple ways to close
                close_methods = [
                    lambda: self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE),
                    lambda: self.driver.find_element(By.XPATH, "//button[@aria-label='Close']").click(),
                    lambda: self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Close')]").click(),
                    lambda: self.driver.execute_script("window.history.back();")
                ]
                
                for method in close_methods:
                    try:
                        method()
                        time.sleep(2)
                        break
                    except:
                        continue
                        
            except:
                pass
            
            print(f"Successfully followed {followed_count} people from #{hashtag}")
            return followed_count > 0
            
        except Exception as e:
            print(f"Follow error: {e}")
            return False
    
    def comment_on_current_post(self):
        """Add emoji comment to current post with multiple attempts"""
        for attempt in range(3):  # Try 3 times
            try:
                print(f"Comment attempt {attempt + 1}...")
                
                # Wait and scroll to make sure comment section is loaded
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                
                # Try to find comment input with multiple selectors
                comment_selectors = [
                    "//textarea[@placeholder='Add a comment...']",
                    "//textarea[@aria-label='Add a comment...']", 
                    "//div[@contenteditable='true'][@aria-label='Add a comment...']",
                    "//textarea[contains(@placeholder, 'comment')]",
                    "//textarea[contains(@aria-label, 'comment')]",
                    "//div[@contenteditable='true'][contains(@aria-label, 'comment')]"
                ]
                
                comment_input = None
                for selector in comment_selectors:
                    try:
                        # Re-find elements to avoid stale references
                        inputs = self.driver.find_elements(By.XPATH, selector)
                        for input_elem in inputs:
                            if input_elem.is_displayed() and input_elem.is_enabled():
                                comment_input = input_elem
                                break
                        if comment_input:
                            break
                    except Exception as selector_error:
                        print(f"Selector failed: {selector_error}")
                        continue
                
                if not comment_input:
                    print(f"❌ Comment attempt {attempt + 1}: Could not find comment input")
                    time.sleep(3)
                    continue
                
                # Select random emoji comment
                comment_text = random.choice(self.emoji_comments)
                
                # Clear and add comment with JavaScript for reliability
                try:
                    # Use JavaScript to focus and clear
                    self.driver.execute_script("arguments[0].focus();", comment_input)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].value = '';", comment_input)
                    time.sleep(1)
                    
                    # Type comment
                    comment_input.send_keys(comment_text)
                    time.sleep(2)
                    
                    # Try to post comment
                    comment_posted = False
                    try:
                        # Find post button
                        post_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Post']")
                        for post_btn in post_buttons:
                            if post_btn.is_displayed() and post_btn.is_enabled():
                                self.driver.execute_script("arguments[0].click();", post_btn)
                                comment_posted = True
                                break
                    except:
                        pass
                    
                    if not comment_posted:
                        # Try Enter key as fallback
                        comment_input.send_keys(Keys.ENTER)
                        comment_posted = True
                    
                    if comment_posted:
                        self.comments += 1
                        print(f"✅ ACTUALLY POSTED COMMENT: '{comment_text}' (Total: {self.comments})")
                        time.sleep(3)
                        return True
                        
                except Exception as comment_error:
                    print(f"Failed to post comment: {comment_error}")
                    time.sleep(2)
                    continue
                    
            except Exception as e:
                print(f"Comment attempt {attempt + 1} error: {e}")
                time.sleep(3)
        
        print("❌ FAILED TO COMMENT after 3 attempts")
        return False

    def like_current_post(self):
        """Like the current post by double-clicking on the image"""
        for attempt in range(3):  # Try 3 times
            try:
                print(f"Like attempt {attempt + 1} - trying double-click method...")
                
                # Wait for page to load
                time.sleep(2)
                
                # Find the post image/video to double-click
                image_selectors = [
                    "//img[contains(@alt, 'Photo')]",  # Photo posts
                    "//video",  # Video posts
                    "//div[contains(@class, '_aagu')]//img",  # Instagram post images
                    "//article//img",  # Images in article
                    "//div[@role='button']//img",  # Clickable images
                    "//img[contains(@style, 'object-fit')]",  # Styled post images
                    "//img[contains(@class, 'x5yr21d')]",  # Instagram image class
                    "//main//img"  # Main content images
                ]
                
                image_found = False
                for selector in image_selectors:
                    try:
                        images = self.driver.find_elements(By.XPATH, selector)
                        for img in images:
                            if img.is_displayed() and img.size['width'] > 200 and img.size['height'] > 200:  # Make sure it's a real post image
                                try:
                                    print(f"Found image: {img.size['width']}x{img.size['height']}")
                                    
                                    # Double-click on the image to like
                                    actions = ActionChains(self.driver)
                                    actions.double_click(img).perform()
                                    
                                    self.likes += 1
                                    print(f"✅ DOUBLE-CLICKED TO LIKE POST (Total: {self.likes})")
                                    time.sleep(3)  # Wait to see if like animation appears
                                    image_found = True
                                    return True
                                    
                                except Exception as click_error:
                                    print(f"Double-click failed: {click_error}")
                                    # Try single click as fallback
                                    try:
                                        actions = ActionChains(self.driver)
                                        actions.click(img).perform()
                                        time.sleep(0.5)
                                        actions.click(img).perform()  # Two quick clicks
                                        
                                        self.likes += 1
                                        print(f"✅ TWO-CLICK TO LIKE POST (Total: {self.likes})")
                                        time.sleep(2)
                                        image_found = True
                                        return True
                                    except:
                                        continue
                        
                        if image_found:
                            break
                            
                    except Exception as selector_error:
                        print(f"Selector {selector} failed: {selector_error}")
                        continue
                
                if image_found:
                    return True
                else:
                    print(f"❌ Like attempt {attempt + 1}: Could not find post image to double-click")
                    # Try to scroll up to find the image
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Like attempt {attempt + 1} error: {e}")
                time.sleep(2)
        
        print("❌ FAILED TO LIKE POST after 3 attempts")
        return False
    
    def unfollow_followers(self):
        """Unfollow people who have followed you back"""
        try:
            print("🔄 Cleaning up: Unfollowing people who followed back...")
            
            # Go to your profile
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Click on profile icon
            try:
                profile_selectors = [
                    "//img[@alt='Your avatar']",
                    "//a[contains(@href, '/accounts/')]//img",
                    "//*[contains(@data-testid, 'user-avatar')]",
                    "//span[contains(@class, 'x1rg5ohu')]//img"  # Profile image
                ]
                
                profile_clicked = False
                for selector in profile_selectors:
                    try:
                        profile_img = self.driver.find_element(By.XPATH, selector)
                        if profile_img.is_displayed():
                            profile_img.click()
                            profile_clicked = True
                            break
                    except:
                        continue
                
                if not profile_clicked:
                    print("Could not find profile icon")
                    return False
                    
            except Exception as e:
                print(f"Failed to click profile: {e}")
                return False
            
            time.sleep(4)
            
            # Click on Following count
            try:
                following_selectors = [
                    "//a[contains(@href, '/following/')]",
                    "//span[contains(text(), 'following')]//parent::a",
                    "//div[contains(text(), 'following')]//parent::a"
                ]
                
                following_clicked = False
                for selector in following_selectors:
                    try:
                        following_link = self.driver.find_element(By.XPATH, selector)
                        if following_link.is_displayed():
                            following_link.click()
                            following_clicked = True
                            break
                    except:
                        continue
                
                if not following_clicked:
                    print("Could not find following link")
                    return False
                    
            except Exception as e:
                print(f"Failed to click following: {e}")
                return False
            
            time.sleep(5)
            
            # Now we're in the following list - look for "Following" buttons to unfollow
            unfollowed_count = 0
            max_unfollows = 20  # Unfollow up to 20 people per cleanup
            
            for attempt in range(10):  # Try multiple scrolls
                print(f"Cleanup attempt {attempt + 1}...")
                
                # Find Following buttons (people who followed back)
                following_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Following']")
                
                if following_buttons:
                    print(f"Found {len(following_buttons)} people who followed back")
                    
                    # Unfollow some of them
                    for button in following_buttons[:3]:  # Max 3 per scroll
                        try:
                            if unfollowed_count >= max_unfollows:
                                break
                                
                            # Get username if possible
                            try:
                                username_elem = button.find_element(By.XPATH, "..//a[contains(@href, '/')]")
                                username = username_elem.get_attribute('href').split('/')[-2]
                            except:
                                username = f"user_{unfollowed_count + 1}"
                            
                            # Click Following button to unfollow
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(2)
                            
                            # Confirm unfollow if popup appears
                            try:
                                unfollow_confirm = self.driver.find_element(By.XPATH, "//button[text()='Unfollow']")
                                unfollow_confirm.click()
                                unfollowed_count += 1
                                print(f"✅ Unfollowed @{username} (Total: {unfollowed_count})")
                                time.sleep(random.randint(2, 4))
                            except:
                                # No confirmation popup, already unfollowed
                                unfollowed_count += 1
                                print(f"✅ Unfollowed @{username} (Total: {unfollowed_count})")
                                time.sleep(random.randint(2, 4))
                                
                        except Exception as e:
                            print(f"Failed to unfollow: {e}")
                            continue
                    
                    if unfollowed_count >= max_unfollows:
                        break
                else:
                    print("No mutual followers found to unfollow")
                
                # Scroll down to find more
                try:
                    modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                    self.driver.execute_script("arguments[0].scrollTop += 300;", modal)
                    time.sleep(3)
                except:
                    # Try page scroll
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(3)
                
                # Break if no more Following buttons after several attempts
                if attempt > 5 and unfollowed_count == 0:
                    print("No mutual followers found after multiple attempts")
                    break
            
            # Close modal
            try:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(2)
            except:
                pass
            
            print(f"✅ Cleanup complete: Unfollowed {unfollowed_count} mutual followers")
            return unfollowed_count > 0
            
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
    
    def run(self):
        """Run the bot with 6-hour targets: 200 follows, 100 comments, lots of likes"""
        print("🚀 ADVANCED INSTAGRAM BOT - 6 HOUR SESSION")
        print("=" * 50)
        print("🎯 TARGETS: 200 Follows | 100 Comments | Unlimited Likes")
        print("⏱️ Duration: 6 Hours")
        
        # Session targets
        target_follows = 200
        target_comments = 100
        session_start = datetime.now()
        
        try:
            # Setup
            print("🔧 Setting up browser...")
            if not self.setup_browser():
                return
            print("🔐 Logging into Instagram...")
            if not self.load_cookies():
                return
            
            # Send working message
            working_msg = f"""ADVANCED BOT STARTED!

6-Hour Session Targets:
200 Follows from Kurdish hashtags
100 Comments with emojis  
Unlimited Likes
🧹 Auto-cleanup: Unfollow mutual followers

Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Bot is working perfectly!"""
            
            print("📱 Sending startup message...")
            self.send_message_to_ze2ow(working_msg)
            
            # Extended hashtag list for more variety
            hashtags = [
                "kurdish", "kurd", "kurdistan", "rojava", "hawler", "erbil",
                "sulaimani", "duhok", "zakho", "kirkuk", "newroz", "peshmerga",
                "fitness", "gym", "workout", "bodybuilding", "strong", "muscle"
            ]
            
            print(f"\n🚀 Starting 6-hour session...")
            print(f"📊 Progress will be updated every 30 minutes")
            
            # Main 6-hour loop
            session_minutes = 0
            max_session_minutes = 360  # 6 hours
            cleanup_counter = 0  # Track when to do cleanup
            
            while session_minutes < max_session_minutes:
                if self.follows >= target_follows and self.comments >= target_comments:
                    print("🎉 All targets achieved early!")
                    break
                
                # Every 60 minutes, do a cleanup (unfollow people who followed back)
                if cleanup_counter % 4 == 0 and cleanup_counter > 0:  # Every 4 rounds = ~60 minutes
                    print("\n🧹 TIME FOR CLEANUP!")
                    self.unfollow_followers()
                    print("🧹 Cleanup finished, back to following...\n")
                
                # Select random hashtag
                hashtag = random.choice(hashtags)
                print(f"\n📍 Round {session_minutes//10 + 1} - Working on #{hashtag}")
                print(f"📊 Progress: {self.follows}/{target_follows} follows | {self.comments}/{target_comments} comments | {self.likes} likes")
                
                # Work on hashtag
                success = self.follow_from_hashtag(hashtag)
                
                if success:
                    print(f"✅ Completed round with #{hashtag}")
                else:
                    print(f"⚠️ Issues with #{hashtag}, trying next...")
                
                cleanup_counter += 1
                
                # Progress report every 30 minutes
                if session_minutes % 30 == 0 and session_minutes > 0:
                    elapsed = datetime.now() - session_start
                    progress_msg = f"""30-MIN PROGRESS REPORT

Session Time: {elapsed}
Follows: {self.follows}/{target_follows} ({(self.follows/target_follows)*100:.1f}%)
Comments: {self.comments}/{target_comments} ({(self.comments/target_comments)*100:.1f}%)
Likes: {self.likes}

Bot working perfectly! Next update in 30 min."""

                    self.send_message_to_ze2ow(progress_msg)
                    print("📱 Progress report sent!")
                
                # Smart delay between hashtags (avoid detection)
                delay = random.randint(45, 90)  # 45-90 seconds
                print(f"⏸️ Waiting {delay} seconds before next hashtag...")
                time.sleep(delay)
                session_minutes += delay // 60
            
            # Final cleanup before session ends
            print("\n🧹 FINAL CLEANUP: Removing mutual followers...")
            final_cleanup = self.unfollow_followers()
            if final_cleanup:
                print("✅ Final cleanup completed!")
            
            # Final session report
            total_time = datetime.now() - session_start
            completion_msg = f"""6-HOUR SESSION COMPLETED!

FINAL RESULTS:
Total Follows: {self.follows}/{target_follows}
Total Comments: {self.comments}/{target_comments}  
Total Likes: {self.likes}
Session Duration: {total_time}

Success Rate:
- Follows: {(self.follows/target_follows)*100:.1f}%
- Comments: {(self.comments/target_comments)*100:.1f}%

Bot performed excellently! Ready for next session"""

            print("\n📱 Sending final report...")
            self.send_message_to_ze2ow(completion_msg)
            
            print(f"\n🎉 SESSION COMPLETE!")
            print(f"📊 Final Stats:")
            print(f"   👥 Follows: {self.follows}/{target_follows}")
            print(f"   💬 Comments: {self.comments}/{target_comments}")
            print(f"   ❤️ Likes: {self.likes}")
            print(f"   ⏱️ Duration: {total_time}")
            
        except Exception as e:
            print(f"❌ Bot error: {e}")
            try:
                error_msg = f"❌ Bot error occurred!\n\nError: {str(e)[:200]}\nTime: {datetime.now().strftime('%H:%M:%S')}\n\nStats: {self.follows} follows, {self.comments} comments, {self.likes} likes"
                self.send_message_to_ze2ow(error_msg)
            except:
                pass
        
        finally:
            if self.driver:
                print("\n⏸️ Session finished. Press Enter to close browser...")
                input()
                self.driver.quit()
                print("✅ Browser closed. Great work! 👋")

if __name__ == "__main__":
    # Check cookies
    if not os.path.exists("cookies.txt"):
        print("ERROR: cookies.txt not found!")
        print("Please add your Instagram cookies to cookies.txt file")
        input("Press Enter to exit...")
        exit()
    
    # Run bot
    bot = SimpleBot()
    bot.run()
