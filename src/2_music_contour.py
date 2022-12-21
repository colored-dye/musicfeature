from typing import (List, Tuple)

from parse_input import (
    parse_input,
    expand_2d_to_1d,
    type2_get_all_chord,
    type3_get_all_melody,
    
)

import numpy as np

def music_contour(chords: list, melodies_2d: list) -> List[Tuple[list, list, list]]:
    """音乐轮廓

    以小节为单位确定旋律线和低音线的轮廓，使用极大/小值及其对应的一阶导数、二阶导数描述

    int LL[]: 每小节的最低音, int LH[]: 每小节的最高音.
    d(LL) = [LL[i] - LL[i-1]], d(LH) = [LH[i] - LH[i-1]]
    dd(LL) = [d(LL)[i] - d(LL)[i-1]], dd(LH) = [d(LH)[i] - d(LH)[i-1]]

    Input:
        - chords: 来自第二类数据的和弦序列
        - melodies: 来自第三类数据的旋律二维序列

    Output:
        [
            (LL, d(LL), dd(LL)),
            (LH, d(LH), dd(LH)),
        ]

    TODO: 曲式结构划分?
    """
    mc = []

    melodies_1d = expand_2d_to_1d(melodies_2d)
    partitions = music_partition(chords, melodies_1d)
    LL = []
    LH = []
    dLL = []
    dLH = []
    ddLL = []
    ddLH = []
    for p in partitions:
        chords = p[0]
        melodies = p[1]
        min_chord_note = min_note_in_chord_sequence(chords)
        min_melody_note = np.min(melodies)
        max_melody_note = np.max(melodies)
        LL.append(min_melody_note - min_chord_note)
        LH.append(max_melody_note - min_chord_note)
    return mc

def music_partition(chords_1d: list, melodies_1d: list, melody_n: int = 64) -> Tuple[list]:
    """将和弦和旋律按照4小节为粒度计算最高音和最低音.

    频率采样频率为64分音符的时值. 和弦采样频率是旋律采样频率的1/16.

    4小节为16拍, 对应256个旋律音符和16个和弦.

    Input:
        - chords_1d: 第二类数据的和弦序列
        - melodies_2d: 第三类数据的旋律一维序列
        - melody_n: 分割粒度的旋律音符个数
    """
    partition = []
    print("len(melody): %d"%len(melodies_1d))
    if len(melodies_1d) % melody_n != 0:
        for i in range(len(melodies_1d)//melody_n):
            partition.append(
                (
                    chords_1d[i*melody_n//16:(i+1)*melody_n//16], 
                    melodies_1d[i*melody_n:(i+1)*melody_n]
                )
            )
    else:
        print("切分粒度不能被整除! 懒得处理了QwQ")

    return partition

def min_note_in_chord_sequence(chords) -> int:
    """和弦序列中最低的音
    """
    ret = 114514
    for c in chords:
        ret = min(ret, c[0])
    return ret


if __name__ == "__main__":
    input_2 = parse_input("../data/2.txt", 2)
    input_3 = parse_input("../data/3.txt", 3)

    chord_all = type2_get_all_chord(input_2)
    melody_all_2d = type3_get_all_melody(input_3)

    with open("../music_contour.txt", "w", encoding='utf-8') as fp:
        fp.write(str(music_contour(chord_all, melody_all_2d)))
