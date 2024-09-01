from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Set up Selenium WebDriver with a Service object
driver_path = '/usr/local/bin/chromedriver'  # Update this with your WebDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# URL of the Facebook post
url = 'https://m.facebook.com/story.php?story_fbid=pfbid0rQKqu3Dz7TfTFPEcpbrpsZt4vkrh4X7HYdwQGN7FceQyt8VgmbJvV8xBE1UkhuFTl&id=100057278327259'

# Open the Facebook post
driver.get(url)

# Wait for the page to load (adjust time as necessary)
time.sleep(5)

# Attempt to extract the post text (optional)
try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    # Locate the meta tag with the post content using its property 'og:description'
    meta_description = wait.until(EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']")))
    post_text = meta_description.get_attribute('content')
    print("Post Text:")
    print(post_text)
except Exception as e:
    print("Could not find post text:", e)

# Extract images
try:
    images = driver.find_elements(By.TAG_NAME, 'img')
    image_urls = [img.get_attribute('src') for img in images if 'scontent' in img.get_attribute('src')]
    print("\nImage URLs:")
    for img_url in image_urls:
        print(img_url)
except Exception as e:
    print("Could not find images:", e)

# Close the driver
driver.quit()

# Create an output folder if it doesn't exist
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# Download the images to the output folder
for index, img_url in enumerate(image_urls):
    try:
        response = requests.get(img_url)
        response.raise_for_status()  # Raise an error for bad responses
        # Save image with a unique name
        with open(os.path.join(output_folder, f'image_{index+1}.jpg'), 'wb') as file:
            file.write(response.content)
        print(f'Downloaded image_{index+1}.jpg')
    except Exception as e:
        print(f'Failed to download image from {img_url}: {e}')
