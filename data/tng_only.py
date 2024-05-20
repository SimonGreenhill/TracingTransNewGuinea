#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

import sys
from collections import Counter
from pathlib import Path
import csvw

BASE = Path(__file__).parent

sys.path.append('../bin')
from common import getcsv


NOT_TRANSNEWGUINEA = {
    'abun1252': 'Abun',
    'amto1249': '',
    'aust1307': 'Austronesian',
    'araf1243': 'Arafundi',
    'bord1247': 'Border',
    'bula1259': '',
    'burm1264': '',
    'dera1245': '',
    'dibi1240': '',
    'doso1239': '',
    'duri1243': '',
    'east1459': "East Bird's Head",
    'east2503': 'ETF',
    'else1239': '',
    'fasu1242': '',
    'geel1240': '',
    'gres1240': '',
    'hata1243': '',
    'indo1319': 'Indo-European',
    'isir1237': '',
    'kala1256': '',
    'kapo1250': '',
    'kauw1242': '',
    'kehu1238': '',
    'kemt1242': '',
    'kera1258': 'Keram',
    'kond1303': '',
    'lake1255': 'Lakes Plain',
    'left1242': '',
    'lowe1437': 'Lower Sepik-Ramu',
    'maib1239': '',
    'mawe1251': '',
    'mekw1241': '',
    'mlap1238': '',
    'moii1235': '',
    'molo1262': '',
    'mora1239': '',
    'mpur1239': '',
    'nduu1242': 'Ndu',
    'nucl1453': '',
    'nucl1454': '',
    'nucl1595': '',
    'nucl1633': '',
    'nucl1708': 'Nuclear Torricelli',
    'odia1239': '',
    'papi1255': '',
    'pidg1258': 'Creole',
    'pyuu1245': '',
    'sama1240': '',
    'saus1247': '',
    'sege1235': '',
    'sepi1257': 'Sepik',
    'sepi1257': 'Sepik',
    'skoo1245': 'Sko',
    'suab1238': '',
    'tabo1241': '',
    'tape1242': '',
    'tehi1237': '',
    'tofa1246': '',
    'toro1256': '',
    'usku1243': '',
    'yaha1248': '',
    'yale1246': '',
    'yawi1238': '',
    'yetf1238': '',
    'yuat1252': 'Yuat',
    'piaw1238': 'Piawi',
    'paho1240': 'Pahoturi',
    'more1255': 'Morehead',
}


# Groups with relatively strong claims to membership in TNG
STRONG_TRANSNEWGUINEA = {
    'anga1289': 'Angan',
    'anim1240': 'Anim',
    'bosa1245': 'Bosavi',
    'daga1274': 'Dagan',
    'suki1244': 'Suki-Gogodala',
    'kaya1327': 'Kayagaric',
    'kiwa1251': 'Kiwaian',
    'koia1260': 'Koiarian',
    'kolo1268': 'Kolopom',
    'kwal1257': 'Kwalean',
    'mail1249': 'Mailuan',
    'manu1261': 'Manubaran',
    'tura1263': 'Turama-Kikori',
    'west2604': 'West Bomberai',
    'yare1250': 'Yareban',
    'east2433': 'East Strickland',
    'soma1242': 'Somahai',
    'east2499': 'East Kutubu',
    
    # in glottolog's nucl1709
    'nucl1709/cent2116/awyu1265': 'Awyu-Ok',
    'nucl1709/cent2116/asma1256': 'Asmat-Kamoro',
    'nucl1709/cent2120': 'Chimbu-Waghi',
    'nucl1709/dani1287': 'Dani',
    'nucl1709/enga1254': 'Enga-Kewa-Huli',
    'nucl1709/fini1244': 'Finisterre-Huon',
    'nucl1709/bina1276': 'Greater Binanderan',
    'nucl1709/kain1273': 'Kainantu-Goroka',
    'nucl1709/mada1298': 'Madang',
    'nucl1709/mekk1240': 'Mek',
    'nucl1709/pani1259': 'Paniai Lakes',
    'kamu1264': 'Kamula-Elevala',  # awin-pa
    
    ## ISOLATES
    'moro1289': 'Marori',
    'wiru1244': 'Wiru',
    'duna1248': 'Duna',
    'boga1247': 'Bogaya',
    'fuyu1242': 'Fuyug (Goilalan)',  # Goilalan
    'kuni1270': 'Kunimaipan (Goilalan)',
    'taua1242': 'Tauade (Goilalan)',
}

# Groups and isolates with weaker or disputed claims to membership in TNG
WEAK_TRANSNEWGUINEA = {
    'bayo1260': 'Bayono-Awbono',
    'momb1255': 'Komolom (Mombum)',
    'mair1253': 'Mairasi',
    'pauw1244': 'Pauwasi',
    'pawa1255': 'Pawaian',
    'sent1261': 'Sentanic',
    'sout1516': "South Bird's Head",
    'tana1288': 'Tanah Merah',
    'tebe1251': 'Teberan',
    'timo1261': 'Timor-Alor-Pantar',
    'dama1272': 'Uhunduni',
}

# Groups and isolates sometimes assigned to the TNG family without sufficient supporting evidence
WSE_TRANSNEWGUINEA = {
    'demm1245': 'Dem',
    'nucl1580': 'Eleman',
    'kaki1249': 'Kaki Ae',
    'kamu1264': 'Kamula',
    'kaur1274': 'Kaure-Narau',
    'morb1239': 'Mor',
    'kibi1239': 'Porome',
    'pura1257': 'Purari',
}

assert len(STRONG_TRANSNEWGUINEA) - 2 == 35  # -2 as Goilalan split into 3 isolate clades
assert len(WEAK_TRANSNEWGUINEA) == 11
assert len(WSE_TRANSNEWGUINEA) == 8

SUBSETS = {
    1: STRONG_TRANSNEWGUINEA,
    2: WEAK_TRANSNEWGUINEA,
    3: WSE_TRANSNEWGUINEA,
    False: NOT_TRANSNEWGUINEA
}

def is_transnewguinea(who, what):
    for rv, members in SUBSETS.items():
        for m in members:
            if m == who or what.startswith(m):
                return (rv, m)
    raise ValueError("bad: %s - %s" % (who, what))
    return (None, None)


if __name__ == '__main__':
    counter = Counter()
    for s in SUBSETS:
        for m in SUBSETS[s]:
            counter[(s, m)] = 0

    for row in getcsv('details.csv'):
        rv, m = is_transnewguinea(row['Glottocode'], row['Classification'])
        counter[(rv, m)] += 1
        
        if not rv:
            print("IGNORE,%s,%s,not transnewguinea" % (
                row['Language'],
                row['Glottocode']
            ))
        if rv == 4:
            print('4=', m)
            
    print("\n\n")
    levels = Counter()
    for (level, clade), n in counter.most_common():
        if level == 1:
            print("%-20s (%s)\t%d" % (clade, level, n))

        levels[level] += n
    print(levels)
