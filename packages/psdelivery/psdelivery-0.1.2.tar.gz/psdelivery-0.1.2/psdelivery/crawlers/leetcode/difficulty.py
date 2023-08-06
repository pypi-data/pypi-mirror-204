from psdelivery.core.difficulty import ProblemDifficultyConverter


class LeetcodeProblemDifficultyConverter(ProblemDifficultyConverter):
    beginner = (0, 0)
    easy = (1, 1)
    normal = (2, 2)
    hard = (3, 3)
    extreme = (4, 9999)
