def parse_input(filename: str, type: int):
    """ type:
    1: 第一类.
    2: 第二类.
    3: 第三类.
    """
    if type == 1:
        return input_type1(filename)
    elif type == 2:
        return input_type2(filename)
    elif type == 3:
        return input_type3(filename)

def input_type1(filename: str):
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

def input_type2_tonality(raw: str):
    tonality = []
    raw = raw[2:-2]
    raw_split = raw.split('), (')
    for t in raw_split:
        pair = t.split(', ')
        tonality.append((pair[0], pair[1]))
    return tonality

def input_type2(filename: str):
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
            tonality_1 = input_type2_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            chord_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, chord_3, terminate_4])
    return ret

def input_type3(filename: str):
    """第三类.
    [((0, 0), 256)]|[(C.MAJOR, 32), (D.MINOR, 16), (C.MAJOR, 208)]|[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 67, 67, 67, 79, 79, 79, 81, 79, 79, 79, 77, 76, 76, 76, 76, 72, 72, 74, 76, 77, 77, 77, 79, 77, 77, 77, 76, 74, 74, 74, 74, 67, 67, 67, 67, 76, 76, 76, 77, 76, 76, 76, 74, 72, 72, 72, 72, 76, 76, 76, 76, 69]|[(0, 44),(67, 16),(79, 12),(81, 4),(79, 12),(77, 4),(76, 16),(72, 8),(74, 4),(76, 4),(77, 12),(79, 4),(77, 12),(76, 4),(74, 16),(67, 16),(76, 12),(77, 4),(76, 12),(74, 4),(72, 16),(76, 16),(69, 4)]|[96, 208]
    (1) VA标签,持续时长
    (2) (调性1,连续出现次数*16), (调性2,连续出现次数*16), ...
    (3) 采样旋律
    (4) 二维旋律64分音符: (连续出现的旋律1, 出现的次数*4), (连续出现的旋律2, 出现的次数*4)...
    (5) 乐句的分割点/和弦终止式的结束点
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            va_time_0 = eval(line_sep[0])
            tonality_1 = input_type2_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            two_dim_rhythm_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, two_dim_rhythm_3, terminate_4])
    return ret
