import utilities.custom_logger as cl
import logging
from base.basepage import BasePage

class NavigationPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _my_courses = "My Courses"
    _all_courses = "All Courses"
    _practice = "Practice"
    _user_icon = "//img[@class='gravatar']"
    _website_logo = "//a[@class='navbar-brand header-logo']"

    def navigateToMyCourses(self):
        self.clickElement(locator=self._my_courses, locatorType="link")

    def navigateToAllCourses(self):
        self.clickElement(locator=self._all_courses, locatorType="link")

    def navigateToPractice(self):
        self.clickElement(locator=self._practice, locatorType="link")

    def navigateToUserIcon(self):
        userIconElement = self.waitForElement(locator=self._user_icon, locatorType="xpath", pollfrequency=1)
        self.clickElement(element=userIconElement)

    def navigateToWebsiteLogo(self):
        self.clickElement(locator=self._website_logo, locatorType="xpath")
