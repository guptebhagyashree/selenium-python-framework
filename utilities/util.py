"""
@package utilities

Util class implementation
All most commonly used utilities should be implemented in this class

Example:
    name = self.util.getUniqueName()
"""

import utilities.custom_logger as cl
import logging
import time
import traceback
import string, random

class Util(object):

    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of time
        """
        if info is not None:
            self.log.info("Wait %s seconds for %s" % (str(sec), info))
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type="letters"):
        """
        Get random string of characters

        Parameters:
            length: Length of string, number of characters string should have
            type: Type of characters string should have. Default is letters
            Provide lower/upper/digits/mix for different types
        """
        alpha_num = ""
        if type == "lower":
            case = string.ascii_lowercase
        elif type == "upper":
            case = string.ascii_uppercase
        elif type == "digits":
            case = string.digits
        elif type == "mix":
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        """
        Get a unique name

        Parameters:
            charCount: To take the character count. By default is 10 characters.
        """
        self.getAlphaNumeric(charCount, "lower")

    def getUniqueNameList(self, listSize=5, itemLength=None):
        """
        Get a list of valid email ids

        Parameters:
            listSize: Number of names. Default is 5 names in a list
            itemLength: It should be a list containing number of items equal to the listSize
                        This determines the length of the each item in the list -> [1, 2, 3, 4, 5]
        """
        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
        return nameList

    def verifyTextContains(self, actualText, expectedText):
        """
        Verify actual text contains expected text string

        Parameters:
            expectedText: Expected Text
            actualText: Actual Text
        """
        self.log.info("Actual Text from application web UI: %s" % actualText)
        self.log.info("Expected Text from application web UI: %s" % expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION CONTAINS !!!")
            return True
        else:
            self.log.error("### VERIFICATION DOES NOT CONTAINS !!!")
            return False

    def verifyTextMatch(self, actualText, expectedText):
        """
        Verify text match

        Parameters:
            expectedText: Expected Text
            actualText: Actual Text
        """
        self.log.info("Actual Text from application web UI: %s" % actualText)
        self.log.info("Expected Text from application web UI: %s" % expectedText)
        if expectedText.lower() == actualText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.error("### VERIFICATION DOES NOT MATCHED !!!")
            return False

    def verifyListMatch(self, actualList, expectedList):
        """
        Verify two list matches

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        return set(expectedList) == set(actualList)

    def verifyListContains(self, actualList, expectedList):
        """
        Verify actual list contains elements of expected list

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True