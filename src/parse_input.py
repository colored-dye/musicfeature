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
    print("Reading data from `%s' ..." % filename, end='')
    data = None
    if type == 1:
        data = _type1_input(filename)
    elif type == 2:
        data = _type2_input(filename)
    elif type == 3:
        data = _type3_input(filename)
    print("finished")
    return data

def type2_get_all_chord(inputs: list) -> list:
    """拼接第二类输入中所有的和弦

    e.g: [[], [], [], [], [48, 52, 55], [48, 52, 55], [48, 52, 55], [48, 52, 55], [50, 53, 57], [50, 53, 57], [55, 59, 62], [55, 59, 62], [48, 52, 55], [48, 52, 55], [48, 52, 55], [48, 52, 55]]
    """
    chord_2d = []
    for l in inputs:
        chord_2d.extend(l[3])
    return chord_2d

def type3_get_all_melody(inputs: list) -> list:
    """拼接第三类输入中所有的二维旋律

    e.g: [(0,44), (67,16), (79,12), (81,4), (79,12), (77,4), (76,16), (72,8), (74,4), (76,4), (77,12), (79,4), (77,12), (76,4), (74,16), (67,16), (76,12), (77,4), (76,12), (74,4), (72,16), (76,16), (69,4)]
    """
    melody_2d = []
    for l in inputs:
        melody_2d.extend(l[3])
    return melody_2d

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
    note_name, _ = tonality.split('.') # 大/小调不管, 只看根音
    if len(note_name) == 1:
        root = MIDDLE[note_name]
    else:
        # 有降调, 'B', 如DB.MAJOR
        root = MIDDLE[note_name[0]] - 1
    while root > pitch:
        root -= 12
    return root

def type3_all_two_dimension_tonality(inputs: list) -> list:
    """从第三类数据中提取所有的二维调性
    """
    tonality = []
    for one_line in inputs:
        tonality.extend(one_line[1])
    return tonality

def expand_2d_to_1d(tonality: list) -> list:
    """将第二类和第三类数据中的二维列表展开为一维
    """
    ret = []
    for t in tonality:
        ret.extend([t[0]] * t[1])
    return ret

#
# 内部函数
#

def _type1_input(filename: str) -> list:
    """第一类.

    [0, 0, 0, 0]|C.MAJOR|[]|[0]|[0, 0, 0, 0]|[31, 33, 38]|[0]

    1. 采样旋律
    2. 调性
    3. 和弦
    4. 权重特征
    5. 权重音
    6. 结构和弦
    7. 终止和弦
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

def _two_dimension_input_tonality(raw: str) -> list:
    """解析字符串为二维调性列表
    """
    tonality = []
    raw = raw[2:-2]
    raw_split = raw.split('), (')
    for t in raw_split:
        pair = t.split(', ')
        tonality.append((pair[0], int(pair[1])))
    return tonality

def _type2_input(filename: str) -> list:
    """第二类.

    [((0, 0), 256)]|[(C.MAJOR, 32), (D.MINOR, 16), (C.MAJOR, 208)]|[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 67, 67, 67, 79, 79, 79, 81, 79, 79, 79, 77, 76, 76, 76, 76, 72, 72, 74, 76, 77, 77, 77, 79, 77, 77, 77, 76, 74, 74, 74, 74, 67, 67, 67, 67, 76, 76, 76, 77, 76, 76, 76, 74, 72, 72, 72, 72, 76, 76, 76, 76, 69]|[[],[],[],[],[48, 52, 55],[48, 52, 55],后面省略10个和弦]|[96, 208]

    1. VA标签,持续时长
    2. (调性1,连续出现次数*16), (调性2,连续出现次数*16), ...
    3. 采样旋律
    4. 和弦
    5. 乐句的分割点/和弦终止式的结束点
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            va_time_0 = eval(line_sep[0])
            tonality_1 = _two_dimension_input_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            chord_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, chord_3, terminate_4])
    return ret

def _type3_input(filename: str) -> list:
    """第三类.

    [((0, 0), 256)]|[(C.MAJOR, 32), (D.MINOR, 16), (C.MAJOR, 208)]|[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67, 67, 67, 67, 79, 79, 79, 81, 79, 79, 79, 77, 76, 76, 76, 76, 72, 72, 74, 76, 77, 77, 77, 79, 77, 77, 77, 76, 74, 74, 74, 74, 67, 67, 67, 67, 76, 76, 76, 77, 76, 76, 76, 74, 72, 72, 72, 72, 76, 76, 76, 76, 69]|[(67, 2)，(79, 4)，(81, 12)……..]|[96, 208]

    1. VA标签,持续时长
    2. (调性1,连续出现次数*16), (调性2,连续出现次数*16), ...
    3. 采样旋律
    4. 二维旋律,64分音符(?待定)
    5. 乐句的分割点/和弦终止式的结束点
    """
    ret = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            line_sep = line.split('|')
            va_time_0 = eval(line_sep[0])
            tonality_1 = _two_dimension_input_tonality(line_sep[1])
            rhythm_2 = eval(line_sep[2])
            two_dim_rhythm_3 = eval(line_sep[3])
            terminate_4 = eval(line_sep[4])
            ret.append([va_time_0, tonality_1, rhythm_2, two_dim_rhythm_3, terminate_4])
    return ret
