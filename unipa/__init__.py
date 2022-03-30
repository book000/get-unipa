# coding: utf-8
"""
Library for get various information about UNIVERSAL PASSPORT.

UNIVERSAL PASSPORT のさまざまな情報を取得するためのライブラリです。
"""
import logging
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import Response


class Unipa:
    """
    UNIVERSAL PASSPORT 基本ライブラリ
    """

    def __init__(self,
                 base_url: str):
        self.session: requests.Session = requests.Session()
        self.logger = logging.getLogger(__name__)
        self.__base_url: str = base_url
        self.__logged_in: bool = False
        self.__response: Optional[Response] = None

    def login(self,
              username: str,
              password: str) -> bool:
        """
        UNIVERSAL PASSPORT にログインする

        Args:
            username: ユーザー名
            password: パスワード

        Returns:
            bool: ログインできたか
        """

        self.__response = self.session.get(self.__base_url)
        if self.__response.status_code != 200:
            raise UnipaInternalError("ログインページの取得に失敗しました。")

        with open("hoge.html", "w", encoding="utf-8") as f:
            f.write(self.__response.text)

        soup = BeautifulSoup(self.__response.text, "html5lib")
        login_form = soup.find("form", {"id": "loginForm"})
        if login_form is None:
            raise UnipaInternalError("ログインフォーム情報の取得に失敗しました。")

        login_url = urljoin(self.__base_url, login_form.get("action"))
        self.logger.debug("ログインフォームのURL: %s", login_url)

        params = {}

        for input_tag in login_form.find_all("input"):
            input_tag_name = input_tag.get("name")
            input_tag_value = input_tag.get("value")
            if input_tag_name is None or input_tag_value is None:
                continue
            if input_tag_value == "":
                continue

            params[input_tag_name] = input_tag_value

        for button_tag in login_form.find_all("button"):
            button_tag_name = button_tag.get("name")
            button_tag_value = button_tag.get("value")
            if button_tag_name is None:
                continue

            if button_tag_value is None:
                button_tag_value = ""

            params[button_tag_name] = button_tag_value

        self.logger.debug("ログインフォームのデフォルトパラメータ: %s", params)

        params["loginForm:userId"] = username
        params["loginForm:password"] = password

        self.__response = self.session.post(login_url, data=params, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

        if self.__response.status_code != 200:
            return False

        soup = BeautifulSoup(self.__response.text, "html5lib")
        error_details = soup.find("span", {"class": "ui-messages-error-detail"})
        if error_details is not None:
            raise UnipaLoginError(error_details.text)

        return True

    def get_latest_response(self) -> Optional[Response]:
        """
        最後のレスポンスを返します。デバッグのために利用することを想定しています。

        Returns:
            Optional[Response]: レスポンス (ない場合は None)
        """
        return self.__response


class UnipaInternalError(Exception):
    """
    処理に失敗した
    """


class UnipaLoginError(Exception):
    """
    ログインに失敗した
    """
