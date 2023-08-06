from psdelivery.core.item import ProblemItem
from psdelivery.crawlers.baekjoon.difficulty import BaekjoonProblemDifficultyConverter


class BaekjoonProblemItem(ProblemItem):
    difficulty_converter = BaekjoonProblemDifficultyConverter
