"""
テストデータ作成
"""
import logging
import os
from typing import List

from unipa import Unipa
from unipa.BulletinBoard import UnipaBulletinBoard, UnipaBulletinBoardItem
from unipa.models.tests import BulletinBoardGetAllModel, BulletinBoardGetDetailsModel, ConfigJsonModel, \
    PublicationPeriodModel, TestsJsonModel


class GenerateTestData:
    """
    テストデータ作成
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        if not os.path.exists("config.json"):
            raise Exception("テストに必要なファイル config.json が見つかりません")

        with open("config.json", encoding="utf-8") as f:
            self.config: ConfigJsonModel = ConfigJsonModel.from_json(f.read())  # type: ignore

        self.unipa = Unipa(self.config.base_url)
        self.unipa.login(self.config.username, self.config.password)

        self.logger.info("テストデータを作成します")
        with open("tests.json", "w", encoding="utf-8") as f:
            f.write(self.generate().to_json(ensure_ascii=False, indent=4))  # type: ignore

    def generate(self) -> TestsJsonModel:
        """

        Returns:

        """
        bulletinboard_items = UnipaBulletinBoard(self.unipa).get_all()
        bulletinboard_get_all = self.get_bulletinboard_get_all(bulletinboard_items)
        bulletinboard_get_details = self.get_bulletinboard_get_details(bulletinboard_items)

        return TestsJsonModel(
            bulletinboard_get_all=bulletinboard_get_all,
            bulletinboard_get_details=bulletinboard_get_details,
        )

    @classmethod
    def get_bulletinboard_get_all(cls,
                                  bulletinboard_items: List[UnipaBulletinBoardItem]) -> List[BulletinBoardGetAllModel]:
        """
        掲示板 掲示リスト

        Args:
            bulletinboard_items (List[UnipaBulletinBoardItem]): UnipaBulletinBoard.get_all
        """
        ret = []

        for item in bulletinboard_items:
            ret.append(BulletinBoardGetAllModel(
                title=item.title,
                target_s=item.target_s,
                target_p=item.target_p,
                flag_id=item.flag_id,
                unread_id=item.unread_id,
                is_attention=item.is_attention,
                is_flag=item.is_flag,
                is_unread=item.is_unread,
            ))

        return ret

    def get_bulletinboard_get_details(self,
                                      bulletinboard_items: List[UnipaBulletinBoardItem]) -> List[
        BulletinBoardGetDetailsModel]:
        """
        掲示板 掲示詳細
        """
        ret = []

        for item in bulletinboard_items:
            details = item.get_details(self.unipa)
            day_of_week = '月火水木金土日'
            ret.append(BulletinBoardGetDetailsModel(
                title=details.title,
                author=details.author,
                category=details.category,
                content_html=details.content_html,
                publication_period=PublicationPeriodModel(
                    start_date=details.publication_period.start_date.strftime("%Y/%m/%d(DAYOFWEEK) %H:%M")
                        .replace("DAYOFWEEK", day_of_week[details.publication_period.start_date.weekday()]),
                    end_date=details.publication_period.end_date.strftime("%Y/%m/%d(DAYOFWEEK) %H:%M")
                        .replace("DAYOFWEEK", day_of_week[details.publication_period.end_date.weekday()]),
                )
            ))

        return ret


def main() -> None:
    """
    テストデータ作成 メイン関数
    """
    GenerateTestData()


if __name__ == '__main__':
    main()
