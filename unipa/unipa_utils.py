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
        self.name = name
        self.sub_name = sub_name

    def __str__(self) -> str:
        return f"Menu(name={self.name}, sub_name={self.sub_name})"


class UnipaNavItem:
    """
    ナビゲーションアイテム
    """

    def __init__(self,
                 menu: Menu,
                 name: str,
                 menu_id: Optional[str]):
        self.menu = menu
        self.name = name
        self.menu_id = menu_id

    def __str__(self) -> str:
        return f"UnipaNavItem(menu={self.menu}, name={self.name}, menu_id={self.menu_id})"


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
