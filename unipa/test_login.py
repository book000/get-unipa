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

            matches = list(filter(lambda item: item.item_id == test.item_id, self.bulletinboard_items))
            self.assertNotEqual(len(matches), 0, "item_id「%s」に該当する掲示が見つかりませんでした。" % test.item_id)

            match = matches[0]
            self.assertEqual(match.item_id, test.item_id, "IDが一致しません")
            self.assertEqual(match.title, test.title, "タイトルが一致しません")
            self.assertEqual(match.target_s, test.target_s, "target_sが一致しません")
            self.assertEqual(match.target_p, test.target_p, "target_pが一致しません")
            self.assertEqual(match.flag_id, test.flag_id, "flag_idが一致しません")
            self.assertEqual(match.unread_id, test.unread_id, "unread_idが一致しません")
            self.assertEqual(match.is_attention, test.is_attention, "is_attentionが一致しません")
            self.assertEqual(match.is_flag, test.is_flag, "is_flagが一致しません")
            self.assertEqual(match.is_unread, test.is_unread, "is_unreadが一致しません")

    def test_bulletinboard_get_details(self) -> None:
        """
        掲示板 掲示詳細の取得テスト
        """
        for test in self.tests.bulletinboard_get_details:
            self.logger.info("掲示板 掲示詳細の取得テスト: 掲示タイトル「%s」", test.title)

            matches = list(filter(lambda item: item.item_id == test.item_id, self.bulletinboard_items))
            self.assertNotEqual(len(matches), 0, "item_id「%s」に該当する掲示が見つかりませんでした。" % test.item_id)

            details = matches[0].get_details(self.unipa)

            self.assertEqual(details.item_id, test.item_id, "IDが一致しません")
            self.assertEqual(details.title, test.title, "タイトルが一致しません")
            self.assertEqual(details.author, test.author, "authorが一致しません")
            self.assertEqual(details.category, test.category, "categoryが一致しません")
            self.assertEqual(details.content_html, test.content_html, "content_htmlが一致しません")
            self.assertEqual(details.publication_period.start_date,
                             UnipaUtils.process_datetime(test.publication_period.start_date),
                             "publication_period.start_dateが一致しません")
            self.assertEqual(details.publication_period.end_date,
                             UnipaUtils.process_datetime(test.publication_period.end_date),
                             "publication_period.end_dateが一致しません")
