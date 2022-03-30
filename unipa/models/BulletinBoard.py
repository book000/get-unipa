"""
掲示板
"""


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
                 target_t: str,
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
            target_t: 掲示 t 値 (リクエスト用)
            flag_id: フラグ ID
            unread_id: 未読 ID
            is_attention: 注目フラグ (投稿者によって設定)
            is_flag: フラグ (ユーザーが設定可能)
            is_unread: 未読か (ユーザーが設定可能)
        """
        self._title = title
        self._target_s = target_s
        self._target_t = target_t
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
    def target_t(self) -> str:
        """
        掲示 t 値 (リクエスト用)

        Returns:
            str: 掲示 t 値 (リクエスト用)
        """
        return self._target_t

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

    def get_details(self) -> BulletinBoardItemDetails:
        """
        掲示アイテムの詳細を取得します。

        Returns:
            BulletinBoardItemDetails: 掲示アイテムの詳細
        """
        pass  # TODO

    def mark_read(self) -> None:
        """
        既読にする
        """
        pass  # TODO

    def mark_unread(self) -> None:
        """
        未読にする
        """
        pass  # TODO

    def mark_flag(self) -> None:
        """
        フラグをつける
        """
        pass  # TODO

    def mark_unflag(self) -> None:
        """
        フラグをはずす
        """
        pass  # TODO

    def __str__(self) -> str:
        return f"BulletinBoardItem(title={self.title}, target_s={self.target_s}, target_t={self.target_t}, is_attention={self.is_attention}, is_flag={self.is_flag}, is_unread={self.is_unread})"
