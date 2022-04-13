"""
ユニットテスト
"""
from unittest import TestCase

from unipa import Unipa, UnipaLoginError
from unipa.test_setup import TestUnipaSetup


class TestUnipa(TestCase):
    """
    ユニットテスト
    """

    # noinspection PyClassHasNoInit
    def setUp(self) -> None:
        """
        テストセットアップ
        """
        tus = TestUnipaSetup()
        self.logger = tus.logger
        self.unipa = tus.unipa
        self.tests = tus.tests
        self.base_url = tus.base_url

    def test_fail_login(self) -> None:
        """
        ログイン失敗テスト
        """
        self.assertRaises(UnipaLoginError, Unipa(self.base_url).login, "XXXXXXXX", "XXXXXXXX")
