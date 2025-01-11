"""
聚合已有的几个较好的IDS版本。

过滤：
1. 排除使用扩展汉字、部首的IDS
2. 排除无法解析，使用特殊符号代替的IDS
3. 排除等于本字的IDS

选择：
优先选择长度短且在几个版本中出现次数多且靠前的作为IDS

版本：
不考虑一个字在不同地区的差异
"""

from pathlib import Path
import logging
import re

import pandas as pd

UNICODE_MAP = {
    # [英文说明，中文说明，字数, [起始序号, 终止序号], [空字符序号]]
    # unihan数据
    "cjk-basic": ["CJK Unified Ideographs", "基本汉字", "20902字", [0x4E00, 0x9FA5]],
    "cjk-basic2": [
        "CJK Unified Ideographs Supplement",
        "基本汉字补充",
        "90字",
        [0x9FA6, 0x9FFF],
    ],
    "cjk-ext-a": [
        "CJK Unified Ideographs Extension A",
        "扩展A",
        "6592字",
        [0x3400, 0x4DBF],
    ],
    "cjk-ext-b": [
        "CJK Unified Ideographs Extension B",
        "扩展B",
        "42720字",
        [0x20000, 0x2A6DF],
    ],
    "cjk-ext-c": [
        "CJK Unified Ideographs Extension C",
        "扩展C",
        "4154字",
        [0x2A700, 0x2B739],
    ],
    "cjk-ext-d": [
        "CJK Unified Ideographs Extension D",
        "扩展D",
        "222字",
        [0x2B740, 0x2B81D],
    ],
    "cjk-ext-e": [
        "CJK Unified Ideographs Extension E",
        "扩展E",
        "5762字",
        [0x2B820, 0x2CEA1],
    ],
    "cjk-ext-f": [
        "CJK Unified Ideographs Extension F",
        "扩展F",
        "7473字",
        [0x2CEB0, 0x2EBE0],
    ],
    "cjk-ext-g": [
        "CJK Unified Ideographs Extension G",
        "扩展G",
        "4939字",
        [0x30000, 0x3134A],
    ],
    "cjk-ext-h": [
        "CJK Unified Ideographs Extension H",
        "扩展H",
        "4192字",
        [0x31350, 0x323AF],
    ],
    "cjk-ext-i": [
        "CJK Unified Ideographs Extension I",
        "扩展I",
        "622字",
        [0x2EBF0, 0x2EE5D],
    ],
    "cjk-ci": [
        "CJK Compatibility Ideographs",
        "兼容汉字",
        "472字",
        [0xF900, 0xFAD9],
        [0xFA6E, 0xFA6F],
    ],  # FA6E、FA6F 为空
    "cjk-cis": [
        "CJK Compatibility Ideographs Supplement",
        "兼容扩展",
        "542字",
        [0x2F800, 0x2FA1D],
    ],
    # 不在unihan
    "cjk-ling": ["Number Zero", "〇", "1字", [0x3007, 0x3007]],
    "cjk-more-kx": ["Kangxi Radicals", "康熙部首", "214字", [0x2F00, 0x2FD5]],
    "cjk-more-radical": [
        "CJK Radicals Supplement",
        "部首扩展",
        "115字",
        [0x2E80, 0x2EF3],
        [0x2E9A],
    ],  # 2E9A为空
    "cjk-more-stroke": ["CJK Strokes", "汉字笔画", "36字", [0x31C0, 0x31E3]],
    "cjk-more-desc": [
        "Ideographic Description Characters",
        "汉字结构",
        "16字",
        [0x2FF0, 0x2FFF],
    ],
    "cjk-more-bpmf": ["Bopomofo", "汉语注音", "43字", [0x3105, 0x312F]],
    "cjk-more-bpmf-ext": ["Extended Bopomofo", "注音扩展", "32字", [0x31A0, 0x31BF]],
    # 私用区
    "pua1a": ["Private Use Area", "", "", [0xE000, 0xF8FF]],
    "pua1b": ["High Private Use Area", "", "", [0xDB80, 0xDBFF]],
    "pua2a": ["Supplemntary Private Use Area-A", "", "", [0xF0000, 0xFFFFF]],
    "pua2b": ["Supplemntary Private Use Area-B", "", "", [0x100000, 0x10FFFF]],
}


IDS_SYMBOL = "⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻"
INCLUDE_SYMBOL = """
㇀㇁㇂㇄㇅㇇㇈㇉㇊㇋㇌㇍㇎㇏㇐㇒㇓㇕㇘㇛㇝㇞㇢㇣
⺀⺁⺄⺆⺇⺈⺊⺌⺍⺕⺜⺝⺥⺧⺩⺪⺬⺮⺳⺴⺵⺶⺷⺸⺻⺼⺽⻊⻎⻕⻗
"""

KEYS = [
    "cjk-ling",
    "cjk-basic",
    "cjk-basic2",
    "cjk-ext-a",
    "cjk-ext-b",
    "cjk-ext-c",
    "cjk-ext-d",
    "cjk-ext-e",
    "cjk-ext-f",
    "cjk-ext-g",
    "cjk-ext-h",
    "cjk-ext-i",
]


def clean_ids(ids, pattern_cjk, pattern_ids):
    ids = [
        v
        for v in ids
        if len(v) > 1
        and re.sub(pattern_cjk, "", v) == ""
        and re.findall(pattern_ids, v)
    ]
    return list(dict.fromkeys(ids)) if len(ids) > 0 else ids


def get_cjk_pattern():
    pattern = ""
    for key in KEYS:
        val = UNICODE_MAP[key]
        start_index, end_index = val[3]
        c1, c2 = chr(start_index), chr(end_index)
        pattern += c1 if start_index == end_index else f"{c1}-{c2}"
    more = (IDS_SYMBOL + INCLUDE_SYMBOL).strip().replace("\n", "")
    pattern_hanzi = rf"[{pattern}{more}]+"
    return pattern_hanzi


def create_chars():
    out = []
    for key in KEYS:
        val = UNICODE_MAP[key]
        en_name, zh_name, count, [start_index, end_index] = val[:4]
        ignores = val[4] if len(val) == 5 else []
        for index in range(start_index, end_index + 1):
            if index in ignores:
                continue
            code = "U+" + hex(index).split("0x")[-1].upper()
            char = chr(index)
            out.append([code, char])
    return out


def get_bablestone(file_path, pattern_cjk, pattern_ids, translation_table):
    out = []
    with open(file_path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            code, char, rest_raw = line.split("\t", 2)
            rest = rest_raw.translate(translation_table)
            ids = []
            for v in rest.split("^"):
                if "$" in v:
                    ids.append(v.split("$")[0])
            ids = clean_ids(ids, pattern_cjk, pattern_ids)
            out.append([code, char, ids, rest_raw])
    return out


def get_chise(dir_path, pattern_cjk, pattern_ids, translation_table):
    out = []
    files = Path(dir_path).glob("IDS-UCS-*.txt")
    files = sorted(files)
    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "" or line.startswith(";;"):
                    continue
                code, char, rest_raw = line.split("\t", 2)
                rest = rest_raw.translate(translation_table)
                ids = []
                for v in re.split(r"[\t]", rest):
                    ids.append(v)
                ids = clean_ids(ids, pattern_cjk, pattern_ids)
                code = code.replace("U-000", "U+")
                out.append([code, char, ids, rest_raw])
    return out


def get_cjkvi_ids(file_path, pattern_cjk, pattern_ids, translation_table):
    out = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            code, char, rest_raw = line.split("\t", 2)
            rest = rest_raw.translate(translation_table)
            ids = []
            for v in rest.split("\t"):
                ids.append(v.split("[")[0])
            ids = clean_ids(ids, pattern_cjk, pattern_ids)
            out.append([code, char, ids, rest_raw])
    return out


def get_yibai_ids(file_path, pattern_cjk, pattern_ids, translation_table):
    out = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            char, rest_raw = line.split("\t", 1)
            rest = rest_raw.translate(translation_table)
            ids = []
            for v in re.split(r"[;\t]", rest):
                v = re.sub(r"[.a-z]+", "", v.split("(")[0])
                ids.append(v)
            ids = clean_ids(ids, pattern_cjk, pattern_ids)
            code = hex(ord(char)).split("0x")[-1].upper()
            out.append([code, char, ids, rest_raw])
    return out


def get_candidate(x, cols):
    candidates = {}
    for col in cols:
        if len(x[col]) == 0:
            continue
        for i, v in enumerate(x[col]):
            if v in candidates:
                candidates[v].append(i)
            else:
                candidates[v] = [i]
    # 优先长度短的，选择排序靠前且次数多
    out = sorted(
        candidates.items(),
        key=lambda x: (len(x[0]), min(x[1]), sum(x[1]) / len(x[1]), -len(x[1])),
    )
    return [o[0] for o in out]


def run(save_dir):
    save_dir = Path(save_dir)
    if not save_dir.exists():
        logging.info(f"Create dir ={save_dir}")
        save_dir.mkdir(parents=True)

    logging.info("Read char map")
    df_map = pd.read_csv("char-map.tsv", sep="\t")
    col1, col2 = df_map.columns[:2]
    df_map2 = df_map[df_map[col2].notnull()][[col1, col2]].copy()
    df_map2 = df_map2.set_index(col1)

    logging.info("Create chars")
    chars = create_chars()
    df = pd.DataFrame(chars, columns=["code", "char"])
    logging.info(f"df = {len(df)}, {df['char'].nunique()}")
    assert len(df) == df["char"].nunique()

    # logging.info("Save to file")
    # df.to_csv(save_dir / "out.tsv", index=False, sep="\t")

    pattern_cjk = get_cjk_pattern()
    pattern_ids = rf"[{IDS_SYMBOL}]"
    logging.info(f"pattern = {pattern_cjk}")
    out = re.sub(pattern_cjk, "", "".join(df_map2[col2]))
    assert len(out) == 0
    out = re.findall(pattern_cjk, "".join(df_map2.index))
    logging.info(f"out = {out}")
    assert len(out) == 0

    logging.info("Create translation_table")
    translation_table = str.maketrans(df_map2[col2].to_dict())

    files = [
        "./cjkvi-ids/ids.txt",
        "./babelstone-ids/IDS.TXT",
        "./chise-ids/",
        "./yibai-ids/ids_lv0.txt",
    ]
    func_list = [
        get_cjkvi_ids,
        get_bablestone,
        get_chise,
        get_yibai_ids,
    ]
    logging.info("Read file data")
    data = [
        fn(file, pattern_cjk, pattern_ids, translation_table)
        for fn, file in zip(func_list, files)
    ]

    logging.info(f"Data = {[len(d) for d in data]}")

    df_list = [pd.DataFrame(d, columns=["code", "char", "ids", "raw"]) for d in data]

    logging.info("merge df")
    cols = []
    df2 = df
    for i, dfx in enumerate(df_list):
        col_new = f"ids-{i}"
        cols.append(col_new)
        t = dfx[["char", "ids"]]
        t.columns = ["char", col_new]
        t = t.drop_duplicates(["char"])
        # assert len(t) == t['char'].nunique()
        df2 = df2.merge(t, how="left")

    logging.info(f"Extract candidate, cols = {cols}")
    df2["candidate"] = (
        df2[cols].fillna("").apply(lambda x: get_candidate(x, cols), axis=1)
    )
    df2["ids"] = df2["candidate"].apply(lambda x: x[0] if x else "")
    df2["more"] = df2["candidate"].apply(lambda x: "/".join(x[1:]) if x else "")

    save_file = save_dir / "ids.tsv"
    logging.info(f"Save IDS to {save_file}")
    df_out = df2[["code", "char", "ids", "more"]]
    df_out.to_csv(save_file, index=False, sep="\t")


if __name__ == "__main__":
    fmt = "%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)

    save_dir = "temp"
    run(save_dir)
