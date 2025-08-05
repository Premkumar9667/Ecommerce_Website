from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

# ✅ Download Firefox GeckoDriver from: https://github.com/mozilla/geckodriver/releases
# Put the path to geckodriver.exe here
GECKO_DRIVER_PATH = r"C:\Users\dhili\Downloads\geckodriver.exe"  # Update this path

# ✅ Phone number format: "countrycode+number" (no + symbol)
phone_number = "6369472647"

# ✅ Message to send
message = "Hello from Selenium automation!"

# ✅ Set up Firefox driver
options = Options()
# options.add_argument("--headless")  # Uncomment to run in background

try:
    print("🔄 Starting Firefox driver...")
    driver = webdriver.Firefox(service=Service(GECKO_DRIVER_PATH), options=options)
    
    # ✅ Open WhatsApp Web
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
    print(f"🔄 Opening: {url}")
    driver.get(url)

    print("🔄 Waiting for WhatsApp Web to load...")
    print("📱 Please scan the QR code if prompted...")
    
    # Wait for message input box
    print("🔄 Waiting for message input box...")
    input_box = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true']"))
    )
    
    print("✅ Message input box found!")
    
    # Send the message
    input_box.click()
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    
    print("✅ Message sent successfully!")
    time.sleep(5)

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 To use Firefox version:")
    print("1. Download GeckoDriver from: https://github.com/mozilla/geckodriver/releases")
    print("2. Extract geckodriver.exe and update GECKO_DRIVER_PATH in the script")
    print("3. Make sure Firefox browser is installed")

finally:
    if 'driver' in locals():
        print("🔄 Cleaning up...")
        time.sleep(5)
        driver.quit()
    print("✅ Done!")