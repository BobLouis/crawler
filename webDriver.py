from selenium import webdriver

# Initialize WebDriver (No need to specify path if in /usr/local/bin)
driver = webdriver.Chrome()

# Open a webpage to test (e.g., Google)
driver.get("https://www.google.com")

# Print page title to verify it's working
print(driver.title)

# Close the browser
driver.quit()
