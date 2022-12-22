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
        e.g: [(0, 44), (7, 16), (7, 12), (9, 4), (7, 12), (5, 4), (4, 16), (0, 8), (2, 4), (4, 4), (5, 12), (7, 4), (5, 12), (4, 4), (2, 16), (7, 16), (4, 12), (5, 4), (4, 12), (2, 4), (0, 16), (4, 16), (9, 4), (9, 8), (11, 4), (0, 12), (2, 4), (11, 16), (7, 16), (7, 12), (9, 4), (7, 12), (5, 4), (4, 16), (0, 8), (2, 4), (4, 4), (5, 12), (7, 4), (5, 12), (4, 4), (2, 16), (7, 16), (4, 12), (5, 4), (4, 12), (2, 4), (0, 12), (2, 4), (4, 12), (7, 4), (9, 4), (9, 8), (0, 16), (11, 4), (0, 16), (7, 16), (7, 12), (9, 4), (7, 12), (5, 4), (4, 16), (0, 8), (2, 4), (4, 4), (5, 12), (7, 4), (5, 12), (4, 4), (2, 16), (7, 16), (4, 12), (5, 4), (4, 12), (2, 4), (0, 16), (4, 16), (9, 4)]

    某旋律音符的节奏模式:
        (相对音高, 持续时长).
    """
    tonality_all_1d = expand_2d_to_1d(tonalities_2d)
    rp = []
    cnt = 0
    for melody in melodies_2d:
        m, t = melody

        rp.append(
            (m - tonality_to_root_note(tonality_all_1d[cnt], m), t)
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
