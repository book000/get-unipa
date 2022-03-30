"""
ユニットテスト
"""
import json
import os
from unittest import TestCase

from unipa import Unipa, UnipaLoginError


class TestUnipa(TestCase):
    """
    ユニットテスト
    """

    # noinspection PyPep8Naming
    def setUp(self) -> None:
        """
        テストセットアップ
        """
        if not os.path.exists("config.json"):
            self.fail("テストに必要なファイル config.json が見つかりません")

        if not os.path.exists("tests.json"):
            self.fail("テストに必要なファイル tests.json が見つかりません")

        with open("config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        with open("tests.json", encoding="utf-8") as f:
            self.tests = json.load(f)

        self.base_url = self.config["base_url"]
        self.unipa = Unipa(self.base_url)

        self.assertRaises(UnipaLoginError, self.unipa.login, "XXXXXXXX", "XXXXXXXX")

        username = self.config["username"]
        password = self.config["password"]

        self.assertTrue(self.unipa.login(username, password), "ログインに失敗しました")

    def test(self) -> None:
        """
        ログインテストを書くためだけのメソッド
        """
