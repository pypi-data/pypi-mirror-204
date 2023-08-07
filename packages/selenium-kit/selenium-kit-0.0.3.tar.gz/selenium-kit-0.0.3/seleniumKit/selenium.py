from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:
    def __init__(self, headless="--headless") -> None:
        chrome_options = webdriver.ChromeOptions()
        if headless == "--headless":
            chrome_options.add_argument(headless)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def callURL(self, url: str) -> None:
        self.driver.get(url)

    def elementByXPath(self, xpath: str) -> webdriver:
        return self.driver.find_element(By.XPATH, f"//{xpath}")

    def elementsByXPath(self, xpath: str) -> webdriver:
        return self.driver.find_elements(By.XPATH, f"//{xpath}")

    def sendKeys(self, element: webdriver, value: str) -> None:
        element.send_keys(value)

    def clickOnElement(self, element: webdriver) -> None:
        element.click()

    def textFromElement(self, element: webdriver) -> str:
        return element.text

    def __del__(self):
        self.driver.quit()
