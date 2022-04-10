"""
パッケージ: 掲示板
"""
import re
from typing import List, Optional

from unipa import Unipa
from unipa.BulletinBoard.BulletinBoard import UnipaBulletinBoardItem
from unipa.errors import UnipaInternalError, UnipaNotLoggedIn


class UnipaBulletinBoard:
    """
    掲示板
    """

    def __init__(self,
                 unipa: Unipa):
        """
        コンストラクタ
        """
        self.unipa = unipa
        self.logger = unipa.logger

    def get_all(self) -> List[UnipaBulletinBoardItem]:
        """
        掲示リストを取得します。

        Returns:
            List[UnipaBulletinBoardItem]: 掲示リスト
        """

        if not self.unipa.is_logged_in():
            raise UnipaNotLoggedIn()

        nav_item = next(filter(lambda x: x.name == "掲示板", self.unipa.get_nav_items()))
        menu_id = nav_item.menu_id

        self.logger.debug(f"BulletinBoard/menu_id: {menu_id}")

        soup = self.unipa.request_from_menu(nav_item, {
            "javax.faces.partial.execute": "@all"
        })
        self.unipa.request_url.set("BULLETBOARD", soup)

        if soup.find("div", {"class": "ui-tabs-panels"}) is None:
            raise UnipaInternalError("掲示板パネルが見つかりませんでした。")

        panels = soup.select("div.ui-tabs-panels > div[role=\"tabpanel\"]")

        if len(panels) < 2:
            raise UnipaInternalError("掲示板パネルのうち、全表示タブが見つかりませんでした。")

        panel = panels[1]

        # このへんの処理あまりにも無理やりなのですぐ壊れるかも

        items = []
        # div.ui-scrollpanel > div.alignRight
        for item in panel.select("div.ui-scrollpanel > div.alignRight"):
            a_tag = item.find("a")
            item_id = a_tag.get("id")
            title = a_tag.text
            onclick = a_tag.get("onclick")
            [target_s, target_p] = self.get_target_sp(onclick)  # idを拾ってもいい
            if target_s is None or target_p is None:
                continue

            is_attention = item.select_one("i.iconColorAttention") is not None

            buttons = panel.select("span.inlineBlock > div[type=\"button\"]")
            if len(buttons) < 2:
                raise UnipaInternalError("掲示板パネルのうち、フラグ・未/既読ボタンが見つかりませんでした。")

            flag_input = buttons[0].select_one("input[type=\"checkbox\"]")
            flag_id = flag_input.get("id")
            is_flag = flag_input.get("checked") is None

            unread_input = buttons[1].select_one("input[type=\"checkbox\"]")
            unread_id = unread_input.get("id")
            is_unread = unread_input.get("checked") is not None

            items.append(UnipaBulletinBoardItem(
                item_id,
                title,
                target_s,
                target_p,
                flag_id,
                unread_id,
                is_attention,
                is_flag,
                is_unread
            ))

        return items

    @staticmethod
    def get_target_sp(onclick: str) -> List[Optional[str]]:
        """
        onclick 属性から、s, pを取得します。

        Args:
            onclick: onclick 属性の値

        Returns:
            [s, p]: s, p 値
        """
        pattern = re.compile(r"PrimeFaces\.ab\({s:\"(.+?)\",p:\"(.+?)\"}\);")
        match = pattern.search(onclick)
        if match is None:
            return [None, None]

        return [match.group(1), match.group(2)]
