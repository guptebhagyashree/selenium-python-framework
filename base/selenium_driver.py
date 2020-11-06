from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
import logging
import os
import time
import traceback

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        """
        Takes screenshot of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, screenshotDirectory, fileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot saved to directory: %s" % destinationFile)
        except:
            self.log.error("### Exception occurred !!!")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "tag":
            return By.TAG_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        elif locatorType == "partiallink":
            return By.PARTIAL_LINK_TEXT
        else:
            self.log.error("Locator type not supported")
        return False

    def getElement(self, locator, locatorType="id"): # if no locator provided, bydefault it will take locatorType="id"
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: %s and locatorType: %s" %(locator, locatorType))
        except:
            self.log.error("Element Not Found with locator: %s and locatorType: %s" %(locator, locatorType))
        return element

    def getElementList(self, locator, locatorType="id"):
        """
        Get list of elements
        """
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
            self.log.info("Elements found with locator: %s and locatorType: %s" %(locator, locatorType))
        except:
            self.log.error("Elements not found with locator: %s and locatorType: %s" %(locator, locatorType))
        return element

    def clickElement(self, locator="", locatorType="id", element=None):
        """
        Click on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator: # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked the element with locator: %s and locatorType: %s" %(locator, locatorType))
        except:
            self.log.error("Cannot click the element with locator: %s and locatorType: %s" %(locator, locatorType))
            print_stack()

    def sendKeys(self, data, locator="", locatorType="id", element=None):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent keys to the element with locator: %s and locatorType: %s" %(locator, locatorType))
        except:
            self.log.error("Cannot send the keys to the element with locator: %s and locatorType: %s" %(locator, locatorType))
            print_stack()

    def sendKeysWhenReady(self, data, locator="", locatorType="id"):
        """
        Send keys to an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: %s :: seconds for element to be visible" % str(10))
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element appeared on the web page")
            element.click()
            element.send_keys(data)

            if element.get_attribute("value") != data:
                self.log.debug("Text is not sent by xpath in field so i will try to send string char by char!")
                element.clear()
                for i in range(len(data)):
                    element.send_keys(data[i] + "")
            self.log.info("Sent data on element with locator: %s and locatorType: %s" % (locator, locatorType))
        except:
            self.log.error("Element not appeared on the web page")
            self.log.error("Exception Caught: {}".format(traceback.format_exc()))
            self.log.error("".join(traceback.format_stack()))

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if element: # This means locator is not empty
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: %s" % str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element: %s" % info)
                self.log.info("The text is: '%s'" % text)
                text = text.strip()
        except:
            self.log.error("Failed to get text on element: %s" % info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="id", element=None):
        """
        Check if element is present
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator: # This means locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: %s and locatorType: %s" %(locator, locatorType))
                return True
            else:
                self.log.error("Element not present with locator: %s and locatorType: %s" %(locator, locatorType))
                return False
        except:
            self.log.error("Element NOT found!")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator: # This means locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: %s and locatorType: %s" %(locator, locatorType))
            else:
                self.log.error("Element is not displayed with locator: %s and locatorType: %s" %(locator, locatorType))
            return isDisplayed
        except:
            self.log.error("Element NOT found!")
            return False

    def isElementListPresent(self, byType, locator):
        """
        Check if element list is present
        """
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element list present with locator: %s and locatorType: %s" %(locator, str(byType)))
                return True
            else:
                self.log.error("Element list not present with locator: %s and locatorType: %s" %(locator, str(byType)))
                return False
        except:
            self.log.error("Element not found!!")
            return False

    def waitForElement(self, locator, locatorType="id", timeout=10, pollfrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waited %s seconds for element on Web page" % str(timeout))
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollfrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the Web page")
        except:
            self.log.error("Element not appeared on the Web page")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        """
        To scroll in up and down direction

        :param direction: Provide scroll direction up or down
        """
        # Scroll up
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0, -1000);")

        # Scroll down
        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def switchToFrameByIndex(self, locator, locatorType="xpath"):
        """
        Get iframe index using element locator inside iframe

        :parameter
            1. Required:
                :param locator: locator of the element
            2. Optional:
                :param locatorType: locatorType to find the element
        :returns
            Index of iframe
        :exception
            None
        """
        result = False
        try:
            iframe_list = self.getElementList("//iframe", locatorType="xpath")
            self.log.info("Length of iframe list: ")
            self.log.info(str(len(iframe_list)))
            for i in range(len(iframe_list)):
                self.switchToFrame(index=iframe_list[i])
                result = self.isElementPresent(locator, locatorType)
                if result:
                    self.log.info("iframe index is: ")
                    self.log.info(str(i))
                    break
                self.switchToDefaultContent()
            return result
        except:
            print("iFrame index not found")
            return result

    def switchToFrame(self, id="", name="", index=None):
        """
        Switch to iframe using element locator inside iframe

        Parameters:
            1. Required:
                None
            2. Optional:
                :param id: id of the iframe
                :param name: name of the iframe
                :param index: index of the iframe
        Returns:
            None
        Exception:
            None
        """
        if id:
            self.driver.switch_to.frame(id)
        elif name:
            self.driver.switch_to.frame(name)
        else:
            self.driver.switch_to.frame(index)

    def switchToDefaultContent(self):
        """
        Switch to default content

        Parameters:
            None
        Returns:
            None
        Exception:
            None
        """
        self.driver.switch_to.default_content()

    def getElementAttributeValue(self, attribute, element=None, locator="", locatorType="id"):
        """
        Get value of attribute of element

        Parameters:
            1. Required:
                :param attribute: attribute whose value to find

            2. Optional:
                :param element: element whose attribute need to find
                :param locator: locator of the element
                :param locatorType: locatorType to find the element
        Returns:
            Value of the attribute

        Exception:
            None
        """
        if locator:
            element = self.getElement(locator=locator, locatorType=locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator="", locatorType="id", info=""):
        """
        Check if element is enabled

        :parameter
            1. Required:
                :param locator: locator of the element to check
            2. Optional:
                :param locatorType: type of the locator(id(default))
                :param info: information about the element, label/name of the element

        :returns
            boolean

        :exception
            None
        """
        element = self.getElement(locator, locatorType=locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                self.log.info("Attribute value from Application Web UI :: %s" % value)
                enabled = not ("disabled" in value)
            if enabled:
                self.log.info("Element :: '%s' is enabled" % info)
            else:
                self.log.info("Element :: '%s' is not enabled" % info)
        except:
            self.log.error("Element :: '%s' state could not be found" % info)
        return enabled