"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
from selenium import webdriver
import os

class WebDriverFactory():

    def __init__(self, browser):
        """
        Inits WebDriverFactory class

        Returns:
            None
        """
        self.browser = browser
    """
        Set chrome driver and iexplorer environment based on OS

        chromedriver = "C:/.../chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        PREFERRED: Set the path on the machine where browser will be executed
    """

    def getWebDriverInstance(self):
        """
       Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        opt = webdriver.ChromeOptions()
        opt.add_argument("user-data-dir=C:\\Users\\Dhanshree\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        baseURL = "https://letskodeit.teachable.com/"
        if self.browser == "chrome":
            # Set chrome driver
            driver = webdriver.Chrome(options=opt)
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "ie":
            # Set ie driver
            driver = webdriver.Ie()
        else:
            driver = webdriver.Chrome(options=opt)
        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(10)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with App URL
        driver.get(baseURL)
        return driver