"""
クラス
"""
import re
from typing import List

from unipa import Unipa
from unipa.Classes.UnipaClass import UnipaClass, UnipaClassLectureAt


class UnipaClasses:
    """
    クラス
    """

    def __init__(self,
                 unipa: Unipa):
        """
        コンストラクタ
        """
        self.unipa = unipa
        self.logger = unipa.logger

    def get_all(self) -> List[UnipaClass]:
        """
        履修中の全クラスを取得する
        """

        info_item = next(filter(lambda x: x.name == "クラスプロファイル", self.unipa.get_info_items()))
        soup = self.unipa.request_from_info(info_item)

        yobi_panels = soup.select(".yobiContArea")
        classes = []
        for yobi_panel in yobi_panels:
            day_of_week = yobi_panel.find("span", {"class": "ui-panel-title"}).text
            period_of_time_elements = yobi_panel.select("div.classJigen")
            class_lists = yobi_panel.select("div.classList")
            for period_of_time_element, class_list in zip(period_of_time_elements, class_lists):
                match = re.search(r"\d+", period_of_time_element.text)
                if match is None:
                    continue
                period_of_time = int(match.group()) if match is not None else None
                class_elements = class_list.select("div.ui-outputpanel")

                lecture_at = UnipaClassLectureAt(day_of_week, period_of_time)
                for class_element in class_elements:
                    a_tag = class_element.find("a")

                    name = a_tag.text
                    internal_id = a_tag.get("id")
                    class_raw = class_element.text
                    match = re.search("\\(([A-Za-z0-9]+)\\)", class_raw)
                    class_id = match.group(1) if match is not None else None

                    classes.append(UnipaClass(name, internal_id, class_id, lecture_at))

        return classes
