from pages.courses.register_courses_page import RegisterCoursesPage
from utilities.verifystatus import VerifyStatus
import unittest
import pytest
from ddt import ddt, data, unpack


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterMultipleCoursesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = VerifyStatus(self.driver)

    @pytest.mark.run(order=1)
    @data(("Learn Python 3 from scratch", "411033"), ("Selenium WebDriver With Java", "123456"))
    @unpack
    def test_invalidEnrollment(self, courseName, zipcode):
        self.courses.enterCourseName(name=courseName)
        self.courses.selectCourseToEnroll(fullCourseName=courseName)
        self.courses.enrollCourse(code=zipcode)
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Failed Verification")
        self.driver.find_element_by_xpath("//a[@class='navbar-brand header-logo']").click()
