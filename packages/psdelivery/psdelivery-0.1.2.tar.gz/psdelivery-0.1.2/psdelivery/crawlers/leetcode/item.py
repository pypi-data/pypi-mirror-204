from psdelivery.core.item import ProblemItem
from psdelivery.crawlers.leetcode.difficulty import LeetcodeProblemDifficultyConverter

class LeetcodeProblemItem(ProblemItem):
    difficulty_converter = LeetcodeProblemDifficultyConverter
