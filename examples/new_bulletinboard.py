"""
新しい掲示を取得する
"""
import json
import os

from unipa import Unipa
from unipa.BulletinBoard import UnipaBulletinBoard
from unipa.models.tests import ConfigJsonModel


def main() -> None:
    """
    メイン処理: 新しい掲示を取得する
    """
    if not os.path.exists("config.json"):
        raise Exception("テストに必要なファイル config.json が見つかりません")

    with open("config.json", encoding="utf-8") as f:
        config: ConfigJsonModel = ConfigJsonModel.from_json(f.read())  # type: ignore

    unipa = Unipa(config.base_url)
    unipa.login(config.username, config.password)

    bulletinboard = UnipaBulletinBoard(unipa)
    items = bulletinboard.get_all()

    already = []
    if os.path.exists("examples/new_bulletinboard.json"):
        with open("examples/new_bulletinboard.json", "r") as f:
            already = json.load(f)

    for item in items:
        if item.title in already:
            continue

        print("NEW ITEM: ", item.title)

        already.append(item.title)

    with open("examples/new_bulletinboard.json", "w") as f:
        json.dump(already, f)


if __name__ == '__main__':
    main()
