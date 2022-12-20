from typing import (List, Tuple)

from parse_input import (
    parse_input,
)

def music_contour(tonalities: list, melodies: list) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """音乐轮廓\n
    以小节为单位确定旋律线和低音线的轮廓，使用极大/小值及其对应的一阶导数、二阶导数描述\n
    int LL[]: 每小节的最低音, int LH[]: 每小节的最高音.\n
    d(LL) = [LL[i] - LL[i-1]], d(LH) = [LH[i] - LH[i-1]]\n
    dd(LL) = [d(LL)[i] - d(LL)[i-1]], dd(LH) = [d(LH)[i] - d(LH)[i-1]]\n
    Input:
        - tonalities: 调性一维序列
        - melodies: 旋律一维序列\n
    Output:
        (
            (LL, d(LL), dd(LL)),
            (LH, d(LH), dd(LH)),
        )
    TODO: 曲式结构划分?\n
    """

if __name__ == "__main__":
    input_3 = parse_input("../data/3.txt", 3)
