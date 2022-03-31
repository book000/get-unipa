"""
テストデータ作成
"""
import logging
import os
from typing import List

from unipa import Unipa
from unipa.BulletinBoard import UnipaBulletinBoard
from unipa.models.tests import BulletinBoardGetAllModel, ConfigJsonModel, TestsJsonModel


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
        bulletinboard_get_all = self.get_bulletinboard_get_all()

        return TestsJsonModel(
            bulletinboard_get_all=bulletinboard_get_all,
        )

    def get_bulletinboard_get_all(self) -> List[BulletinBoardGetAllModel]:
        """
        掲示板 掲示リスト
        """
        ret = []

        items = UnipaBulletinBoard(self.unipa).get_all()
        for item in items:
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


def main() -> None:
    """
    テストデータ作成 メイン関数
    """
    GenerateTestData()


if __name__ == '__main__':
    main()
