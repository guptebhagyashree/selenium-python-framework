import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
import time

class RegisterCoursesPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _search_box = "search-courses"
    _search_icon = "search-course-button"
    _course = "//div[contains(@class,'course-listing-title') and contains(text(),'{0}')]"
    _all_courses = "//div[@class='course-listing-title']"
    _enroll_button = "enroll-button-top"
    _postal_code_field = "billingPostalCode"
    _buy_now_button = "//div[@id='react-checkout']//div[@class='m-b-4-xs _3pM7B']//span[1]"
    _error_message = "//li[contains(text(),'Sorry, there was an error completing your purchase -- please try again.')]"


    # Element interactions
    def enterCourseName(self, name):
        self.sendKeys(name, locator=self._search_box)
        self.clickElement(locator=self._search_icon)

    def selectCourseToEnroll(self, fullCourseName):
        self.clickElement(locator=self._course.format(fullCourseName), locatorType="xpath")

    def clickOnEnrollButton(self):
        self.clickElement(locator=self._enroll_button)

    def enterPostalCode(self, code):
        self.sendKeys(code, locator=self._postal_code_field)

    def clickBuyNowButton(self):
        self.clickElement(locator=self._buy_now_button, locatorType="xpath")

    def enrollCourse(self, code=""):
        self.clickOnEnrollButton()
        self.webScroll(direction="down")
        self.enterPostalCode(code)
        self.clickBuyNowButton()
        time.sleep(5)
        self.webScroll(direction="up")

    def verifyEnrollFailed(self):
        messageElement = self.waitForElement(self._error_message, locatorType="xpath")
        result = self.isElementDisplayed(element=messageElement)
        return result










