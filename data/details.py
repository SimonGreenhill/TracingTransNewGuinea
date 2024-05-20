#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'
import sys
from collections import Counter

import csvw
from pycldf import Dataset

sys.path.append('../bin')
from common import getcsv


CLADELIST = {
    # NG
    
    'abun1252': 'Abun',
    'amto1249': 'Amto-Musan',
    'anga1289': 'Angan',
    'anim1240': 'Anim',
    'araf1243': 'Arafundi',
    'aust1307': 'Austronesian',
    'bain1263': 'Baining',
    'bord1247': 'Border',
    'bosa1245': 'Bosavi',
    'bula1259': 'Bulaka River',
    'daga1274': 'Dagan',
    'doso1238': 'Doso-Turumsa',
    'east1459': "East Bird's Head",
    'east2499': 'East Kutubu',
    'east2503': 'Eastern Trans-Fly',
    'geel1240': 'Geelvink Bay',
    'hata1242': 'Hatam-Mansim',
    'inan1242': 'Inanwatan',
    'indo1319': 'Indo-European',
    'kamu1264': 'Kamula-Elevala',
    'kaur1274': 'Kaure-Kosare',
    'kaya1327': 'Kayagaric',
    'kera1258': 'Keram',
    'kiwa1251': 'Kiwaian',
    'koia1260': 'Koiarian',
    'kolo1268': 'Kolopom',
    'kond1302': 'Konda-Yahadian',
    'kwal1257': 'Kwalean',
    'kwer1242': 'Greater Kwerba',
    'lake1255': 'Lakes Plain',
    'left1242': 'Left May',
    'lowe1437': 'Lower Sepik-Ramu',
    'maib1239': 'Maybrat-Karon',
    'mail1249': 'Mailuan',
    'mair1253': 'Mairasic',
    'manu1261': 'Manubaran',
    'momb1255': 'Mombum-Koneraw',
    'more1255': 'Yam',
    'naml1239': 'Namla-Tofanma',
    'nduu1242': 'Ndu',
    'nimb1257': 'Nimboranic',
    'nort2923': 'North Halmahera',
    'nucl1580': 'Eleman',
    'nucl1708': 'Nuclear Torricelli',
    'pauw1244': 'Pauwasi',
    'piaw1238': 'Piawi',
    'sena1264': 'Senagi',
    'sent1261': 'Sentanic',
    'sepi1257': 'Sepik',
    'skoo1245': 'Sko',
    'sout1516': "South Bird's Head Family",
    'suki1244': 'Suki-Gogodala',
    'tebe1251': 'Teberan',
    'timo1261': 'Timor-Alor-Pantar',
    'toro1256': 'Tor-Orya',
    'tura1263': 'Turama-Kikori',
    'wali1264': 'Walioic',
    'east2433': 'East Strickland',
    'paho1240': 'Pahoturi',
    'west1493': "West Bird's Head",
    'west2604': 'West Bomberai',
    'yare1250': 'Yareban',
    'yawa1259': 'Yawa-Saweru',
    'yuat1252': 'Yuat',
    'pidg1258': 'Creole',
    'soma1242': 'Somahai',

    
    # TNG
    'nucl1709/pani1259': 'TNG.PaniaiLakes',
    'nucl1709/enga1254': 'TNG.Enga-Kewa-Huli',
    'nucl1709/fini1244/fini1245': 'TNG.FH.Finisterre',
    'nucl1709/fini1244/huon1246': 'TNG.FH.Huon',
    'nucl1709/kain1273': 'TNG.Kainantu-Goroka',
    'nucl1709/cent2116/asma1256': 'TNG.Asmat',
    'nucl1709/cent2116/awyu1265': 'TNG.Awyu-Ok',
    'nucl1709/dani1287': 'TNG.Dani',
    'nucl1709/mekk1240': 'TNG.Mek',
    'nucl1709/bina1276': 'TNG.GreaterBinanderean',
    'nucl1709/cent2120': 'TNG.Chimbu-Wahgi',
    
    # Madang
    'nucl1709/mada1298/raic1241': 'TNG.Madang.RaiCoast',
    'nucl1709/mada1298/croi1234': 'TNG.Madang.Croiselles',
    'nucl1709/mada1298/kala1403': 'TNG.Madang.Kalamic-SouthAdelbert',
}

OVERRIDES = {
    'magi-musak': 'magi1243',
}


def label_clade(taxon, clade, labels):
    
    if taxon in OVERRIDES:
        return OVERRIDES.get(taxon)
    
    for o in CLADELIST:
        if clade.startswith(o):
            return CLADELIST[o]
    
    return None # 

if __name__ == '__main__':
    ignore = {r['ID'] for r in getcsv("ignore.csv")}
    source_labels = {r['ID']: r['Label'] for r in getcsv("sources.csv")}
    
    tng = Dataset.from_metadata("transnewguinea-org/cldf/cldf-metadata.json")
    glott = Dataset.from_metadata("glottolog-cldf/cldf/cldf-metadata.json")
    
    languages = {r.data['ID']: r.data for r in tng.objects('LanguageTable')}
    
    # collect source information
    sources = {
        (r.data['Language_ID'], r.data['Source'][0]) for r in tng.objects('FormTable')
    }
    
    classifs = {g.data['Language_ID']: g.data['Value'] for g in glott.objects('ValueTable') if g.data['ID'].endswith("-classification")}
    labels = {g.data['ID']: g.data['Name'] for g in glott.objects('LanguageTable')}
    
    out = []
    tally = Counter()
    for l in languages:
        if l in ignore:
            continue

        gc = OVERRIDES.get(l, languages[l]['Glottocode'])
            
        cl = classifs.get(gc, "?")
        if cl == '?':
            cl = labels.get(gc)
            fam = cl
        else:
            fam = label_clade(gc, cl, labels)

        if not cl:
            #print("BAD CLADE: %s %s = %r : %r" % (l, gc, cl, fam))
            raise ValueError("BAD CLADE: %s %s = %r : %r" % (l, gc, cl, fam))

        if not fam:
            #print("BAD FAMILY: %s %s = %r : %r" % (l, gc, cl, fam))
            raise ValueError("BAD FAMILY: %s %s = %r : %r" % (l, gc, cl, fam))

        tally[fam] += 1
    
        sources_for_this_language = [s for s in sources if s[0] == l]
        for s in sources_for_this_language:
            out.append({
                'Language': l,
                'Taxon': "%s_%s" % (s[0], source_labels.get(s[1], s[1])),
                'Glottocode': gc,
                'Family': languages[l]['Family'],
                'Clade': fam,
                'Classification': cl,
                'Latitude': languages[l]['Latitude'],
                'Longitude': languages[l]['Longitude'],
            })
    
    header = ['Language', 'Taxon', 'Glottocode', 'Family', 'Clade', 'Classification', 'Latitude', 'Longitude']
    with csvw.UnicodeWriter('details.csv') as writer:
        writer.writerow(header)
        for o in out:
            writer.writerow([o.get(h, '') for h in header])
