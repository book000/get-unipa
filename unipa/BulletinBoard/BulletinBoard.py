"""
掲示板
"""
import re
from typing import List

from unipa import Unipa, UnipaUtils
from unipa.BulletinBoard.BulletinBoardFile import UnipaBulletinBoardFile
from unipa.BulletinBoard.BulletinBoardItemDetails import UnipaBulletinBoardItemDetails
from unipa.BulletinBoard.PublicationPeriod import UnipaPublicationPeriod


class UnipaBulletinBoardItem:
    """
    掲示板の掲示アイテム
    """

    def __init__(self,
                 item_id: str,
                 title: str,
                 target_s: str,
                 target_p: str,
                 flag_id: str,
                 unread_id: str,
                 is_attention: bool,
                 is_flag: bool,
                 is_unread: bool):
        """
        掲示板の掲示アイテム コンストラクタ

        Args:
            item_id: 掲示 ID (恒久的なIDではないことに注意)
            title: 掲示タイトル
            target_s: 掲示 s 値 (リクエスト用)
            target_p: 掲示 p 値 (リクエスト用)
            flag_id: フラグ ID
            unread_id: 未読 ID
            is_attention: 注目フラグ (投稿者によって設定)
            is_flag: フラグ (ユーザーが設定可能)
            is_unread: 未読か (ユーザーが設定可能)
        """
        self._item_id = item_id
        self._title = title
        self._target_s = target_s
        self._target_p = target_p
        self._flag_id = flag_id
        self._unread_id = unread_id
        self._is_attention = is_attention
        self._is_flag = is_flag
        self._is_unread = is_unread

    @property
    def item_id(self) -> str:
        """
        掲示 ID

        Returns:
            str: 掲示 ID

        Notes:
            この ID は恒久的な ID ではなく、掲示表示順番のみで ID が振られているようです。<br>
            <b>掲示内容の変化検知など、掲示が合致するかどうかのチェックには用いないでください</b>
        """
        return self._item_id

    @property
    def title(self) -> str:
        """
        掲示タイトル

        Returns:
            str: 掲示タイトル
        """
        return self._title

    @property
    def target_s(self) -> str:
        """
        掲示 s 値 (リクエスト用)

        Returns:
            str: 掲示 s 値 (リクエスト用)
        """
        return self._target_s

    @property
    def target_p(self) -> str:
        """
        掲示 p 値 (リクエスト用)

        Returns:
            str: 掲示 t 値 (リクエスト用)
        """
        return self._target_p

    @property
    def flag_id(self) -> str:
        """
        フラグ ID

        Returns:
            str: フラグ ID
        """
        return self._flag_id

    @property
    def unread_id(self) -> str:
        """
        未読 ID

        Returns:
            str: 未読 ID
        """
        return self._unread_id

    @property
    def is_attention(self) -> bool:
        """
        注目フラグ (投稿者によって設定)

        Returns:
            bool: 注目フラグ (投稿者によって設定)
        """
        return self._is_attention

    @property
    def is_flag(self) -> bool:
        """
        フラグ (ユーザーが設定可能)

        Returns:
            bool: フラグ (ユーザーが設定可能)
        """
        return self._is_flag

    @property
    def is_unread(self) -> bool:
        """
        未読か (ユーザーが設定可能)

        Returns:
            bool: 未読か (ユーザーが設定可能)
        """
        return self._is_unread

    def get_details(self,
                    unipa: Unipa) -> UnipaBulletinBoardItemDetails:
        """
        掲示アイテムの詳細を取得します。

        Returns:
            UnipaBulletinBoardItemDetails: 掲示アイテムの詳細
        """
        soup = unipa.request("BULLETBOARD", "funcForm", {
            "javax.faces.source": self.target_s,
            "javax.faces.partial.execute": self.target_s,
            "funcForm:tabArea_activeIndex": "1",
            self.target_s: self.target_p
        }, "html5lib")

        outputpanel = soup.select_one("div.ui-outputpanel")
        if outputpanel is None:
            raise RuntimeError("掲示板の詳細パネルが見つかりません。")

        table = outputpanel.select_one("table.singleTable > tbody")
        data = {}
        for tr in table.find_all("tr", recursive=False):
            tds = tr.find_all("td", recursive=False)
            if len(tds) != 2:
                continue

            row_key = tds[0]
            row_value = tds[1]

            # print(row_key.text, row_value.text)
            data[row_key.text.strip()] = row_value

        raw_publication_period = data["掲示期間"]
        raw_start_date: str = raw_publication_period.find_all("span")[0].text.strip()
        raw_end_date = raw_publication_period.find_all("span")[2].text.strip()

        start_date = UnipaUtils.process_datetime(raw_start_date)
        end_date = UnipaUtils.process_datetime(raw_end_date)

        publication_period = UnipaPublicationPeriod(start_date, end_date)

        # 掲示添付ファイル取得
        files = []
        buttons = soup.select("div.btnAreaBottom button")
        if len(buttons) > 0:
            for button in buttons:
                if "添付ファイル" not in button.get("title"):
                    continue

                check_files_id = button.get("id")
                files = self.__get_files(unipa, check_files_id)

        return UnipaBulletinBoardItemDetails(
            item_id=self.item_id,
            title=data["件名"].text.strip(),
            author=data["差出人"].text.strip(),
            category=data["カテゴリ"].text.strip(),
            content_html=str(data["本文"]),
            publication_period=publication_period,
            files=files
        )

    @staticmethod
    def __get_files(unipa: Unipa,
                    check_files_id: str) -> List[UnipaBulletinBoardFile]:
        """
        掲示に添付されているファイル一覧を取得

        Args:
            unipa: Unipa オブジェクト
            check_files_id: 「添付資料を確認」ボタンの ID

        Returns:
            List[UnipaBulletinBoardFile]: 掲示に添付されているファイル一覧
        """
        soup = unipa.request("BULLETBOARD", check_files_id, {
            "javax.faces.source": check_files_id,
            "javax.faces.partial.execute": check_files_id
        }, "html5lib")
        file_list_area = soup.select_one("div.fileListArea")
        if file_list_area is None:
            return []
        form_id = file_list_area.find_parent("form").get("name")

        files = []
        rows = file_list_area.select("div.tableDownloadRow")
        for row in rows:
            raw_filename = row.select_one("div.fileListCell").text.strip()  # ファイルサイズも含まれているので注意
            filename = re.sub("(.+)\\([0-9]+[a-zA-Z]+\\)", r"\1", raw_filename)

            # わけがわからないが、ファイルダウンロード時には一つめのボタンのIDを使って事前リクエスト、その後実リクエストでファイルが得られるらしい
            item_id = row.find_all("button")[0].get("id")
            file_id = row.find_all("button")[1].get("id")

            files.append(UnipaBulletinBoardFile(filename, form_id, item_id, file_id))

        return files

    def mark_read(self,
                  unipa: Unipa) -> None:
        """
        既読にする
        """
        raise NotImplementedError("未実装です。")  # TODO

    def mark_unread(self,
                    unipa: Unipa) -> None:
        """
        未読にする
        """
        raise NotImplementedError("未実装です。")  # TODO

    def mark_flag(self,
                  unipa: Unipa) -> None:
        """
        フラグをつける
        """
        raise NotImplementedError("未実装です。")  # TODO

    def mark_unflag(self,
                    unipa: Unipa) -> None:
        """
        フラグをはずす
        """
        raise NotImplementedError("未実装です。")  # TODO

    def __str__(self) -> str:
        return f"BulletinBoardItem(title={self.title}, " \
               f"target_s={self.target_s}, " \
               f"target_p={self.target_p}, " \
               f"is_attention={self.is_attention}, " \
               f"is_flag={self.is_flag}, " \
               f"is_unread={self.is_unread})"
