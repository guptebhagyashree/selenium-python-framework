from utilities.verifystatus import VerifyStatus
from pages.home.login_page import LoginPage
import unittest
import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = VerifyStatus(self.driver)

    # Need to verify 2 verification points
    # 1 fails, code will not go to the next verification point
    # If assert fails, it stops current test execution and
    # moves to the next test method
    @pytest.mark.run(order=2)
    def test_validLogin(self):
        self.lp.login(email="test@email.com", password="abcabc")
        result1 = self.lp.verifyLoginTitle()
        self.ts.mark(result1, "Title verification")
        result2 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal("test_validLogin", result2, resultMessage="Successful login verification")

    @pytest.mark.run(order=1)
    def test_invalidLogin(self):
        self.lp.logout()
        self.lp.login(email="test@email.com", password="123")
        result = self.lp.verifyLoginFailed()
        assert result == True