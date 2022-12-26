from typing import (List, Tuple)

from parse_input import (
    parse_input,
    expand_2d_to_1d,
    type2_get_all_chord,
    type3_get_all_melody,

)

import numpy as np

INVALID_CHORD_NOTE = 114514

def music_contour(melodies_2d: list) -> List[Tuple[list, list, list]]:
    """音乐轮廓

    用最高/低点, 整体上升/下降趋势, 凹凸性描述.

    e.g: [(101, 0), 1, 1]

    Input:
        - melodies: 来自第三类数据的旋律二维序列

    Output:
        [最高/低点, 整体上升(1)/下降(-1), 凹(-1)/凸(1)/非凹非凸(0)]
    """

    # 二维旋律转换为一维旋律
    melodies_1d = expand_2d_to_1d(melodies_2d)

    # 最高/低点
    melody_max = np.max(melodies_1d)
    melody_min = np.min(melodies_1d)

    # 整体趋势
    if melodies_1d[0] <= melodies_1d[-1]:
        trend = 1
    else:
        trend = -1

    # 凹凸性
    if melody_max == melodies_1d[0] or \
            melody_max == melodies_1d[-1] or \
            melody_min == melodies_1d[0] or \
            melody_min == melodies_1d[-1]:
        if melody_max > melodies_1d[0] and melody_max > melodies_1d[-1]:
            # 凸
            convex = 1
        elif melody_min < melodies_1d[0] and melody_min < melodies_1d[-1]:
            # 凹
            convex = -1
        else:
            convex = 0
    else:
        convex = 0
    
    return [(melody_max, melody_min), trend, convex]    

    
def min_note_in_chord_sequence(chords) -> int:
    """和弦序列中最低的音
    """
    ret = INVALID_CHORD_NOTE
    for c in chords:
        if len(c) != 0:
            ret = min(ret, c[0])
    return ret

if __name__ == "__main__":
    # input_2 = parse_input("../data/2.txt", 2)
    input_3 = parse_input("../data/3.txt", 3)

    # 只看前256
    # input_2 = input_2[:1]
    # input_3 = input_3[:1]

    # 提取和弦和旋律
    # chord_all = type2_get_all_chord(input_2)
    melody_all_2d = type3_get_all_melody(input_3)

    mc = music_contour(melody_all_2d)

    # 将音乐旋律的文本形式写入文件
    import os
    if not os.path.exists("../output"):
        os.makedirs("../output")
    with open("../output/music_contour.txt", "w", encoding='utf-8') as fp:
        fp.write(str(mc))

    # 作图，展示LL和LH的变化趋势
    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.plot(mc[0][0])
    # plt.plot(mc[1][0])
    # fig = plt.gcf()
    # if not os.path.exists("../imgs"):
    #     os.makedirs("../imgs")
    # fig.savefig("../imgs/LL_LH.png", format='png', dpi=600)
