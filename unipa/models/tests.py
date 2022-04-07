"""
テスト関連モデル
"""

from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
# noinspection PyClassHasNoInit
class ConfigJsonModel:
    """
    設定JSONモデル
    """
    base_url: str
    username: str
    password: str


@dataclass_json
@dataclass
# noinspection PyClassHasNoInit
class BulletinBoardGetAllModel:
    """
    掲示板リスト取得テストモデル
    """
    item_id: str
    title: str
    target_s: str
    target_p: str
    flag_id: str
    unread_id: str
    is_attention: bool
    is_flag: bool
    is_unread: bool


@dataclass_json
@dataclass
# noinspection PyClassHasNoInit
class PublicationPeriodModel:
    """
    公開期間モデル
    """
    start_date: str
    end_date: str


@dataclass_json
@dataclass
# noinspection PyClassHasNoInit
class BulletinBoardGetDetailsModel:
    """
    掲示詳細取得テストモデル
    """
    item_id: str
    title: str
    author: str
    category: str
    content_html: str
    publication_period: PublicationPeriodModel


@dataclass_json
@dataclass
# noinspection PyClassHasNoInit
class TestsJsonModel:
    """
    テスト用JSONモデル
    """
    bulletinboard_get_all: List[BulletinBoardGetAllModel]
    bulletinboard_get_details: List[BulletinBoardGetDetailsModel]
