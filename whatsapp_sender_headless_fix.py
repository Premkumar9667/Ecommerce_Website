from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import tempfile
import os

# ✅ Set path to your chromedriver.exe correctly
CHROME_DRIVER_PATH = r"C:\Users\dhili\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# ✅ Phone number format: "countrycode+number" (no + symbol)
phone_number = "6369472647"

# ✅ Message to send
message = "Hello from Selenium automation!"

def create_chrome_driver():
    """Create Chrome driver with isolated profile"""
    options = Options()
    
    # Create a temporary directory for this session
    temp_dir = tempfile.mkdtemp()
    
    # Essential Chrome options to prevent crashes
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=0")  # Use random port
    
    # Window size
    options.add_argument("--window-size=1200,800")
    
    # Disable notifications and other popups
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.media_stream": 2,
        "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    # Disable logging
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    
    return webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

try:
    print("🔄 Creating Chrome driver with isolated profile...")
    driver = create_chrome_driver()
    
    print("✅ Chrome driver created successfully!")
    
    # Open WhatsApp Web
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    print(f"🔄 Opening: {url}")
    driver.get(url)
    
    print("🔄 Waiting for WhatsApp Web to load...")
    print("📱 Please scan the QR code if prompted...")
    
    # Wait for page to load - try multiple indicators
    page_loaded = False
    for attempt in range(3):
        try:
            # Wait for any of these elements to appear
            WebDriverWait(driver, 30).until(
                lambda d: (
                    len(d.find_elements(By.XPATH, "//canvas[@aria-label='Scan me!']")) > 0 or  # QR code
                    len(d.find_elements(By.XPATH, "//div[@title='Menu']")) > 0 or  # Main menu
                    len(d.find_elements(By.XPATH, "//div[@contenteditable='true']")) > 0  # Message box
                )
            )
            page_loaded = True
            print("✅ WhatsApp Web loaded!")
            break
        except:
            print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
            time.sleep(5)
    
    if not page_loaded:
        print("❌ WhatsApp Web failed to load properly")
        raise Exception("Page load timeout")
    
    # Wait a bit more for everything to stabilize
    time.sleep(5)
    
    # Look for message input box with multiple attempts
    print("🔄 Looking for message input box...")
    
    input_box = None
    input_selectors = [
        "//div[@contenteditable='true'][@data-tab='10']",
        "//div[@contenteditable='true'][@role='textbox']",
        "//div[@contenteditable='true'][contains(@title, 'message')]",
        "//div[@contenteditable='true' and contains(@class, 'to2l77zo')]",
        "//div[@contenteditable='true']"
    ]
    
    for selector in input_selectors:
        try:
            print(f"🔍 Trying selector: {selector}")
            input_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"✅ Found input box with selector: {selector}")
            break
        except:
            print(f"❌ Selector failed: {selector}")
            continue
    
    if input_box is None:
        print("❌ Could not find message input box")
        print("💡 Make sure you've scanned the QR code and WhatsApp Web is fully loaded")
        # Take a screenshot for debugging
        driver.save_screenshot("debug_screenshot.png")
        print("📸 Screenshot saved as debug_screenshot.png")
        raise Exception("Message input box not found")
    
    # Send the message
    print("🔄 Sending message...")
    input_box.click()
    time.sleep(2)
    
    # Clear any existing text and send new message
    input_box.clear()
    input_box.send_keys(message)
    time.sleep(1)
    input_box.send_keys(Keys.ENTER)
    
    print("✅ Message sent successfully!")
    time.sleep(3)

except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure Chrome is completely closed before running")
    print("2. Check if ChromeDriver version matches your Chrome browser")
    print("3. Run as administrator if needed")
    print("4. Disable antivirus temporarily")
    print("5. Try restarting your computer")

finally:
    if 'driver' in locals():
        print("🔄 Cleaning up...")
        time.sleep(5)
        driver.quit()
        print("✅ Browser closed.")