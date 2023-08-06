from abc import ABCMeta
from typing import Type

from psdelivery.core.difficulty import ProblemDifficulty, ProblemDifficultyConverter


class ProblemItem(metaclass=ABCMeta):
    seq: str
    title: str
    problem_site: str
    difficulty: ProblemDifficulty
    difficulty_converter: Type[ProblemDifficultyConverter]

    def __init__(self, 
                 seq: str, 
                 title: str, 
                 problem_site: str, 
                 website_difficulty: float):
        self.seq = seq
        self.title = title
        self.problem_site = problem_site
        self.difficulty = self.difficulty_converter.convert(website_difficulty)

    @property
    def __dict__(self):
        return {
            'seq': self.seq,
            'title': self.title,
            'problem_site': self.problem_site,
            'difficulty': self.difficulty.value,
        }
