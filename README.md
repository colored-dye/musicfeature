## 数据: `data/`

1. all-half.pre.full压缩一半-原来的数据

2. all-half.pre.full压缩一半-和声生成
    
3. 暂时替代all-half.pre.full压缩一半-旋律生成


## 代码: `src/`

0. 通用函数: 处理输入，提取旋律、调性等 -- `parse_input.py`

    不能直接运行。

1. 节奏模式 -- `1_rhythm_pattern.py`

    修改该文件中的数据文件名，如下。必须是第三类数据。

    ```python
    input_3 = parse_input("../data/3.txt", 3)
    ```

    *运行*：
    ```
    python3 1_rhythm_pattern.py
    ```

    e.g: [(0, 44), (7, 16), (7, 12), (9, 4), (7, 12), (5, 4), (4, 16), (0, 8), (2, 4), (4, 4), (5, 12), (7, 4), (5, 12), (4, 4), (2, 16), (7, 16), (4, 12), (5, 4), (4, 12), (2, 4), (0, 16), (4, 16), (9, 4)]

2. 音乐轮廓 -- `2_music_contour.py`

    修改入口函数处的数据文件名，如下：

    ```python
    input_3 = parse_input("../data/3.txt", 3)
    ```

    *运行*：

    ```
    python3 2_music_contour.py
    ```

    e.g: [(101, 0), 1, 1]
