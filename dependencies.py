from asyncio import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


async def connect_driver(docker: bool = False):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    if docker:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability("browserVersion", "98")
        # driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        driver = webdriver.Remote(
            options=options,
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
    else:
        driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/bin/chromedriver')
    return driver


async def get_user_photos(username: str, max_count: int) -> list:
    driver = await connect_driver()
    driver.get(f"https://www.instagram.com/{username}/")
    await sleep(1)
    photos = []
    elements = driver.find_elements(By.XPATH, '//div[@class="_aabd _aa8k  _al3l"]')
    for element in elements:
        link = element.find_element(By.XPATH, './/a[@role="link"]').get_attribute('href')
        if link not in photos:
            photos.append(link)
            if len(photos) == max_count:
                break
    driver.quit()
    return photos
