from psdelivery.core.difficulty import ProblemDifficultyConverter


class BaekjoonProblemDifficultyConverter(ProblemDifficultyConverter):
    beginner = (1, 3)
    easy = (4, 7)
    normal = (8, 12)
    hard = (13, 17)
    extreme = (18, 9999)
