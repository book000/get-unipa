"""
ユーティリティ
"""
import re
from typing import List, Optional

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


class UnipaUtils:
    """
    ユーティリティ
    """

    def get_nav_items(self,
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
                        menu_id=self.get_menuid(pfconfirmcommand)
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
