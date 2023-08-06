from typing import Tuple, final
from enum import Enum
from abc import ABCMeta


WebsiteDifficultyRange = Tuple[float, float]

@final
class ProblemDifficulty(Enum):
    BEGINNER = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4
    NOT_RATED = -1

class ProblemDifficultyConverter(metaclass=ABCMeta):
    beginner: WebsiteDifficultyRange
    easy: WebsiteDifficultyRange
    normal: WebsiteDifficultyRange
    hard: WebsiteDifficultyRange
    extreme: WebsiteDifficultyRange

    @final
    @staticmethod
    def is_difficulty( 
            website_difficulty: float,           
            difficulty_range: WebsiteDifficultyRange,
    ) -> bool:
        return difficulty_range[0] <= website_difficulty <= difficulty_range[1]

    @final
    @classmethod
    def convert(cls, website_difficulty: float) -> ProblemDifficulty:
        if cls.is_difficulty(website_difficulty, cls.beginner):
            return ProblemDifficulty.BEGINNER
        if cls.is_difficulty(website_difficulty, cls.easy):
            return ProblemDifficulty.EASY
        if cls.is_difficulty(website_difficulty, cls.normal):
            return ProblemDifficulty.NORMAL
        if cls.is_difficulty(website_difficulty, cls.hard):
            return ProblemDifficulty.HARD
        if cls.is_difficulty(website_difficulty, cls.extreme):
            return ProblemDifficulty.EXTREME
        return ProblemDifficulty.NOT_RATED
