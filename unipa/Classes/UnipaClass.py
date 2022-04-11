"""
クラス 基本情報

クラスプロファイルより取得
"""
from typing import Optional


class UnipaClassLectureAt:
    """
    クラス 曜日・時限情報
    """

    def __init__(self,
                 day_of_week: str,
                 period_of_time: Optional[int]):
        """

        Args:
            day_of_week: 実施曜日 (月曜日 etc or 集中講義 or 実習)
            period_of_time: 実施時限 (数値)
        """
        self._day_of_week = day_of_week
        self._period_of_time = period_of_time

    @property
    def day_of_week(self) -> str:
        """
        実施曜日 (月曜日 etc or 集中講義 or 実習)

        Returns:
            str: 実施曜日 (月曜日 etc or 集中講義 or 実習)
        """
        return self._day_of_week

    @property
    def period_of_time(self) -> Optional[int]:
        """
        実施時限 (数値)

        Returns:
            Optional[int]: 実施時限 (数値)
        """
        return self._period_of_time

    def __str__(self) -> str:
        return f"UnipaClassLectureAt(day_of_week={self._day_of_week}, period_of_time={self._period_of_time})"


class UnipaClass:
    """
    クラス 基本情報
    """

    def __init__(self,
                 class_internal_id: str,
                 name: str,
                 class_id: Optional[str],
                 lecture_at: UnipaClassLectureAt):
        """
        コンストラクタ

        Args:
            class_internal_id: クラス内部ID
            name: クラス名
            class_id: クラスID (表示されている数値)
            lecture_at: 実施曜日・時限
        """
        self._class_internal_id = class_internal_id
        self._name = name
        self._class_id = class_id
        self._lecture_at = lecture_at

    @property
    def class_internal_id(self) -> str:
        """
        クラス内部ID

        Returns:
            str: クラス内部ID
        """
        return self._class_internal_id

    @property
    def name(self) -> str:
        """
        クラス名

        Returns:
            str: クラス名
        """
        return self._name

    @property
    def class_id(self) -> Optional[str]:
        """
        クラスID (表示されている数値)

        Returns:
            Optional[str]: クラスID (表示されている数値)
        """
        return self._class_id

    @property
    def lecture_at(self) -> UnipaClassLectureAt:
        """
        実施曜日・時限

        Returns:
            UnipaClassLectureAt: 実施曜日・時限
        """
        return self._lecture_at

    def __str__(self) -> str:
        return f"UnipaClass(class_internal_id={self._class_internal_id}, " \
               f"name={self._name}, " \
               f"class_id={self._class_id}, " \
               f"lecture_at={self._lecture_at})"
