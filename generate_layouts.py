#!/usr/bin/python3

import os

NAME = "name"
SOURCE = "source"
# simple string replacement
REPLACE = "replace"
# remove "map key scancode KEYCODE" by scancode
REMOVE_SCANCODES = "remove_scancodes"
# remove "key KEYCODE { ... } " by KEYCODE
REMOVE_KEYCODES = "remove_keycodes"
ADD = "add"

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
]

def generate_layout(layout):
    layout_dir = os.path.join(os.path.dirname(__file__), "finqwerty", "src", "main", "res", "raw")
    with \
    open(os.path.join(layout_dir, layout[SOURCE]), 'r') as src, \
    open(os.path.join(layout_dir, layout[NAME]), 'w') as dst:
        remove_this_key = False
        for line in src:
            if remove_this_key:
                if line.startswith('}'):
                    remove_this_key = False
                # skip this key
                continue

            if line.startswith("map key "):
                for scancode in layout.get(REMOVE_SCANCODES, []):
                    if line.startswith("map key {} ".format(scancode)):
                        line = "#" + line
                        break

            if line.startswith("key "):
                for keycode in layout.get(REMOVE_KEYCODES, []):
                    if line.startswith("key {} ".format(keycode)):
                        remove_this_key = True
                        break
                if remove_this_key:
                    continue

            for replacement in layout.get(REPLACE, []):
                if replacement[0] in line:
                    line = line.replace(replacement[0], replacement[1])
                    break
            dst.write(line)
        dst.write(layout.get(ADD, ""))

def generate_layouts(layouts):
    for layout in layouts:
        generate_layout(layout)

def generate_all_layouts():
    generate_layouts(GENERATED_LAYOUTS)

def main():
    generate_all_layouts()

if __name__ == "__main__":
    main()
