from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# ✅ Set path to your chromedriver.exe correctly
CHROME_DRIVER_PATH = r"C:\Users\dhili\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# ✅ Phone number format: "countrycode+number" (no + symbol)
phone_number = "6369472647"  # Example: "6369472647" for India without country code

# ✅ Message to send
message = "Hello from Selenium automation!"

def setup_chrome_driver():
    """Set up Chrome driver with proper options to avoid crashes"""
    options = Options()
    
    # Create a separate profile directory for automation
    profile_dir = os.path.join(os.path.expanduser("~"), "selenium_chrome_profile")
    
    # Chrome options to prevent crashes
    options.add_argument(f"--user-data-dir={profile_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Keep the browser open for manual QR code scanning if needed
    options.add_experimental_option("detach", True)
    
    # Disable notifications
    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    return webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

def send_whatsapp_message():
    """Send WhatsApp message using Selenium"""
    driver = None
    try:
        print("🔄 Setting up Chrome driver...")
        driver = setup_chrome_driver()
        
        # ✅ Open WhatsApp Web with pre-filled message
        url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        print(f"🔄 Opening WhatsApp Web: {url}")
        driver.get(url)
        
        print("🔄 Waiting for WhatsApp Web to load...")
        print("📱 Please scan the QR code if prompted and wait for WhatsApp to load completely...")
        
        # Wait for WhatsApp to load - look for either the menu or chat interface
        try:
            # Wait for either the main menu (if logged in) or QR code (if not logged in)
            WebDriverWait(driver, 120).until(
                lambda d: d.find_element(By.XPATH, "//div[@title='Menu']") or 
                         d.find_element(By.XPATH, "//canvas[@aria-label='Scan me!']") or
                         d.find_element(By.XPATH, "//div[@contenteditable='true']")
            )
            print("✅ WhatsApp Web loaded successfully!")
        except:
            print("⚠️ WhatsApp Web took longer than expected to load, continuing anyway...")
        
        # Wait a bit more for the page to stabilize
        time.sleep(3)
        
        # ✅ Wait for the message input box and send the message
        print("🔄 Looking for message input box...")
        
        # Multiple possible XPaths for the message input box
        input_box_xpaths = [
            "//div[@contenteditable='true'][@data-tab='10']",
            "//div[@contenteditable='true'][contains(@class, 'to2l77zo')]",
            "//div[@contenteditable='true'][@role='textbox']",
            "//div[@contenteditable='true' and @aria-label]"
        ]
        
        input_box = None
        for xpath in input_box_xpaths:
            try:
                input_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                print(f"✅ Found message input box with xpath: {xpath}")
                break
            except:
                continue
        
        if input_box is None:
            print("❌ Could not find message input box. Make sure you're logged into WhatsApp Web.")
            return False
        
        # Click on the input box and send the message
        input_box.click()
        time.sleep(1)
        
        # Clear any existing text and type the new message
        input_box.clear()
        input_box.send_keys(message)
        time.sleep(1)
        
        # Send the message
        input_box.send_keys(Keys.ENTER)
        
        print("✅ Message sent successfully!")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("💡 Make sure:")
        print("   1. ChromeDriver path is correct")
        print("   2. You're logged into WhatsApp Web")
        print("   3. The phone number is valid")
        print("   4. You have internet connection")
        return False
        
    finally:
        if driver:
            print("🔄 Keeping browser open for 10 seconds...")
            time.sleep(10)
            driver.quit()
            print("✅ Browser closed.")

if __name__ == "__main__":
    print("🚀 Starting WhatsApp automation...")
    success = send_whatsapp_message()
    if success:
        print("🎉 WhatsApp message automation completed successfully!")
    else:
        print("😞 WhatsApp message automation failed.")