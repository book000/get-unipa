"""
掲示板
"""
from unipa import Unipa


class BulletinBoardItemDetails:
    """
    掲示板の掲示アイテム 詳細情報
    """
    pass


class BulletinBoardItem:
    """
    掲示板の掲示アイテム
    """

    def __init__(self,
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
            title: 掲示タイトル
            target_s: 掲示 s 値 (リクエスト用)
            target_p: 掲示 p 値 (リクエスト用)
            flag_id: フラグ ID
            unread_id: 未読 ID
            is_attention: 注目フラグ (投稿者によって設定)
            is_flag: フラグ (ユーザーが設定可能)
            is_unread: 未読か (ユーザーが設定可能)
        """
        self._title = title
        self._target_s = target_s
        self._target_p = target_p
        self._flag_id = flag_id
        self._unread_id = unread_id
        self._is_attention = is_attention
        self._is_flag = is_flag
        self._is_unread = is_unread

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
                    unipa: Unipa) -> BulletinBoardItemDetails:
        """
        掲示アイテムの詳細を取得します。

        Returns:
            BulletinBoardItemDetails: 掲示アイテムの詳細
        """
        soup = unipa.request("funcForm", {
            "javax.faces.partial.execute": self.target_s,
            self.target_s: self.target_p
        })

        return BulletinBoardItemDetails()

    def mark_read(self,
                  unipa: Unipa) -> None:
        """
        既読にする
        """
        soup = unipa.request("funcForm", {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": self.target_s,
            "javax.faces.partial.execute": self.target_s,
            "javax.faces.partial.render": "funcForm:tabArea",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
        }, "lxml")
        pass  # TODO

    def mark_unread(self,
                    unipa: Unipa) -> None:
        """
        未読にする
        """
        soup = unipa.request("funcForm", {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": self.target_s,
            "javax.faces.partial.execute": self.target_s,
            "javax.faces.partial.render": "funcForm:tabArea",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "funcForm:tabArea_activeIndex": "1",
            self.unread_id: "on"
        }, "lxml")
        pass  # TODO

    def mark_flag(self,
                  unipa: Unipa) -> None:
        """
        フラグをつける
        """
        pass  # TODO

    def mark_unflag(self,
                    unipa: Unipa) -> None:
        """
        フラグをはずす
        """
        pass  # TODO

    def __str__(self) -> str:
        return f"BulletinBoardItem(title={self.title}, target_s={self.target_s}, target_p={self.target_p}, is_attention={self.is_attention}, is_flag={self.is_flag}, is_unread={self.is_unread})"
