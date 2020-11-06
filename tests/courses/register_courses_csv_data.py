from pages.courses.register_courses_page import RegisterCoursesPage
from utilities.verifystatus import VerifyStatus
import unittest
import pytest
from ddt import ddt, data, unpack
from utilities.read_data import getCSVData
from pages.home.navigation_page import NavigationPage

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterCoursesCSVDataTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = VerifyStatus(self.driver)
        self.nav = NavigationPage(self.driver)

    def setUp(self) -> None:
        self.nav.navigateToWebsiteLogo()

    @pytest.mark.run(order=1)
    @data(*getCSVData("C:\\Users\\Dhanshree\\workspace_python\\ATFTutorial\\testdata.csv"))
    @unpack
    def test_invalidEnrollment(self, courseName, zipcode):
        self.courses.enterCourseName(name=courseName)
        self.courses.selectCourseToEnroll(fullCourseName=courseName)
        self.courses.enrollCourse(code=zipcode)
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_invalidEnrollment", result, "Enrollment Failed Verification")