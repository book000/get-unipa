"""
テスト関連モデル
"""

from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ConfigJsonModel:
    """
    設定JSONモデル
    """
    base_url: str
    username: str
    password: str

    def __init__(self) -> None:
        pass


@dataclass_json
@dataclass
class BulletinBoardGetAllModel:
    """
    掲示板リスト取得テストモデル
    """
    title: str
    target_s: str
    target_p: str
    flag_id: str
    unread_id: str
    is_attention: bool
    is_flag: bool
    is_unread: bool

    def __init__(self) -> None:
        pass


@dataclass_json
@dataclass
class PublicationPeriodModel:
    """
    公開期間モデル
    """
    start_date: str
    end_date: str

    def __init__(self) -> None:
        pass


@dataclass_json
@dataclass
class BulletinBoardGetDetailsModel:
    """
    掲示詳細取得テストモデル
    """
    title: str
    author: str
    category: str
    content_html: str
    publication_period: PublicationPeriodModel

    def __init__(self) -> None:
        pass


@dataclass_json
@dataclass
class TestsJsonModel:
    """
    テスト用JSONモデル
    """
    bulletinboard_get_all: List[BulletinBoardGetAllModel]
    bulletinboard_get_details: List[BulletinBoardGetDetailsModel]

    def __init__(self) -> None:
        pass
