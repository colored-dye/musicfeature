"""处理数据输入:
- 三类数据文本转列表
- 旋律提取
- 调性根音计算
"""

#
# 外部函数
#

def parse_input(filename: str, type: int) -> list:
    """ type:
    1: 第一类.
    2: 第二类.
    3: 第三类.
    """
    if type == 1:
        return type1_input(filename)
    elif type == 2:
        return type2_input(filename)
    elif type == 3:
        return type3_input(filename)

def type3_concat_all_melody(inputs: list) -> list:
    """将第三类输入的二维旋律扩展为一维
    """
    ret = []
    melody = [l[3] for l in inputs]
    for pairs in melody:
        for m in pairs:
            ret.extend([m[0]] * m[1])
    return ret

def tonality_to_root_note(tonality: str, pitch: int) -> int:
    """获取一个MIDI音符在某调性下的根音
    """
    MIDDLE = {
        'C' : 60,
        'D' : 62,
        'E' : 64,
        'F' : 65,
        'G' : 67,
        'A' : 69,
        'B' : 71,
    }
    note_name, _ = tonality.split('.')
    root = MIDDLE[note_name]
    while root > pitch:
        root -= 12
    # while root < pitch:
    #     root += 12
    return root

def type3_all_two_dimension_tonality(inputs: list) -> list:
    """从第三类数据中提取所有的二维调性
    """
    tonality = []
    for one_line in inputs:
        tonality.extend(one_line[1])
    return tonality

def tonality_2d_to_1d(tonality: list) -> list:
    """将第二类和第三类数据中的二维(调性,出现次数)的列表展开为一维
    """
    ret = []
    for t in tonality:
        ret.extend([t[0]] * t[1])
    return ret

#
# 内部函数
#

def type1_input(filename: str) -> list:
    """第一类.
    [0, 0, 0, 0]|C.MAJOR|[]|[0]|[0, 0, 0, 0]|[31, 33, 38]|[0]
    (1) 采样旋律
    (2) 调性
    (3) 和弦
    (4) 权重特征
    (5) 权重音
    (6) 结构和弦
    (7) 终止和弦
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            melody_0 = eval(line_sep[0])
            tonality_1 = line_sep[1]
            chord_2 = eval(line_sep[2])
            weight_feature_3 = eval(line_sep[3])
            weight_note_4 = eval(line_sep[4])
            structure_chord = eval(line_sep[5])
            end_chord = eval(line_sep[6])
            ret.append([melody_0, tonality_1, chord_2, weight_feature_3, weight_note_4, structure_chord, end_chord])
    return ret

def two_dimension_input_tonality(raw: str) -> list:
    """解析字符串为二维调性列表
    """
    tonality = []
    raw = raw[2:-2]
    raw_split = raw.split('), (')
    for t in raw_split:
        pair = t.split(', ')
        tonality.append((pair[0], int(pair[1])))
    return tonality

def type2_input(filename: str) -> list:
    """第二类.
    [((0, 0), 256)]|[(C.MAJOR, 32), (D.MINOR, 16), (C.MAJOR, 208)]|[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 67, 67, 67, 79, 79, 79, 81, 79, 79, 79, 77, 76, 76, 76, 76, 72, 72, 74, 76, 77, 77, 77, 79, 77, 77, 77, 76, 74, 74, 74, 74, 67, 67, 67, 67, 76, 76, 76, 77, 76, 76, 76, 74, 72, 72, 72, 72, 76, 76, 76, 76, 69]|[[],[],[],[],[48, 52, 55],[48, 52, 55],后面省略10个和弦]|[96, 208]
    (1) VA标签,持续时长
    (2) (调性1,连续出现次数*16), (调性2,连续出现次数*16), ...
    (3) 采样旋律
    (4) 和弦
    (5) 乐句的分割点/和弦终止式的结束点
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            va_time_0 = eval(line_sep[0])
            tonality_1 = two_dimension_input_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            chord_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, chord_3, terminate_4])
    return ret

def type3_input(filename: str) -> list:
    """第三类.
    [((0, 0), 256)]|[(C.MAJOR, 32), (D.MINOR, 16), (C.MAJOR, 208)]|[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 67, 67, 67, 79, 79, 79, 81, 79, 79, 79, 77, 76, 76, 76, 76, 72, 72, 74, 76, 77, 77, 77, 79, 77, 77, 77, 76, 74, 74, 74, 74, 67, 67, 67, 67, 76, 76, 76, 77, 76, 76, 76, 74, 72, 72, 72, 72, 76, 76, 76, 76, 69]|[(67, 2)，(79, 4)，(81, 12)……..]|[96, 208]
    (1) VA标签,持续时长
    (2) (调性1,连续出现次数*16), (调性2,连续出现次数*16), ...
    (3) 采样旋律
    (4) 二维旋律,64分音符(?待定)
    (5) 乐句的分割点/和弦终止式的结束点
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            va_time_0 = eval(line_sep[0])
            tonality_1 = two_dimension_input_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            two_dim_rhythm_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, two_dim_rhythm_3, terminate_4])
    return ret
