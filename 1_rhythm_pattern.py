from parse_input import \
    type3_all_tonality, \
    parse_input, \
    tonality_to_root_note

def rhythm_pattern():
    rp = []

    return rp

if __name__ == "__main__":
    input_3 = parse_input("./data/3.txt", 3)
    tonality_all = type3_all_tonality(input_3, 1)
    print(tonality_to_root_note(tonality_all[0]), )
