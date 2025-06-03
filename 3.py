#https://unsplash.com/s/photos/Peacock
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from io import BytesIO

# Setup download folder
os.makedirs("Peacock_images", exist_ok=True)

driver = webdriver.Chrome()
driver.get("https://unsplash.com/s/photos/Peacock")
time.sleep(3)

image_urls = set()

def click_load_more():
    try:
        load_more = driver.find_element(By.CSS_SELECTOR, 'button.WfcG4.WybTA.yoWgy.DimJM.ae8ZH.y9IO6.VyUnB.BCGzd.pYP1f')
        driver.execute_script("arguments[0].click();", load_more)
        print("✅ Clicked 'Load more'")
        return True
    except NoSuchElementException:
        return False

# Loop until we get 100 images
while len(image_urls) < 100:
    click_load_more()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    imgs = driver.find_elements(By.CSS_SELECTOR, "img[srcset]")

    for img in imgs:
        if "KD8Jx" in img.get_attribute("class"):
            continue  # Skip profile/user pics
        srcset = img.get_attribute("srcset")
        if srcset:
            largest = srcset.strip().split(",")[-1].split()[0]
            image_urls.add(largest)
        if len(image_urls) >= 100:
            break

    print(f"🔄 Collected {len(image_urls)} image URLs...")

# Download images
for i, url in enumerate(image_urls):
    try:
        response = requests.get(url, timeout=10)
        image = Image.open(BytesIO(response.content))
        image.save(f"Peacock_images/Peacock_{i+1}.jpg")
        print(f"📥 Saved Peacock_{i+1}.jpg")
    except Exception as e:
        print(f"❌ Error downloading image {i+1}: {e}")

driver.quit()
