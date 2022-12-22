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
        e.g: [(0, 0, 44), (0, 1, 44), (0, 2, 44), (0, 3, 44), (0, 4, 44), (0, 5, 44), (0, 6, 44), (0, 7, 44), (0, 8, 44),...]

    某个旋律音符的节奏模式:
        (相对音高, 起始位置, 持续时长).
    """
    tonality_all_1d = expand_2d_to_1d(tonalities_2d)
    rp = []
    for melody in melodies_2d:
        m, t = melody
        for _ in range(t):
            rp_0_relative_pitch = m - tonality_to_root_note(tonality_all_1d[len(rp)], m)
            rp_1_start_position = len(rp)
            rp_2_duration = t
            rp.append(
                (rp_0_relative_pitch, rp_1_start_position, rp_2_duration)
            )

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
