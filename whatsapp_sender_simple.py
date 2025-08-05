from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# ✅ Set path to your chromedriver.exe correctly
CHROME_DRIVER_PATH = r"C:\Users\dhili\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# ✅ Phone number format: "countrycode+number" (no + symbol)
phone_number = "6369472647"  # Example: "6369472647"

# ✅ Message to send
message = "Hello from Selenium automation!"

# ✅ Set up Chrome driver with minimal options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9223")

# Disable notifications
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

try:
    print("🔄 Starting Chrome driver...")
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    
    # ✅ Open WhatsApp Web
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    print(f"🔄 Opening: {url}")
    driver.get(url)

    print("🔄 Waiting for WhatsApp Web to load...")
    print("📱 Please scan the QR code and wait for the chat to open...")
    
    # Wait for the message input box to appear (this means WhatsApp is loaded and logged in)
    print("🔄 Waiting for message input box...")
    input_box = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
    )
    
    print("✅ Message input box found!")
    
    # Click on the input box and send message
    input_box.click()
    time.sleep(2)
    
    # The message should already be pre-filled, just press Enter
    input_box.send_keys(Keys.ENTER)
    
    print("✅ Message sent successfully!")
    time.sleep(5)

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure ChromeDriver path is correct")
    print("2. Close any existing Chrome windows")
    print("3. Scan the QR code when prompted")
    print("4. Wait for WhatsApp Web to fully load")

finally:
    print("🔄 Keeping browser open for 10 seconds...")
    time.sleep(10)
    if 'driver' in locals():
        driver.quit()
    print("✅ Done!")