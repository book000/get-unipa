"""
ユニットテスト
"""
import logging
import os
import sys

from unipa import Unipa, UnipaLoginError
from unipa.models.tests import ConfigJsonModel, TestsJsonModel


class TestUnipaSetup:
    """
    ユニットテストセットアップ (ログイン)
    """

    def __init__(self) -> None:
        """
        テストセットアップ
        """
        self.__logger = logging.getLogger(__name__)
        if not self.__logger.hasHandlers():
            sh = logging.StreamHandler(sys.stdout)
            self.__logger.setLevel(logging.DEBUG)
            self.__logger.addHandler(sh)

        if not os.path.exists("config.json"):
            raise Exception("テストに必要なファイル config.json が見つかりません")

        with open("config.json", encoding="utf-8") as f:
            config: ConfigJsonModel = ConfigJsonModel.from_json(f.read())  # type: ignore

        self.__logger.info("config.json の読み込みに成功しました")

        if not os.path.exists("tests.json"):
            raise Exception("テストに必要なファイル tests.json が見つかりません")

        with open("tests.json", encoding="utf-8") as f:
            self.__tests: TestsJsonModel = TestsJsonModel.from_json(f.read())  # type: ignore

        self.__logger.info("tests.json の読み込みに成功しました")

        # ------------------------------------------------------------ #

        self.__base_url = config.base_url
        self.__unipa = Unipa(self.__base_url)

        username = config.username
        password = config.password

        try:
            self.__unipa.login(username, password)
        except UnipaLoginError as e:
            raise Exception(f"ログインに失敗しました: {e}")

    @property
    def logger(self) -> logging.Logger:
        """
        ロガーを返す

        Returns:
            logging.Logger: ロガー
        """
        return self.__logger

    @property
    def unipa(self) -> Unipa:
        """
        Unipa インスタンスを返す

        Returns:
            Unipa: Unipa インスタンス
        """
        return self.__unipa

    @property
    def tests(self) -> TestsJsonModel:
        """
        テスト用データを返す

        Returns:
            TestsJsonModel: テスト用データ
        """
        return self.__tests

    @property
    def base_url(self) -> str:
        """
        ベース URL を返す

        Returns:
            str: ベース URL
        """
        return self.__base_url
