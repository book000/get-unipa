# coding: utf-8
"""
Library for get various information about UNIVERSAL PASSPORT.

UNIVERSAL PASSPORT のさまざまな情報を取得するためのライブラリです。
"""
import logging
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import Response

from unipa.errors import UnipaInternalError, UnipaLoginError, UnipaNotLoggedIn
from unipa.unipa_utils import UnipaNavItem, UnipaUtils


class UnipaToken:
    """
    トークンクラス
    """

    def __init__(self,
                 rx_token: str,
                 rx_login_key: str,
                 rx_device_kbn: str,
                 rx_login_type: str,
                 javax_view_state: str):
        """
        トークンクラス コンストラクタ

        Args:
            rx_token: トークン
            rx_login_key: ログインキー
            rx_device_kbn: デバイス区分
            rx_login_type: ログイン種別
            javax_view_state: View state
        """
        self._rx_token = rx_token
        self._rx_login_key = rx_login_key
        self._rx_device_kbn = rx_device_kbn
        self._rx_login_type = rx_login_type
        self._javax_view_state = javax_view_state

    @property
    def rx_token(self) -> str:
        """
        トークン

        Returns:
            str: トークン
        """
        return self._rx_token

    @property
    def rx_login_key(self) -> str:
        """
        ログインキー

        Returns:
            str: ログインキー
        """
        return self._rx_login_key

    @property
    def rx_device_kbn(self) -> str:
        """
        デバイス区分

        Returns:
            str: デバイス区分
        """
        return self._rx_device_kbn

    @property
    def rx_login_type(self) -> str:
        """
        ログイン種別

        Returns:
            str: ログイン種別
        """
        return self._rx_login_type

    @property
    def javax_view_state(self) -> str:
        """
        View state

        Returns:
            str: View state
        """
        return self._javax_view_state


class Unipa:
    """
    UNIVERSAL PASSPORT 基本ライブラリ
    """

    def __init__(self,
                 base_url: str):
        """
        Unipa クラスを初期化します

        Args:
            base_url: UNIVERSAL PASSPORT のベース URL (ログインページ URL にて、 `/up/` より前の URL を指定します。例: https://unipa.itp.kindai.ac.jp/)
        """
        self.session: requests.Session = requests.Session()
        self.session.headers["User-Agent"] = "get-unipa (https://github.com/book000/get-unipa)"
        self.logger = logging.getLogger(__name__)
        self.__base_url: str = base_url
        self.__logged_in: bool = False
        self.__response: Optional[Response] = None

        self.__token: Optional[UnipaToken] = None
        self.__nav_items: List[UnipaNavItem] = []

        self.__request_url: Optional[str] = None

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
            # form#loginForm が見つからない場合、ログイントークンなどが取得できないのでログイン不可
            raise UnipaInternalError("ログインフォーム情報の取得に失敗しました。")

        # ログインURL構成 (base_url + actionの値)
        login_url = urljoin(self.__base_url, login_form.get("action"))
        self.logger.debug("ログインフォームのURL: %s", login_url)

        params = {}

        # input と button の値をログイン処理でそのまま流用する
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

        self.__logged_in = True
        self.update_token(soup)

        utils = UnipaUtils()
        self.__nav_items = utils.get_nav_items(soup)

        header_form = soup.find("form", {"id": "headerForm"})
        self.__request_url = urljoin(self.__base_url, header_form.get("action"))

        return True

    def request_from_menu(self,
                          menu_item: UnipaNavItem) -> BeautifulSoup:
        """
        メニューからリクエストを送信する

        Args:
            menu_item: メニューアイテム

        Returns:
            Response: レスポンス
        """
        if not self.__logged_in or self.__request_url is None or self.__token is None:
            raise UnipaNotLoggedIn()

        return self.request("menuForm", {
            "menuForm:mainMenu": "menuForm:mainMenu",
            "rx.sync.source": "menuForm:mainMenu",
            "menuForm:mainMenu_menuid": str(menu_item.menu_id),
        })

    def request(self,
                request_type: str,
                extra_params: dict[str, str],
                response_markup: str = "html5lib") -> BeautifulSoup:
        """
        リクエストを送信する

        Args:
            request_type: リクエストタイプ (menuForm, funcForm など)
            extra_params: リクエストに付加するパラメータ (トークンなど以外)
            response_markup: レスポンスのマークアップ

        Returns:
            Response: レスポンス
        """
        if not self.__logged_in or self.__request_url is None or self.__token is None:
            raise UnipaNotLoggedIn()

        params = {
            "rx-token": self.__token.rx_token,
            "rx-loginKey": self.__token.rx_login_key,
            "rx-deviceKbn": self.__token.rx_device_kbn,
            "rx-loginType": self.__token.rx_login_type,
            "javax.faces.ViewState": self.__token.javax_view_state,
            request_type: request_type
        }
        params.update(extra_params)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if response_markup == "lxml":
            headers["Accept"] = "application/xml"
            headers["Faces-Request"] = "partial/ajax"
            headers["X-Requested-With"] = "XMLHttpRequest"

        self.__response = self.session.post(self.__request_url, data=params, headers=headers)

        if self.__response.status_code != 200:
            raise UnipaInternalError("リクエストに失敗しました。(" + str(self.__response.status_code) + ")")

        soup = BeautifulSoup(self.__response.text, response_markup)
        self.logger.debug("soupレスポンス: %s", soup.prettify())

        if response_markup == "html5lib":
            self.update_token(soup)

        return soup

    def is_logged_in(self) -> bool:
        """
        ログインしているかどうかを返します。

        Returns:
            bool: ログインしているかどうか
        """
        return self.__logged_in

    def get_token(self) -> Optional[UnipaToken]:
        """
        トークンを返します。

        Returns:
            Optional[UnipaToken]: トークン
        """
        return self.__token

    def get_nav_items(self) -> List[UnipaNavItem]:
        """
        ナビゲーションアイテムを返します。

        Returns:
            List[UnipaNavItem]: ナビゲーションアイテム
        """
        return self.__nav_items

    def get_latest_response(self) -> Optional[Response]:
        """
        最後のレスポンスを返します。デバッグのために利用することを想定しています。

        Returns:
            Optional[Response]: レスポンス (ない場合は None)
        """
        return self.__response

    def update_token(self,
                     soup: BeautifulSoup) -> None:
        """
        トークンをアップデートします。
        """
        header_form = soup.find("form", {"id": "headerForm"})
        if header_form is None:
            raise UnipaInternalError("トークンを更新するためのフォーム情報の取得に失敗しました。")

        rx_token = header_form.find("input", {"name": "rx-token"}).get("value")
        rx_login_key = header_form.find("input", {"name": "rx-loginKey"}).get("value")
        rx_device_kbn = header_form.find("input", {"name": "rx-deviceKbn"}).get("value")
        rx_login_type = header_form.find("input", {"name": "rx-loginType"}).get("value")
        javax_view_state = header_form.select_one("input[name=\"javax.faces.ViewState\"]").get("value")

        self.__token = UnipaToken(rx_token, rx_login_key, rx_device_kbn, rx_login_type, javax_view_state)
