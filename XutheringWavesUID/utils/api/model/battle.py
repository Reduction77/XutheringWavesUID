from typing import Dict, List, Union, Optional

from pydantic import Field, BaseModel, model_validator


# 定义角色模型
class AbyssRole(BaseModel):
    roleId: int
    iconUrl: Optional[str] = None


# 定义楼层模型
class AbyssFloor(BaseModel):
    floor: int
    picUrl: str
    star: int
    roleList: Optional[List[AbyssRole]] = None


# 定义区域模型
class AbyssArea(BaseModel):
    areaId: int
    areaName: str
    star: int
    maxStar: int
    floorList: Optional[List[AbyssFloor]] = None


# 定义难度模型
class AbyssDifficulty(BaseModel):
    difficulty: int
    difficultyName: str
    towerAreaList: List[AbyssArea]


# 定义顶层模型
class AbyssChallenge(BaseModel):
    isUnlock: bool
    seasonEndTime: Optional[int]
    difficultyList: Optional[List[AbyssDifficulty]]


class ChallengeRole(BaseModel):
    roleName: str
    roleHeadIcon: str
    roleLevel: int


class Challenge(BaseModel):
    challengeId: int
    bossHeadIcon: str
    bossIconUrl: str
    bossLevel: int
    bossName: str
    passTime: int
    difficulty: int
    roles: Optional[List[ChallengeRole]] = None


class ChallengeArea(BaseModel):
    challengeInfo: Dict[str, List[Challenge]]
    open: bool = False
    isUnlock: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_depending_on_unlock(cls, data):
        """根据 isUnlock 状态预处理数据"""
        if isinstance(data, dict):
            if not data.get("isUnlock", False):
                # 创建一个新的数据字典，只保留基本字段
                new_data = {"isUnlock": False, "open": data.get("open", False)}

                # 将 areaId 和 areaName 设置为 None
                new_data["areaId"] = None
                new_data["areaName"] = None

                # 创建一个空的 challengeInfo 字典
                new_data["challengeInfo"] = {}

                return new_data

        return data


class ExploreItem(BaseModel):
    name: str
    progress: int
    type: int
    icon: Optional[str] = None


class AreaInfo(BaseModel):
    areaId: int
    areaName: str
    areaProgress: int
    itemList: List[ExploreItem]


class ExploreCountry(BaseModel):
    countryId: int
    countryName: str
    detailPageFontColor: str
    detailPagePic: str
    detailPageProgressColor: str
    homePageIcon: str


class ExploreArea(BaseModel):
    areaInfoList: Union[List[AreaInfo], None] = None
    country: ExploreCountry
    countryProgress: str


class ExploreList(BaseModel):
    """探索度"""

    exploreList: Union[List[ExploreArea], None] = None
    open: bool


class SlashRole(BaseModel):
    iconUrl: str  # 角色头像
    roleId: int  # 角色ID


class SlashHalf(BaseModel):
    buffDescription: str  # 描述
    buffIcon: str  # 图标
    buffName: str  # 名称
    buffQuality: int  # 品质
    roleList: List[SlashRole]  # 角色列表
    score: int  # 分数


class SlashChallenge(BaseModel):
    challengeId: int  # 挑战ID
    challengeName: str  # 挑战名称
    halfList: List[Optional[SlashHalf]] = Field(default_factory=list)  # 半场列表
    rank: Optional[str] = Field(default="")  # 等级
    score: int  # 分数

    @model_validator(mode="before")
    @classmethod
    def filter_null_halves(cls, data):
        if isinstance(data, dict) and "halfList" in data:
            data["halfList"] = [h for h in data["halfList"] if h is not None]
        return data

    def get_rank(self):
        if not self.rank:
            return ""
        return self.rank.lower()


class SlashDifficulty(BaseModel):
    allScore: int  # 总分数
    challengeList: List[SlashChallenge] = Field(default_factory=list)  # 挑战列表
    difficulty: int  # 难度
    difficultyName: str  # 难度名称
    homePageBG: str  # 首页背景
    maxScore: int  # 最大分数
    teamIcon: str  # 团队图标


class SlashDetail(BaseModel):
    """冥海"""

    isUnlock: bool  # 是否解锁
    seasonEndTime: int  # 赛季结束时间
    difficultyList: List[SlashDifficulty] = Field(default_factory=list)  # 难度列表
