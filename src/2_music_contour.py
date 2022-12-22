from typing import (List, Tuple)

from parse_input import (
    parse_input,
    expand_2d_to_1d,
    type2_get_all_chord,
    type3_get_all_melody,

)

import numpy as np
# import matplotlib.pyplot as plt

INVALID_CHORD_NOTE = 114514

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

    # 二维旋律转换为一维旋律
    melodies_1d = expand_2d_to_1d(melodies_2d)
    # 分段
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

        # 可能出现一大串空和弦, 令其最低音为默认值0
        if min_chord_note == INVALID_CHORD_NOTE:
            min_chord_note = 0
        LL.append(min_melody_note - min_chord_note)
        LH.append(max_melody_note - min_chord_note)

    # 一阶导数
    for i in range(len(LL)):
        if i == 0:
            dLL.append(0)
            dLH.append(0)
        else:
            dLL.append(LL[i] - LL[i-1])
            dLH.append(LH[i] - LH[i-1])

    # 二阶导数
    for i in range(len(dLL)):
        if i == 0:
            ddLL.append(0)
            ddLH.append(0)
        else:
            ddLL.append(dLL[i] - dLL[i-1])
            ddLH.append(dLH[i] - dLH[i-1])

    return [
        (LL, dLL, ddLL),
        (LH, dLH, ddLH),
    ]

def music_partition(chords_1d: list, melodies_1d: list, melody_n: int = 64) -> Tuple[list]:
    """将和弦和旋律按照4小节为粒度计算最高音和最低音.

    频率采样频率为64分音符的时值. 和弦采样频率是旋律采样频率的1/16.

    4小节为16拍, 对应256个旋律音符和16个和弦.

    日后可以替换此函数的逻辑, 根据乐理分割.

    Input:
        - chords_1d: 第二类数据的和弦序列
        - melodies_2d: 第三类数据的旋律一维序列
        - melody_n: 分割粒度的旋律音符个数

    Output: 输出(和弦, 旋律)
        [(chords, melodies), ...]
    """
    partition = []
    print("旋律长度: %d" % len(melodies_1d))
    partition_number = len(melodies_1d)//melody_n
    if len(melodies_1d) % melody_n != 0:
        print("切分粒度不能被整除! 去掉尾巴就可以吃了~")
        melodies_1d = melodies_1d[:partition_number*melody_n]
        print("旋律长度更新为: %d" % len(melodies_1d))

    for i in range(partition_number):
        partition.append(
            (
                chords_1d[i*melody_n//16:(i+1)*melody_n//16],
                melodies_1d[i*melody_n:(i+1)*melody_n]
            )
        )

    return partition

def min_note_in_chord_sequence(chords) -> int:
    """和弦序列中最低的音
    """
    ret = INVALID_CHORD_NOTE
    for c in chords:
        if len(c) != 0:
            ret = min(ret, c[0])
    return ret

if __name__ == "__main__":
    input_2 = parse_input("../data/2.txt", 2)
    input_3 = parse_input("../data/3.txt", 3)

    # 提取和弦和旋律
    chord_all = type2_get_all_chord(input_2)
    melody_all_2d = type3_get_all_melody(input_3)

    mc = music_contour(chord_all, melody_all_2d)

    # 将音乐旋律的文本形式写入文件
    import os
    if not os.path.exists("../output"):
        os.makedirs("../output")
    with open("../output/music_contour.txt", "w", encoding='utf-8') as fp:
        fp.write(str(mc))

    # 作图，展示LL和LH的变化趋势
    # plt.figure()
    # plt.plot(mc[0][0])
    # plt.plot(mc[1][0])
    # fig = plt.gcf()
    # if not os.path.exists("../imgs"):
    #     os.makedirs("../imgs")
    # fig.savefig("../imgs/LL_LH.png", format='png', dpi=600)
