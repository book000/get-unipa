"""
ユニットテスト
"""
import logging
import os
import sys
from unittest import TestCase

from unipa import Unipa, UnipaLoginError, UnipaUtils
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
        if not self.logger.hasHandlers():
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

        self.bulletinboard_items = UnipaBulletinBoard(self.unipa).get_all()

    def test_bulletinboard_get_all(self) -> None:
        """
        掲示リストの取得テスト
        """

        for test in self.tests.bulletinboard_get_all:
            self.logger.info("掲示リスト取得テスト: タイトル「%s」", test.title)

            target = None
            target_match = 0
            for match in self.bulletinboard_items:
                results = [
                    match.title == test.title,
                    match.flag_id == test.flag_id,
                    match.unread_id == test.unread_id,
                    match.is_attention == test.is_attention,
                    match.is_flag == test.is_flag,
                    match.is_unread == test.is_unread,
                ]
                if len(list(filter(lambda result: result is True, results))) > target_match:
                    target = match
                    target_match = len(list(filter(lambda result: result is True, results)))

            if target is None:
                self.fail("掲示リストに該当する掲示が見つかりませんでした。")

            self.assertEqual(target.title, test.title, "タイトルが一致しません")
            self.assertEqual(target.flag_id, test.flag_id, "flag_idが一致しません")
            self.assertEqual(target.unread_id, test.unread_id, "unread_idが一致しません")
            self.assertEqual(target.is_attention, test.is_attention, "is_attentionが一致しません")
            self.assertEqual(target.is_flag, test.is_flag, "is_flagが一致しません")
            self.assertEqual(target.is_unread, test.is_unread, "is_unreadが一致しません")

    def test_bulletinboard_get_details(self) -> None:
        """
        掲示板 掲示詳細の取得テスト
        """
        for test in self.tests.bulletinboard_get_details:
            self.logger.info("掲示板 掲示詳細の取得テスト: 掲示タイトル「%s」", test.title)

            target = None
            target_match = 0
            for match in self.bulletinboard_items:
                details = match.get_details(self.unipa)
                results = [
                    details.title == test.title,
                    details.author == test.author,
                    details.category == test.category,
                    details.content_html == test.content_html,
                    details.publication_period.start_date == UnipaUtils.process_datetime(
                        test.publication_period.start_date),
                    details.publication_period.end_date == UnipaUtils.process_datetime(
                        test.publication_period.end_date),
                ]
                if len(list(filter(lambda result: result is True, results))) > target_match:
                    target = details
                    target_match = len(list(filter(lambda result: result is True, results)))

            if target is None:
                self.fail("掲示リストに該当する掲示が見つかりませんでした。")

            self.assertEqual(target.item_id, test.item_id, "IDが一致しません")
            self.assertEqual(target.title, test.title, "タイトルが一致しません")
            self.assertEqual(target.author, test.author, "authorが一致しません")
            self.assertEqual(target.category, test.category, "categoryが一致しません")
            self.assertEqual(target.content_html, test.content_html, "content_htmlが一致しません")
            self.assertEqual(target.publication_period.start_date,
                             UnipaUtils.process_datetime(test.publication_period.start_date),
                             "publication_period.start_dateが一致しません")
            self.assertEqual(target.publication_period.end_date,
                             UnipaUtils.process_datetime(test.publication_period.end_date),
                             "publication_period.end_dateが一致しません")
