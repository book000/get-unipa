"""
ユニットテスト
"""
import hashlib
import tempfile
from unittest import TestCase

from unipa import UnipaUtils
from unipa.BulletinBoard import UnipaBulletinBoard
from unipa.test_setup import TestUnipaSetup


class TestBulletinboardUnipa(TestCase):
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

            self.logger.info("target_match: %s", str(target_match))

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
        detail_items = [x.get_details(self.unipa) for x in self.bulletinboard_items]

        for test in self.tests.bulletinboard_get_details:
            self.logger.info("掲示板 掲示詳細の取得テスト: 掲示タイトル「%s」", test.title)

            target = None
            target_match = 0
            for details in detail_items:
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

            self.logger.info("target_match: %s", str(target_match))

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

            if len(test.file_hashs) > 0:
                file_hashs = []
                with tempfile.TemporaryDirectory() as temppath:
                    for file in target.files:
                        path = temppath + "/" + file.filename
                        print(path)
                        file.download(self.unipa, path)

                        with open(path, "rb") as f:
                            file_hashs.append(hashlib.sha256(f.read()).hexdigest())

                for filehash in test.file_hashs:
                    self.assertIn(filehash, file_hashs, "添付ファイルのファイルハッシュが一致しません")
