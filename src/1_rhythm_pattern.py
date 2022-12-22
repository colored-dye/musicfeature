from parse_input import (
    expand_2d_to_1d,
    parse_input,
    tonality_to_root_note,
    type3_all_two_dimension_tonality,
    type3_get_all_melody,
)


def rhythm_pattern(tonalities_2d: list, melodies_2d: list) -> list:
    """节奏模式

    Input:
        - tonalities_2d: 二维调性. e.g: ['C.MAJOR', 'C.MAJOR', ...]
        - melodies_2d: 二维旋律. e.g: [(11, 4), (5, 14), ...]

    Output:
        旋律中每个音符的节奏模式列表.
        e.g: [(0, 0, 44), (7, 44, 16), (7, 60, 12), (9, 72, 4), (7, 76, 12), (5, 88, 4), (4, 92, 16), (0, 108, 8), (2, 116, 4), (4, 120, 4), (5, 124, 12), (7, 136, 4), (5, 140, 12), (4, 152, 4), (2, 156, 16), (7, 172, 16), (4, 188, 12), (5, 200, 4), (4, 204, 12), (2, 216, 4), (0, 220, 16), (4, 236, 16), (9, 252, 4)]

    某旋律音符的节奏模式:
        (相对音高, 起始位置, 持续时长).
    """
    tonality_all_1d = expand_2d_to_1d(tonalities_2d)
    rp = []
    cnt = 0
    for melody in melodies_2d:
        m, t = melody

        rp.append(
            (m - tonality_to_root_note(tonality_all_1d[cnt], m), cnt, t)
        )

        cnt += t

    return rp

if __name__ == "__main__":
    input_3 = parse_input("../data/3.txt", 3)

    # 提取调性和旋律
    tonality_all_2d = type3_all_two_dimension_tonality(input_3)
    melody_all_2d = type3_get_all_melody(input_3)

    # 将节奏模式的文本形式写入文件
    import os
    if not os.path.exists("../output"):
        os.makedirs("../output")
    with open("../output/rhythm_pattern.txt", "w", encoding='utf-8') as fp:
        fp.write(str(rhythm_pattern(tonality_all_2d, melody_all_2d)))
