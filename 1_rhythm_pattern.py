from parse_input import (
    tonality_2d_to_1d,
    parse_input,
    tonality_to_root_note,
    type3_all_two_dimension_tonality,
)


def rhythm_pattern(tonality: list, melody: list) -> list:
    """节奏模式
    Input: 调性,旋律二维序列
    Output: 对旋律中每个音符的节奏模式列表
        某个音符的节奏模式:
        [相对音高, 起始位置, 持续时长]
    """
    rp = []

    return rp

if __name__ == "__main__":
    input_3 = parse_input("./data/3.txt", 3)

    tonality_all_2d = type3_all_two_dimension_tonality(input_3)
    tonality_all_1d = tonality_2d_to_1d(tonality_all_2d)
    # print(tonality_to_root_note(tonality_all_1d[256], melody_all[256]))
    # print(melody_all[256])
