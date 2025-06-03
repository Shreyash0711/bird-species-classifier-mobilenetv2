import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from io import BytesIO

def download_unsplash_images(keyword: str, total: int = 100):
    folder = f"{keyword.replace(' ', '_')}_images"
    os.makedirs(folder, exist_ok=True)
    driver = webdriver.Chrome()
    driver.get(f"https://unsplash.com/s/photos/{keyword.replace(' ', '-')}")
    time.sleep(3)

    image_urls = set()
    attempts = 0

    while len(image_urls) < total and attempts < 30:
        attempts += 1
        try:
            load_more = driver.find_element(By.CSS_SELECTOR,
                'button.WfcG4.WybTA.yoWgy.DimJM.ae8ZH.y9IO6.VyUnB.BCGzd.pYP1f')
            driver.execute_script("arguments[0].click();", load_more)
            print(f"[{keyword}] ✅ Clicked 'Load more' (attempt #{attempts})")
        except NoSuchElementException:
            print(f"[{keyword}] ⚠️ 'Load more' not found (attempt #{attempts})")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        imgs = driver.find_elements(By.CSS_SELECTOR, "img[srcset]")
        new = 0
        for img in imgs:
            if "KD8Jx" in img.get_attribute("class"):
                continue
            srcset = img.get_attribute("srcset")
            if srcset:
                url = srcset.strip().split(",")[-1].split()[0]
                if url not in image_urls:
                    image_urls.add(url)
                    new += 1
                    if len(image_urls) >= total:
                        break

        print(f"[{keyword}] 🔄 Collected {len(image_urls)} / {total} URLs, +{new} new")

        if new == 0:
            time.sleep(2)  # Extra wait, maybe page is slow

    print(f"[{keyword}] 📦 Downloading {len(image_urls)} images...")

    for i, url in enumerate(image_urls, start=1):
        try:
            resp = requests.get(url, timeout=10)
            img = Image.open(BytesIO(resp.content))
            img.save(os.path.join(folder, f"{keyword.replace(' ', '_').lower()}_{i}.jpg"))
            print(f"[{keyword}] 📥 Saved {keyword.replace(' ', '_').lower()}_{i}.jpg")
        except Exception as e:
            print(f"[{keyword}] ❌ Error saving {keyword.replace(' ', '_').lower()}_{i}.jpg — {e}")

    driver.quit()

# Example usage:
download_unsplash_images("King penguin", total=100)
