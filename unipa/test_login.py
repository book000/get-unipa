"""
ユニットテスト
"""
import logging
import os
import sys
from unittest import TestCase

from unipa import Unipa, UnipaLoginError
from unipa.BulletinBoard import UnipaBulletinBoard
from unipa.models.tests import ConfigJsonModel, TestsJsonModel


class TestUnipa(TestCase):
    """
    ユニットテスト
    """

    # noinspection PyPep8Naming
    def setUp(self) -> None:
        """
        テストセットアップ
        """
        self.logger = logging.getLogger(__name__)
        sh = logging.StreamHandler(sys.stdout)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)

        if not os.path.exists("config.json"):
            self.fail("テストに必要なファイル config.json が見つかりません")

        with open("config.json", encoding="utf-8") as f:
            self.config: ConfigJsonModel = ConfigJsonModel.from_json(f.read())  # type: ignore

        self.logger.info("config.json の読み込みに成功しました")

        if not os.path.exists("tests.json"):
            self.fail("テストに必要なファイル tests.json が見つかりません")

        with open("tests.json", encoding="utf-8") as f:
            self.tests: TestsJsonModel = TestsJsonModel.from_json(f.read())  # type: ignore

        self.logger.info("tests.json の読み込みに成功しました")

        # ------------------------------------------------------------ #

        self.base_url = self.config.base_url
        self.unipa = Unipa(self.base_url)

        self.assertRaises(UnipaLoginError, self.unipa.login, "XXXXXXXX", "XXXXXXXX")

        username = self.config.username
        password = self.config.password

        self.assertTrue(self.unipa.login(username, password), "ログインに失敗しました")

    def test_bulletinboard_get_all(self) -> None:
        """
        掲示リストの取得テスト
        """
        items = UnipaBulletinBoard(self.unipa).get_all()
        for test in self.tests.bulletinboard_get_all:
            self.logger.info("掲示リスト取得テスト: タイトル「%s」", test.title)

            match = list(filter(lambda item: item.title == test.title or item.target_s == test.target_s, items))
            self.assertNotEqual(len(match), 0,
                                "タイトル「%s」または target_s「%s」に該当する掲示が見つかりませんでした。" % (test.title, test.target_s))
