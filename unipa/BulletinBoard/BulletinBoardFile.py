"""
掲示板 掲示添付ファイル
"""
import os

from unipa import Unipa


class UnipaBulletinBoardFile:
    """
    掲示板 掲示添付ファイル
    """

    def __init__(self,
                 filename: str,
                 form_id: str,
                 item_id: str,
                 file_id: str):
        """
        コンストラクタ

        Args:
            filename: ファイル名
            form_id: フォーム ID
            item_id: ファイル ID
            file_id: アイテム ID

        Notes:
            UNIPAでは、どうもファイルダウンロード前に一回事前リクエストを挟まないと実ファイルがダウンロードできないらしい。<br>
            get-unipa では、事前リクエストで使うIDを item_id 、実ファイルのダウンロードで使うIDを file_id として扱う。
        """
        self._filename = filename
        self._form_id = form_id
        self._item_id = item_id
        self._file_id = file_id

    @property
    def filename(self) -> str:
        """
        ファイル名 (拡張子付き)

        Returns:
            str: ファイル名
        """
        return self._filename

    @property
    def form_id(self) -> str:
        """
        フォーム ID

        Returns:
            str: フォーム ID
        """
        return self.form_id

    @property
    def item_id(self) -> str:
        """
        アイテム ID

        Returns:
            str: ファイル ID
        """
        return self._item_id

    @property
    def file_id(self) -> str:
        """
        ファイル ID

        Returns:
            str: ファイル ID
        """
        return self._file_id

    def download(self,
                 unipa: Unipa,
                 filepath: str) -> None:
        """
        ファイルをダウンロードする

        Notes:
            ファイルタイトルをファイルパスに設定する場合は {filename} を使ってください。
        """
        filepath = os.path.abspath(filepath)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        filepath = filepath.replace("{filename}", self._filename)

        unipa.request("BULLETBOARD", self._form_id, {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": self._item_id,
            "javax.faces.partial.execute": "@all",
            self._item_id: self._item_id,
        }, "lxml")

        unipa.download("BULLETBOARD", self._form_id, {
            self._file_id: self._file_id,
        }, filepath)

    def __str__(self) -> str:
        return f"UnipaBulletinBoardFile(title={self._filename}, " \
               f"form_id={self._form_id}, " \
               f"item_id={self._item_id}, " \
               f"file_id={self._file_id})"
