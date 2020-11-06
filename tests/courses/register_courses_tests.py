from pages.courses.register_courses_page import RegisterCoursesPage
from utilities.verifystatus import VerifyStatus
import unittest
import pytest
import time

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class RegisterCoursesTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = VerifyStatus(self.driver)

    @pytest.mark.run(order=1)
    def test_invalidEnrollment(self):
        self.courses.enterCourseName(name="Python")
        self.courses.selectCourseToEnroll(fullCourseName="Learn Python 3 from scratch")
        self.courses.enrollCourse(code="411033")
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Failed Verification")
