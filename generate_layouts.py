#!/usr/bin/python3

# This is called automatically by the build process to generate some
# layouts that are similar to other layouts.

import os
import pathlib
import sys

NAME = "name"
SOURCE = "source"
# simple string replacement
REPLACE = "replace"
# remove "map key scancode KEYCODE" by scancode
REMOVE_SCANCODES = "remove_scancodes"
# remove "key KEYCODE { ... } " by KEYCODE
REMOVE_KEYCODES = "remove_keycodes"
ADD = "add"

# complex replacement
# replace only within keycode
REPL_KEYCODE = "repl_keycode"
# prev string
REPL_OLD = "repl_old"
# replacement string
REPL_NEW = "repl_new"
# do not replace if line contains:
REPL_SKIP = "repl_skip"


DAN_SWE_REPLACE = [
    ("æ", "ö"),
    ("u00e6", "u00f6"),
    ("Æ", "Ö"),
    ("u00c6", "u00d6"),
    ("ø", "ä"),
    ("u00f8", "u00e4"),
    ("Ø", "Ä"),
    ("u00d8", "u00c4"),
]

DAN_NOR_REPLACE = [
    ("æ", "ø"),
    ("u00e6", "u00f8"),
    ("Æ", "Ø"),
    ("u00c6", "u00d8"),
    ("ø", "æ"),
    ("u00f8", "u00e6"),
    ("Ø", "Æ"),
    ("u00d8", "u00c6"),
]

USINTL_ALTGR_REPLACE_APOSTROPHE = [
    {
        REPL_KEYCODE: "APOSTROPHE",
        REPL_OLD: r"'\''",
        REPL_NEW: r"'\u0301'",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "APOSTROPHE",
        REPL_OLD: "'\"'",
        REPL_NEW: r"'\u0308'",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "APOSTROPHE",
        REPL_OLD: r"'\u0301'",
        REPL_NEW: r"'\''",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "APOSTROPHE",
        REPL_OLD: r"'\u0308'",
        REPL_NEW: "'\"'",
        REPL_SKIP: ["alt:", "label:"],
    },
]
USINTL_ALTGR_REPLACE_GRAVE = [
    {
        REPL_KEYCODE: "GRAVE",
        REPL_OLD: r"'`'",
        REPL_NEW: r"'\u0300'",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "GRAVE",
        REPL_OLD: "'~'",
        REPL_NEW: r"'\u0303'",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "GRAVE",
        REPL_OLD: r"'\u0300'",
        REPL_NEW: r"'`'",
        REPL_SKIP: ["alt:", "label:"],
    },
    {
        REPL_KEYCODE: "GRAVE",
        REPL_OLD: r"'\u0303'",
        REPL_NEW: "'~'",
        REPL_SKIP: ["alt:", "label:"],
    },
]

USINTL_POL_PROG_REPLACE = [
    ("u00e9", "u0119"),  # é to ę
    ("u00c9", "u0118"),  # É to Ę
    ("u00e1", "u0105"),  # á to ą
    ("u00c1", "u0104"),  # Á to Ą
    {
        REPL_KEYCODE: "S",
        REPL_OLD: r"'\u00df'",
        REPL_NEW: r"'\u015b'",
        REPL_SKIP: ["alt:"],
    },  # ß to ś (except on alt modifier)
    ("u00a7", "u015a"),  # § to Ś
    ("u00f8", "u0142"),  # ø to ł
    ("u00d8", "u0141"),  # Ø to Ł
    ("u00e6", "u017c"),  # æ to ż
    ("u00c6", "u017b"),  # Æ to Ż
    ("u00a9", "u0107"),  # © to ć
    ("u00a2", "u0106"),  # ¢ to Ć
    ("u00f1", "u0144"),  # ñ to ń
    ("u00d1", "u0143"),  # Ñ to Ń
]

# map Pro1 keycodes to Pro1 X keycodes
PRO1_PRO1X_REPLACE = [
    ("map key 41 ", "map key 16 "),
    ("map key 16 ", "map key 17 "),
    ("map key 17 ", "map key 18 "),
    ("map key 18 ", "map key 19 "),
    ("map key 19 ", "map key 20 "),
    ("map key 20 ", "map key 21 "),
    ("map key 21 ", "map key 22 "),
    ("map key 22 ", "map key 23 "),
    ("map key 23 ", "map key 24 "),
    ("map key 24 ", "map key 25 "),
    ("map key 25 ", "map key 26 "),
    ("map key 39 ", "map key 27 "),
    ("map key 43 ", "map key 30 "),
    ("map key 30 ", "map key 31 "),
    ("map key 31 ", "map key 32 "),
    ("map key 32 ", "map key 33 "),
    ("map key 33 ", "map key 34 "),
    ("map key 34 ", "map key 35 "),
    ("map key 35 ", "map key 36 "),
    ("map key 36 ", "map key 37 "),
    ("map key 37 ", "map key 38 "),
    ("map key 38 ", "map key 39 "),
    ("map key 26 ", "map key 41 "),
    ("map key 27 ", "map key 44 "),
    ("map key 44 ", "map key 45 "),
    ("map key 45 ", "map key 46 "),
    ("map key 46 ", "map key 47 "),
    ("map key 47 ", "map key 48 "),
    ("map key 48 ", "map key 49 "),
    ("map key 49 ", "map key 50 "),
    ("map key 50 ", "map key 51 "),
    ("map key 51 ", "map key 52 "),
    ("map key 52 ", "map key 53 "),
]

# for Pro1 X autogeneration
QWERTZ_LAYOUTS = [
    "cze_1",
    "cze_2",
    "che_fra",
    "dan_1",
    "ell_1",
    "fin_1",
    "ger_1",
    "hun_1",
    "nor_1",
    "por_1",
    "usa_1",
    "usaintl_1",
    "usaintl_fndead",
]

GENERATED_LAYOUTS = [
    {
        NAME: "pro1_qwerty_cze_1.kcm",
        SOURCE: "pro1_qwerty_cze_2.kcm",
        REMOVE_SCANCODES: [
            21, # Z
            44, # Y
        ],
    },
    {
        NAME: "pro1_qwertz_cze_1.kcm",
        SOURCE: "pro1_qwertz_cze_2.kcm",
        REPLACE: [
            ("map key 20 Z", "map key 20 Y"),
            ("map key 27 Y", "map key 27 Z"),
            ("key Y", "key Z"),
            ("key Z", "key Y"),
            ("'z'", "'y'"),
            ("'Z'", "'Y'"),
            ("'y'", "'z'"),
            ("'Y'", "'Z'"),
        ],
    },
    {
        NAME: "pro1_qwerty_nor_1.kcm",
        SOURCE: "pro1_qwerty_dan_1.kcm",
        REPLACE: DAN_NOR_REPLACE,
    },
    {
        NAME: "pro1_qwertz_nor_1.kcm",
        SOURCE: "pro1_qwertz_dan_1.kcm",
        REPLACE: DAN_NOR_REPLACE,
    },
    {
        NAME: "pro1_qwerty_swe_1.kcm",
        SOURCE: "pro1_qwerty_dan_1.kcm",
        REPLACE: DAN_SWE_REPLACE,
    },
    {
        NAME: "pro1x_qwerty_fin_1.kcm",
        SOURCE: "pro1x_qwerty_dan_1.kcm",
        REPLACE: DAN_SWE_REPLACE,
    },
    {
        NAME: "pro1x_qwerty_nor_1.kcm",
        SOURCE: "pro1x_qwerty_dan_1.kcm",
        REPLACE: DAN_NOR_REPLACE,
    },
    {
        NAME: "pro1x_scandic_fin_1.kcm",
        SOURCE: "pro1x_scandic_dan_1.kcm",
        REPLACE: DAN_SWE_REPLACE,
    },
    {
        NAME: "pro1x_scandic_nor_1.kcm",
        SOURCE: "pro1x_scandic_dan_1.kcm",
        REPLACE: DAN_NOR_REPLACE,
    },
    {
        NAME: "pro1_qwerty_usaintl_fndead.kcm",
        SOURCE: "pro1_qwerty_usaintl_1.kcm",
        REPLACE: USINTL_ALTGR_REPLACE_APOSTROPHE+
                 USINTL_ALTGR_REPLACE_GRAVE,
    },
    {
        NAME: "pro1_qwertz_usaintl_fndead.kcm",
        SOURCE: "pro1_qwertz_usaintl_1.kcm",
        REPLACE: USINTL_ALTGR_REPLACE_APOSTROPHE,
        # no GRAVE key on QWERTZ variant
    },
    {
        NAME: "pro1_qwertz_fin_1.kcm",
        SOURCE: "pro1_qwertz_dan_1.kcm",
        REPLACE: DAN_SWE_REPLACE,
    },
    {
        NAME: "pro1_qwerty_fin_1.kcm",
        SOURCE: "pro1_qwerty_swe_1.kcm",
        REPLACE: [
            ("å", "ä"),
            ("u00e5", "u00e4"),
            ("Å", "Ä"),
            ("u00c5", "u00c4"),
        ],
        REMOVE_SCANCODES: [
            111, # DEL
            13, # =
        ],
        REMOVE_KEYCODES: [
            "PLUS",
        ],
        ADD: r"""
key O {
    label:                              'O'
    base:                               'o'
    shift, capslock:                    'O'
    fn:                                 '\u00e5' # å
    fn+shift, fn+capslock, fn+ctrl:     '\u00c5' # Å
}
""",
    },
    {
        NAME: "pro1_qwerty_pol_prog.kcm",
        SOURCE: "pro1_qwerty_usaintl_fndead.kcm",
        REPLACE: USINTL_POL_PROG_REPLACE,
        REMOVE_KEYCODES : [
            "X",
        ],
        ADD: r"""
key X {
    label:                              'X'
    base:                               'x'
    shift, capslock:                    'X'
    fn:                                 '\u017a' # ź
    fn+shift, ctrl+fn, fn+capslock:     '\u0179' # Ź
}
""",
    },
] + [
    {
        NAME: f"pro1x_qwertz_{name}.kcm",
        SOURCE: f"pro1_qwertz_{name}.kcm",
        REPLACE: PRO1_PRO1X_REPLACE,
        # Remove Sym = WAKEUP assignment, it does not work on Pro1X stock OS
        # and the Sym has some stock functionality (keyboard layout setup).
        REMOVE_SCANCODES: [
            249, # Sym
        ],
    } for name in QWERTZ_LAYOUTS
]

def expand_replacement(rule):
    if isinstance(rule, tuple):
        return {REPL_OLD: rule[0], REPL_NEW: rule[1]}
    return rule

def layout_path(filename, layout_dir, generated_dir):
    gendirname = os.path.join(generated_dir, filename)
    if os.path.exists(gendirname):
        return gendirname
    return os.path.join(layout_dir, filename)

def generate_layout(layout, target_dir):
    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)
    layout_dir = os.path.join(os.path.dirname(__file__), "finqwerty", "src", "main", "res", "raw")
    with \
    open(layout_path(layout[SOURCE], layout_dir, target_dir), 'r', encoding="utf-8") as src, \
    open(os.path.join(target_dir, layout[NAME]), 'w', encoding="utf-8") as dst:
        remove_this_key = False
        cur_keycode = None
        rules_matched = {REPLACE: [], REMOVE_SCANCODES: [], REMOVE_KEYCODES: []}
        for line in src:
            if remove_this_key:
                if line.startswith('}'):
                    remove_this_key = False
                # skip this key
                continue

            if line.startswith('}'):
                cur_keycode = None

            if line.startswith("map key "):
                for scancode in layout.get(REMOVE_SCANCODES, []):
                    if line.startswith("map key {} ".format(scancode)):
                        line = "#" + line
                        rules_matched[REMOVE_SCANCODES].append(scancode)
                        break

            if line.startswith("key "):
                cur_keycode = line.split()[1]

                for keycode in layout.get(REMOVE_KEYCODES, []):
                    if line.startswith("key {} ".format(keycode)):
                        remove_this_key = True
                        rules_matched[REMOVE_KEYCODES].append(keycode)
                        break
                if remove_this_key:
                    continue

            for replacement_orig in layout.get(REPLACE, []):
                replacement = expand_replacement(replacement_orig)
                if REPL_KEYCODE in replacement and cur_keycode != replacement[REPL_KEYCODE]:
                    continue
                if any(skip in line for skip in replacement.get(REPL_SKIP, [])):
                    continue
                if replacement[REPL_OLD] in line:
                    line = line.replace(replacement[REPL_OLD], replacement[REPL_NEW])
                    rules_matched[REPLACE].append(replacement_orig)
                    break
            dst.write(line)

        for ruletype in rules_matched.keys():
            for rule in layout.get(ruletype, []):
                if rule not in rules_matched[ruletype]:
                    if ruletype == REPLACE and any(ord(c) >= 128 for c in expand_replacement(rule)[REPL_OLD]):
                        # non-ASCII rule, it is just for comments so allow not matching
                        continue
                    raise RuntimeError(f"Rule {rule} for {layout[NAME]} were never executed")

        dst.write(layout.get(ADD, ""))

def generate_layouts(layouts, target_dir):
    for layout in layouts:
        generate_layout(layout, target_dir)

def remove_previous_layouts(target_dir):
    if pathlib.Path(target_dir).exists():
        # for safety, only remove .kcm files
        for path in pathlib.Path(target_dir).iterdir():
            if path.suffix == '.kcm':
                path.unlink()
        pathlib.Path(target_dir).rmdir()

def generate_all_layouts(target_dir):
    # in case layouts are removed, clean the target directory
    remove_previous_layouts(target_dir)

    generate_layouts(layouts=GENERATED_LAYOUTS, target_dir=target_dir)

def main():
    generate_all_layouts(target_dir=sys.argv[1])

if __name__ == "__main__":
    main()
