"""2020 인구총조사 시군구 기준으로 행정구역명을 모은다.

센서스(KOSIS DT_1PA2004)는 코드 없이 이름만 있어서 이름을 정규화해 맞춘다.
census_key = "시도|시군구" (예: "경기도|화성시"). 일반구는 상위 시로 합친다.
시군구 목록(229개)은 common/sgg_2020.csv에 있고, `python -m common.sgg`로
RAW/kosis_mirror/dh_DT_1PA2004_2020.csv에서 다시 만든다.
"""
import csv
import re
from pathlib import Path

_CSV = Path(__file__).with_name('sgg_2020.csv')

# 법정동코드 앞 2자리 -> 2020 센서스 시도명 (시도 표기가 이름에 없을 때만 쓴다)
SIDO_BY_CODE = {
    '11': '서울특별시', '26': '부산광역시', '27': '대구광역시', '28': '인천광역시', '29': '광주광역시',
    '30': '대전광역시', '31': '울산광역시', '36': '세종특별자치시', '41': '경기도', '42': '강원도',
    '51': '강원도', '43': '충청북도', '44': '충청남도', '45': '전라북도', '52': '전라북도',
    '46': '전라남도', '47': '경상북도', '48': '경상남도', '50': '제주특별자치도',
}
_SHORT = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시',
          '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시', '세종': '세종특별자치시',
          '경기': '경기도', '강원': '강원도', '충북': '충청북도', '충남': '충청남도', '전북': '전라북도',
          '전남': '전라남도', '경북': '경상북도', '경남': '경상남도', '제주': '제주특별자치도'}
_RENAMED = {'강원특별자치도': '강원도', '전북특별자치도': '전라북도'}  # 2023·2024 시도 개명
SIDO_ALIAS = {**{v: v for v in _SHORT.values()}, **_SHORT, **_RENAMED}

# 인천 2026 개편: 제물포구(옛 중구·동구 원도심)·영종구 -> 중구, 서해구·검단구 -> 서구
# ponytail: 제물포구는 중구·동구를 합친 단위라 이름만으로는 둘로 못 가른다. 행정동 단위 매핑이 필요하면 그때 쪼갠다.
_INCHEON_2026 = {'제물포구': '중구', '영종구': '중구', '서해구': '서구', '검단구': '서구'}


def _load():
    with open(_CSV, encoding='utf-8', newline='') as f:
        return [(r['sido'], r['sgg'], r['type']) for r in csv.DictReader(f)]


_UNITS = _load()
SGG_TYPE = {f'{s}|{n}': t for s, n, t in _UNITS}


def to_census2020(code, name):
    """(법정동 시군구 코드, 시군구 이름) -> (census_key, 2020 센서스 시군구명).

    이름이 기준이고 코드는 시도가 이름에 없을 때만 쓴다(법정동코드 앞 2자리).
    매핑이 모호하거나 없으면 KeyError (조용히 틀린 곳에 붙이지 않는다).
    """
    toks = name.split()
    sido = SIDO_ALIAS.get(toks[0]) if toks else None
    rest = ' '.join(toks[1:] if sido else toks)
    if sido == '세종특별자치시' and not rest:
        rest = '세종시'
    rest = re.sub(r'^(\S+시)\s*\S+구$', r'\1', rest)  # 일반구 -> 상위 시 (공백 없는 표기 포함)
    if rest in _INCHEON_2026:
        sido, rest = '인천광역시', _INCHEON_2026[rest]
    cands = [s for s, n, _ in _UNITS if n == rest]
    for s in (sido, SIDO_BY_CODE.get(str(code)[:2])):
        if s in cands:
            return f'{s}|{rest}', rest
    if len(cands) == 1:  # 시도가 바뀐 단위(군위군: 센서스 경북, 지금 대구)
        return f'{cands[0]}|{rest}', rest
    raise KeyError(f'2020 센서스 시군구로 매핑 불가: code={code!r} name={name!r}')


def build_csv(src):
    """KOSIS 센서스 CSV(행 순서가 시도 > 시군구 > 일반구)에서 시군구 목록을 뽑는다."""
    names, prev = [], None
    for row in csv.reader(open(src, encoding='utf-8', newline='')):
        if row and row[0] != prev:
            names.append(row[0])
            prev = row[0]
    out, sido = [], None
    for n in names[1:]:  # 첫 행은 헤더
        if n in ('전국', '동부', '읍부', '면부'):
            continue
        if re.search(r'(특별시|광역시|특별자치시|특별자치도|도)$', n):
            sido = n
        elif n.endswith('구') and sido.endswith('도'):
            continue  # 도 아래의 구는 일반구 (상위 시로 합침)
        else:
            out.append((sido, n, n[-1] if n[-1] in '시군구' else '?'))
    with open(_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['sido', 'sgg', 'type'])
        w.writerows(out)
    return out


if __name__ == '__main__':
    from common.paths import RAW
    print(len(build_csv(RAW / 'kosis_mirror' / 'dh_DT_1PA2004_2020.csv')), '개 시군구 ->', _CSV)
