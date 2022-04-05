"""
ユーティリティ
"""
import datetime
import re
from typing import Dict, List, Literal, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from unipa import UnipaInternalError


class Menu:
    """
    ナビゲーションメニュー
    """

    def __init__(self,
                 name: str,
                 sub_name: Optional[str]):
        """
        ナビゲーションメニュー コンストラクタ

        Args:
            name: メニュー名
            sub_name: サブメニュー名
        """
        self._name = name
        self._sub_name = sub_name

    @property
    def name(self) -> str:
        """
        メニュー名

        Returns:
            str: メニュー名
        """
        return self._name

    @property
    def sub_name(self) -> Optional[str]:
        """
        サブメニュー名

        Returns:
            Optional[str]: サブメニュー名
        """
        return self._sub_name

    def __str__(self) -> str:
        return f"Menu(_name={self.name}, sub__name={self.sub_name})"


class UnipaNavItem:
    """
    ナビゲーションアイテム
    """

    def __init__(self,
                 menu: Menu,
                 name: str,
                 menu_id: Optional[str]):
        """
        ナビゲーションアイテム コンストラクタ

        Args:
            menu: メニュー
            name: アイテム名
            menu_id: メニュー ID
        """
        self._menu = menu
        self._name = name
        self._menu_id = menu_id

    @property
    def menu(self) -> Menu:
        """
        メニュー

        Returns:
            Menu: メニュー
        """
        return self._menu

    @property
    def name(self) -> str:
        """
        アイテム名

        Returns:
            str: アイテム名
        """
        return self._name

    @property
    def menu_id(self) -> Optional[str]:
        """
        メニュー ID

        Returns:
            Optional[str]: メニュー ID
        """
        return self._menu_id

    def __str__(self) -> str:
        return f"UnipaNavItem(_menu={self._menu}, _name={self._name}, __menu_id={self._menu_id})"


class UnipaRequestUrl:
    """
    リクエスト URL の列挙

    フォームのaction属性を取得し更新する。システムによって違うかもしれないので
    """
    KEYS = Literal['TOP', 'BULLETBOARD', 'SITEMAP']
    __urls: Dict[KEYS, Optional[str]] = {
        "TOP": None,
        "BULLETBOARD": None,
        "SITEMAP": None,
    }

    def __init__(self,
                 base_url: str):
        """
        UnipaRequestUrl コンストラクタ

        Args:
            base_url: ベース URL
        """
        self.__base_url = base_url

    def get(self,
            name: KEYS) -> Optional[str]:
        """
        UnipaRequestUrl の値 (URL) を取得する

        Args:
            name: UnipaRequestUrl の名前

        Returns:
            Optional[str]: UnipaRequestUrl の値 (URL)
        """
        if name not in self.__urls:
            raise UnipaInternalError(f"{name} is undefined")

        if self.__urls[name] is None:
            return None

        return urljoin(self.__base_url, self.__urls[name])

    def set(self,
            name: KEYS,
            soup: BeautifulSoup) -> None:
        """
        BeautifulSoup から UnipaRequestUrl の値 (URL) を設定する

        Args:
            name: UnipaRequestUrl の名前
            soup: BeautifulSoup
        """
        if name not in self.__urls:
            raise UnipaInternalError(f"{name} is undefined")

        header_form = soup.find("form", {"id": "headerForm"})
        self.__urls[name] = header_form.get("action")


class UnipaUtils:
    """
    ユーティリティ
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def get_nav_items(cls,
                      soup: BeautifulSoup) -> List[UnipaNavItem]:
        """
        ナビゲーションアイテムを取得する

        Args:
            soup: BeautifulSoup

        Returns:
            List[UnipaNavItem]: ナビゲーションアイテム
        """
        menu_form = soup.find("div", {"id": "menuForm:mainMenu"})
        if menu_form is None:
            raise UnipaInternalError("メニューが見つかりません")

        items = []
        menu_items = soup.select("div[id=\"menuForm:mainMenu\"] > .ui-menu-list > .ui-menuitem")
        for menu_item in menu_items:
            menu_name = menu_item.select_one("a.ui-submenu-link").find("span", {"class": "ui-menuitem-text"})

            submenus = menu_item.select_one("ul.ui-menu-child").find_all("td")

            for submenu in submenus:
                submenu_name = submenu.select_one("li.ui-widget-header").find("h3")
                submenu_items = submenu.select("li.ui-menuitem")
                for submenu_item in submenu_items:
                    pfconfirmcommand = submenu_item.select_one("a.ui-menuitem-link").get("data-pfconfirmcommand")
                    if pfconfirmcommand is None:
                        continue
                    items.append(UnipaNavItem(
                        menu=Menu(
                            name=menu_name.text,
                            sub_name=submenu_name.text
                        ),
                        name=submenu_item.find("span", {"class": "ui-menuitem-text"}).text,
                        menu_id=cls.get_menuid(pfconfirmcommand)
                    ))

        return items

    @staticmethod
    def get_menuid(pfconfirmcommand: str) -> Optional[str]:
        """
        メニュー ID を取得する

        Args:
            pfconfirmcommand: data-pfconfirmcommand

        Returns:
            Optional[str]: メニュー ID
        """
        pattern = re.compile(r"'menuForm:mainMenu_menuid':'(.+?)'")
        match = pattern.search(pfconfirmcommand)
        if match is None:
            return None

        return match.group(1)

    @staticmethod
    def process_datetime(datetime_str: Optional[str]) -> Optional[datetime.datetime]:
        """
        UNIPA の日時テキスト(YYYY/MM/DD HH:MM)から datetime.datetime に変換する

        Args:
            datetime_str: UNIPA の日時テキスト

        Returns:
            Optional[datetime.datetime]: 変換後の datetime.datetime
        """
        if datetime_str is None or datetime_str == "":
            return None
        datetime_str = re.sub(r"\(.+?\)", "", datetime_str)
        datetime_format = "%Y/%m/%d %H:%M %z"
        jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        return datetime.datetime.strptime(datetime_str + " +0900", datetime_format).astimezone(jst)
