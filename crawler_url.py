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

def initialize_webdriver(driver_path):
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_post_text(driver):
    """Extract the post text using the meta description."""
    try:
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        meta_description = wait.until(EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']")))
        post_text = meta_description.get_attribute('content')
        return post_text
    except Exception as e:
        print("Could not find post text:", e)
        return None

def extract_image_urls(driver):
    """Extract image URLs from the post."""
    try:
        # Scroll to the bottom to ensure lazy-loaded images are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for images to load
        images = driver.find_elements(By.TAG_NAME, 'img')
        image_urls = [img.get_attribute('src') for img in images if 'scontent' in img.get_attribute('src')]
        print("getImageURLs:", image_urls)
        return image_urls
    except Exception as e:
        print("Could not find images:", e)
        return []

def download_images(image_urls, post_id):
    """Download images to the output folder with the specified naming convention."""
    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)
    for index, img_url in enumerate(image_urls):
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Raise an error for bad responses
            # Save image with a unique name format: image{post_id}_{image_index}.png
            image_path = os.path.join(output_folder, f'image{post_id}_{index+1}.png')
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f'Downloaded {image_path}')
        except Exception as e:
            print(f'Failed to download image from {img_url}: {e}')

def process_urls(file_path):
    """Read URLs from file and process each to extract text and images."""
    driver = initialize_webdriver(driver_path)
    post_texts = []

    with open(file_path, 'r') as url_file:
        urls = url_file.readlines()

    for i, url in enumerate(urls, start=1):
        url = url.strip()  # Remove leading/trailing whitespace
        print(f'Processing URL {i}: {url}')
        driver.get(url)
        time.sleep(5)  # Wait for the page to load fully
        
        # Extract post text
        post_text = extract_post_text(driver)
        if post_text:
            post_texts.append(f'id:{i}\ndescription:"{post_text}"\n')

        # Extract and download images
        image_urls = extract_image_urls(driver)
        download_images(image_urls, i)

    # Save post texts to a file
    with open('post_text.txt', 'w') as text_file:
        text_file.writelines(post_texts)

    driver.quit()

# Run the process with the URL file
process_urls('url.txt')
