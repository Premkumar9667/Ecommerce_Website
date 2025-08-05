from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time

# ✅ Edge WebDriver is usually installed automatically with Windows
# If not, download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
EDGE_DRIVER_PATH = r"msedgedriver.exe"  # Usually in PATH, or provide full path

# ✅ Phone number format: "countrycode+number" (no + symbol)
phone_number = "6369472647"

# ✅ Message to send
message = "Hello from Selenium automation!"

def create_edge_driver():
    """Create Edge driver with stable options"""
    options = Options()
    
    # Add options to prevent crashes
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Disable notifications
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    
    try:
        # Try with explicit service path first
        return webdriver.Edge(service=Service(EDGE_DRIVER_PATH), options=options)
    except:
        # If that fails, try without service (using system PATH)
        return webdriver.Edge(options=options)

try:
    print("🔄 Starting Edge driver...")
    driver = create_edge_driver()
    
    print("✅ Edge driver created successfully!")
    
    # ✅ Open WhatsApp Web
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    print(f"🔄 Opening: {url}")
    driver.get(url)

    print("🔄 Waiting for WhatsApp Web to load...")
    print("📱 Please scan the QR code if prompted...")
    
    # Wait for page to load
    time.sleep(10)
    
    # Wait for message input box with multiple selectors
    print("🔄 Looking for message input box...")
    
    input_selectors = [
        "//div[@contenteditable='true'][@data-tab='10']",
        "//div[@contenteditable='true'][@role='textbox']",
        "//div[@contenteditable='true']"
    ]
    
    input_box = None
    for selector in input_selectors:
        try:
            print(f"🔍 Trying selector: {selector}")
            input_box = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"✅ Found input box!")
            break
        except:
            continue
    
    if input_box is None:
        print("❌ Could not find message input box")
        print("💡 Make sure you've scanned QR code and WhatsApp is fully loaded")
        raise Exception("Input box not found")
    
    # Send the message
    print("🔄 Sending message...")
    input_box.click()
    time.sleep(2)
    
    # The message should be pre-filled, just press Enter
    input_box.send_keys(Keys.ENTER)
    
    print("✅ Message sent successfully!")
    time.sleep(5)

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Edge WebDriver troubleshooting:")
    print("1. Make sure Microsoft Edge browser is installed")
    print("2. Edge WebDriver is usually installed automatically")
    print("3. If not, download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    print("4. Make sure you scan the QR code when prompted")

finally:
    if 'driver' in locals():
        print("🔄 Cleaning up...")
        time.sleep(5)
        driver.quit()
    print("✅ Done!")