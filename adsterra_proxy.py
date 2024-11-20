import asyncio
import random
import time
import uuid
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Read proxies and Adsterra links
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Setup Selenium WebDriver with proxy
def setup_driver(proxy_url):
    ua = UserAgent()
    user_agent = ua.random

    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={proxy_url}")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")  # Run browser in headless mode for performance
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Mimic human-like interactions
def mimic_human_behavior(driver):
    action = ActionChains(driver)
    for _ in range(random.randint(5, 10)):
        x_offset = random.randint(-200, 200)
        y_offset = random.randint(-200, 200)
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.1, 0.5))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 5))

# Visit Adsterra link
async def visit_adsterra(driver, link):
    try:
        logger.info(f"Visiting: {link}")
        driver.get(link)
        time.sleep(random.uniform(5, 10))  # Let the page load
        mimic_human_behavior(driver)
        page_title = driver.title
        logger.info(f"Visited: {link}, Title: {page_title}")
    except Exception as e:
        logger.error(f"Error visiting {link}: {e}")

# Main task to handle proxy rotation
async def handle_proxy(proxy_url, adsterra_links, visit_count):
    driver = setup_driver(proxy_url)
    try:
        for _ in range(visit_count):
            link = random.choice(adsterra_links)
            await visit_adsterra(driver, link)
    finally:
        driver.quit()

# Main function
async def main():
    proxy_file = "proxy.txt"
    links_file = "adsterra_links.txt"

    proxies = read_file(proxy_file)
    adsterra_links = read_file(links_file)

    visit_count_per_proxy = 10  # Adjust as needed
    tasks = []

    for proxy_url in proxies:
        tasks.append(asyncio.create_task(handle_proxy(proxy_url, adsterra_links, visit_count_per_proxy)))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
