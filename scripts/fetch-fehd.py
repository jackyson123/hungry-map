#!/usr/bin/env python3
"""
Download FEHD restaurant licences (with coordinates from public ArcGIS layer
derived from official open data) and write data/restaurants.min.json

Attribution required: 資料來源：食物環境衞生署 / DATA.GOV.HK
"""
import json
import os
import time
import urllib.request

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BASE = (
    'https://services3.arcgis.com/6j1KwZfY2fZrfNMR/arcgis/rest/services/'
    'Restaurant_licences/FeatureServer/0/query'
)

TYPE_EMOJI = {'RL': '🍽️', 'RR': '☕', 'MR': '🚢'}
DIST = {
    '11': '東區', '12': '灣仔', '15': '南區', '17': '離島', '18': '中西區',
    '31': '美食車', '51': '觀塘', '52': '九龍城', '53': '黃大仙',
    '61': '油尖', '62': '旺角', '63': '深水埗', '91': '葵青', '92': '荃灣',
    '93': '屯門', '94': '元朗', '95': '大埔', '96': '北區', '97': '沙田', '98': '西貢',
}


def fetch_all():
    feats = []
    offset = 0
    page = 2000
    while True:
        url = (
            f'{BASE}?where=1%3D1&outFields=*&returnGeometry=false'
            f'&resultOffset={offset}&resultRecordCount={page}&f=json'
        )
        req = urllib.request.Request(url, headers={'User-Agent': 'HungryMap/2.1'})
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.load(r)
        batch = data.get('features') or []
        print(f'offset {offset}: {len(batch)}')
        if not batch:
            break
        feats.extend(batch)
        if len(batch) < page:
            break
        offset += page
        time.sleep(0.25)
    return feats


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    feats = fetch_all()
    places = []
    seen = set()
    for f in feats:
        a = f.get('attributes') or {}
        try:
            lat = float(a.get('LATITUDE') or 0)
            lng = float(a.get('LONGITUDE') or 0)
        except (TypeError, ValueError):
            continue
        if abs(lat) < 1 or abs(lng) < 1:
            continue
        tcode = (a.get('NSEARCH02_TC') or a.get('NSEARCH02_EN') or 'RL').strip()
        dcode = str(a.get('NSEARCH01_TC') or a.get('NSEARCH01_EN') or '')
        name = (
            a.get('NSEARCH03_TC') or a.get('NSEARCH03_EN')
            or a.get('NAME_TC') or a.get('NAME_EN') or ''
        ).strip()
        if not name:
            continue
        key = (name, round(lat, 4), round(lng, 4))
        if key in seen:
            continue
        seen.add(key)
        places.append({
            'i': 'f' + str(a.get('OBJECTID') or len(places)),
            'n': name,
            't': tcode,
            'a': round(lat, 6),
            'o': round(lng, 6),
            'd': dcode,
            'ad': (a.get('ADDRESS_TC') or a.get('ADDRESS_EN') or '')[:80],
        })

    out = {
        'src': 'FEHD',
        'attr': '資料來源：食物環境衞生署 / DATA.GOV.HK',
        'date': time.strftime('%Y-%m-%d'),
        'n': len(places),
        'p': places,
    }
    path = os.path.join(OUT_DIR, 'restaurants.min.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'Wrote {len(places)} places -> {path}')


if __name__ == '__main__':
    main()
