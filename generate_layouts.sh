#!/bin/sh

set -ex

qd="./finqwerty/src/main/res/raw"

sed \
	-e "s,æ,ö,g" \
	-e "s,u00e6,u00f6,g" \
	-e "s,Æ,Ö,g" \
	-e "s,u00c6,u00d6,g" \
	-e "s,ø,ä,g" \
	-e "s,u00f8,u00e4,g" \
	-e "s,Ø,Ä,g" \
	-e "s,u00d8,u00c4,g" \
	$qd/pro1_qwerty_dan_1.kcm \
	>$qd/pro1_qwerty_swe_1.kcm

sed \
	-e "s,æ,ö,g" \
	-e "s,u00e6,u00f6,g" \
	-e "s,Æ,Ö,g" \
	-e "s,u00c6,u00d6,g" \
	-e "s,ø,æ,g" \
	-e "s,u00f8,u00e6,g" \
	-e "s,Ø,Æ,g" \
	-e "s,u00d8,u00c6,g" \
	-e "s,ö,ø,g" \
	-e "s,u00f6,u00f8,g" \
	-e "s,Ö,Ø,g" \
	-e "s,u00d6,u00d8,g" \
	$qd/pro1_qwerty_dan_1.kcm \
	>$qd/pro1_qwerty_nor_1.kcm

sed \
	-e "s,å,ä,g" \
	-e "s,u00e5,u00e4,g" \
	-e "s,Å,Ä,g" \
	-e "s,u00c5,u00c4,g" \
	-e "s,^map key 111 ,#&," \
	-e "s,^map key 13 ,#&," \
	$qd/pro1_qwerty_swe_1.kcm \
	| grep -v "# ä" \
	| awk '/^key PLUS/ { skip=1 } /^}/ { if (skip) { skip=0 ; next } } { if (!skip) print }' \
	>$qd/pro1_qwerty_fin_1.kcm
cat >>$qd/pro1_qwerty_fin_1.kcm <<'EOF'

key O {
    label:                              'O'
    base:                               'o'
    shift, capslock:                    'O'
    fn:                                 '\u00e5'
    fn+shift, fn+capslock, fn+ctrl:     '\u00c5'
}
EOF

sed \
	-e "s,æ,ö,g" \
	-e "s,u00e6,u00f6,g" \
	-e "s,Æ,Ö,g" \
	-e "s,u00c6,u00d6,g" \
	-e "s,ø,ä,g" \
	-e "s,u00f8,u00e4,g" \
	-e "s,Ø,Ä,g" \
	-e "s,u00d8,u00c4,g" \
	$qd/pro1_qwertz_dan_1.kcm \
	>$qd/pro1_qwertz_fin_1.kcm

sed \
	-e "s,æ,ö,g" \
	-e "s,u00e6,u00f6,g" \
	-e "s,Æ,Ö,g" \
	-e "s,u00c6,u00d6,g" \
	-e "s,ø,æ,g" \
	-e "s,u00f8,u00e6,g" \
	-e "s,Ø,Æ,g" \
	-e "s,u00d8,u00c6,g" \
	-e "s,ö,ø,g" \
	-e "s,u00f6,u00f8,g" \
	-e "s,Ö,Ø,g" \
	-e "s,u00d6,u00d8,g" \
	$qd/pro1_qwertz_dan_1.kcm \
	>$qd/pro1_qwertz_nor_1.kcm

sed \
	-e "s,# ROW 1,# Y/Z swap\nmap key 20 Z\nmap key 27 Y\n\n&," \
	$qd/pro1_qwerty_cze_1.kcm \
	>$qd/pro1_qwerty_cze_2.kcm

sed \
	-e "s,map key 20 Y,map key 20 Z," \
	-e "s,map key 27 Z,map key 27 Y," \
	-e "s,key Y,key FOO," \
	-e "s,'y','foo'," \
	-e "s,'Y','FOO'," \
	-e "s,key Z,key Y," \
	-e "s,'z','y'," \
	-e "s,'Z','Y'," \
	-e "s,key FOO,key Z," \
	-e "s,'foo','z'," \
	-e "s,'FOO','Z'," \
	$qd/pro1_qwertz_cze_1.kcm \
	>$qd/pro1_qwertz_cze_2.kcm

