# 字段格式：[英文说明，中文说明，字数, [起始序号, 终止序号], [空字符序号]]
UNICODE_HANZI_MAP = {
    # unihan数据
    "cjk-basic": ["CJK Unified Ideographs", "基本汉字", "20902字", [0x4E00, 0x9FA5]],
    "cjk-suppl": ["CJK Unified Ideographs Supplement", "基本汉字补充", "90字", [0x9FA6, 0x9FFF]],
    "cjk-ext-a": ["CJK Unified Ideographs Extension A", "扩展A", "6592字", [0x3400, 0x4DBF]],
    "cjk-ext-b": ["CJK Unified Ideographs Extension B", "扩展B", "42720字", [0x20000, 0x2A6DF]],
    "cjk-ext-c": ["CJK Unified Ideographs Extension C", "扩展C", "4154字", [0x2A700, 0x2B739]],
    "cjk-ext-d": ["CJK Unified Ideographs Extension D", "扩展D", "222字", [0x2B740, 0x2B81D]],
    "cjk-ext-e": ["CJK Unified Ideographs Extension E", "扩展E", "5762字", [0x2B820, 0x2CEA1]],
    "cjk-ext-f": ["CJK Unified Ideographs Extension F", "扩展F", "7473字", [0x2CEB0, 0x2EBE0]],
    "cjk-ext-g": ["CJK Unified Ideographs Extension G", "扩展G", "4939字", [0x30000, 0x3134A]],
    "cjk-ext-h": ["CJK Unified Ideographs Extension H", "扩展H", "4192字", [0x31350, 0x323AF]],
    "cjk-ext-i": ["CJK Unified Ideographs Extension I", "扩展I", "622字", [0x2EBF0, 0x2EE5D]],
    # unihan兼容汉字
    "cjk-comp-basic": ["CJK Compatibility Ideographs", "兼容汉字", "472字", [0xF900, 0xFAD9], [0xFA6E, 0xFA6F]],
    "cjk-comp-suppl": ["CJK Compatibility Ideographs Supplement","兼容扩展","542字",[0x2F800, 0x2FA1D]],
    # 不在unihan
    "cjk-ling": ["Number Zero", "〇", "1字", [0x3007, 0x3007]],
    "cjk-more-kx": ["Kangxi Radicals", "康熙部首", "214字", [0x2F00, 0x2FD5]],
    "cjk-more-radical": ["CJK Radicals Supplement", "部首扩展", "115字", [0x2E80, 0x2EF3], [0x2E9A]],
    "cjk-more-stroke": ["CJK Strokes", "汉字笔画", "36字", [0x31C0, 0x31E3]],
    "cjk-more-desc": ["Ideographic Description Characters", "汉字结构", "16字", [0x2FF0, 0x2FFF]],
    "cjk-more-bpmf": ["Bopomofo", "汉语注音", "43字", [0x3105, 0x312F]],
    "cjk-more-bpmf-ext": ["Extended Bopomofo", "注音扩展", "32字", [0x31A0, 0x31BF]],
}

UNICODE_PUA_MAP = {
    # 私用区
    "pua-1a": ["Private Use Area", "", "", [0xE000, 0xF8FF]],
    "pua-1b": ["High Private Use Area", "", "", [0xDB80, 0xDBFF]],
    "pua-2a": ["Supplemntary Private Use Area-A", "", "", [0xF0000, 0xFFFFF]],
    "pua-2b": ["Supplemntary Private Use Area-B", "", "", [0x100000, 0x10FFFF]],
}

# MORE_RADICALS = "⺀⺁⺄⺆⺇⺈⺊⺌⺍⺕⺜⺝⺥⺧⺩⺪⺬⺮⺳⺴⺵⺶⺷⺸⺻⺼⺽⻊⻎⻕⻗"
