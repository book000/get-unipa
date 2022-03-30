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
                 is_attention: bool,
                 is_flag: bool,
                 is_unread: bool):
        """
        掲示板の掲示アイテム コンストラクタ

        Args:
            title: 掲示タイトル
            is_attention: 注目フラグ (投稿者によって設定)
            is_flag: フラグ (ユーザーが設定可能)
            is_unread: 未読か (ユーザーが設定可能)
        """
        self.title = title
        self.target_s = target_s
        self.target_t = target_t
        self.is_attention = is_attention
        self.is_flag = is_flag
        self.is_unread = is_unread

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
