"""
掲示板の掲示アイテム 詳細情報
"""
from unipa.BulletinBoard.PublicationPeriod import UnipaPublicationPeriod


class UnipaBulletinBoardItemDetails:
    """
    掲示板の掲示アイテム 詳細情報

    Notes:
        get-unipa ではコンテンツ内容のプレーンテキスト化はしていません。`content_html` プロパティで HTML をそのまま返すため、Markdown などへの変換は利用側で実施してください。
    """

    def __init__(self,
                 item_id: str,
                 title: str,
                 author: str,
                 category: str,
                 content_html: str,
                 publication_period: UnipaPublicationPeriod):
        """
        コンストラクタ

        Args:
            item_id: 掲示 ID (恒久的なIDではないことに注意)
            title: 掲示タイトル
            author: 差出人
            category: カテゴリ
            content_html: コンテンツ HTML
            publication_period: 公開期間
        """
        self._item_id = item_id
        self._title = title
        self._author = author
        self._category = category
        self._content_html = content_html
        self._publication_period = publication_period

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
    def author(self) -> str:
        """
        差出人

        Returns:
            str: 差出人
        """
        return self._author

    @property
    def category(self) -> str:
        """
        カテゴリ

        Returns:
            str: カテゴリ
        """
        return self._category

    @property
    def content_html(self) -> str:
        """
        コンテンツ HTML

        Returns:
            str: コンテンツ HTML
        """
        return self._content_html

    @property
    def publication_period(self) -> UnipaPublicationPeriod:
        """
        公開期間

        Returns:
            PublicationPeriod: 公開期間
        """
        return self._publication_period

    def __str__(self) -> str:
        return f"UnipaBulletinBoardItemDetails(title={self._title}, author={self._author}, category={self._category}, content_html={self._content_html}, publication_period={self._publication_period})"
