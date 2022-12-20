from parse_input import (
    tonality_2d_to_1d,
    parse_input,
    tonality_to_root_note,
    type3_all_two_dimension_tonality,
    type3_get_all_melody,
)


def rhythm_pattern(tonalities: list, melodies: list, n: int) -> list:
    """节奏模式\n
    Input:
        - 一维调性: ['C.MAJOR', 'C.MAJOR', ...]
        - 二维旋律: [(11, 4), (5, 14), ...]
        - n: n分音符. 如64分音符, 则n=64.\n
    Output:
        旋律中每个音符的节奏模式列表.\n
    某个音符的节奏模式:
        [相对音高, 起始位置, 持续时长(单位: 拍)]
    """
    rp = []
    for melody in melodies:
        m, t = melody
        for _ in range(t):
            rp_0_relative_pitch = m - tonality_to_root_note(tonalities[len(rp)], m)
            rp_1_start_position = len(rp)
            rp_2_duration = t / n
            rp.append([rp_0_relative_pitch, rp_1_start_position, rp_2_duration])

    return rp

if __name__ == "__main__":
    input_3 = parse_input("../data/3.txt", 3)

    tonality_all_2d = type3_all_two_dimension_tonality(input_3)
    tonality_all_1d = tonality_2d_to_1d(tonality_all_2d)
    melody_all_2d = type3_get_all_melody(input_3)

    with open("../rhythm_pattern.txt", "w", encoding='utf-8') as fp:
        fp.write(str(rhythm_pattern(tonality_all_1d, melody_all_2d, 64)))
