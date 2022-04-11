"""
公開期間情報 (掲示板掲示用)
"""
import datetime
from typing import Optional


class UnipaPublicationPeriod:
    """
    公開期間情報 (掲示板掲示用)
    """

    def __init__(self,
                 start_date: Optional[datetime.datetime],
                 end_date: Optional[datetime.datetime]):
        """
        公開期間情報 (掲示板掲示用) を生成する。

        Args:
            start_date: 公開開始日
            end_date: 公開終了日
        """
        self._start_date = start_date
        self._end_date = end_date

    @property
    def start_date(self) -> Optional[datetime.datetime]:
        """
        公開開始日

        Returns:
            Optional[datetime.datetime]: 公開開始日
        """
        return self._start_date

    @property
    def end_date(self) -> Optional[datetime.datetime]:
        """
        公開終了日

        Returns:
            Optional[datetime.datetime]: 公開終了日
        """
        return self._end_date
