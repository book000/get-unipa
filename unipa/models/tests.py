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


@dataclass_json
@dataclass
class TestsJsonModel:
    """
    テスト用JSONモデル
    """
    bulletinboard_get_all: List[BulletinBoardGetAllModel]