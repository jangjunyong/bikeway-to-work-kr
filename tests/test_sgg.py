import pytest

from common.sgg import SGG_TYPE, to_census2020


def test_to_census2020_hwaseong_gu():
    assert to_census2020('41597', '화성시 만세구') == ('경기도|화성시', '화성시')
    assert to_census2020('41591', '경기도 화성시 동탄구')[1] == '화성시'
    assert to_census2020('41111', '수원시 장안구')[1] == '수원시'
    assert to_census2020('', '수원시장안구')[1] == '수원시'  # 띄어쓰기 없는 표기


def test_to_census2020_gunwi():
    # 2020 센서스는 경상북도 군위군. 대구 편입(2023) 표기도 같은 항목으로 모은다
    key = ('경상북도|군위군', '군위군')
    assert to_census2020('27720', '대구광역시 군위군') == key
    assert to_census2020('47720', '경상북도 군위군') == key
    assert to_census2020('27720', '군위군') == key


def test_incheon_2026_reorganization():
    assert to_census2020('', '인천광역시 영종구') == ('인천광역시|중구', '중구')
    assert to_census2020('', '인천광역시 제물포구') == ('인천광역시|중구', '중구')
    assert to_census2020('', '인천광역시 서해구') == ('인천광역시|서구', '서구')
    assert to_census2020('', '인천광역시 검단구') == ('인천광역시|서구', '서구')
    assert to_census2020('', '인천광역시 중구') == ('인천광역시|중구', '중구')
    assert to_census2020('', '인천광역시 동구') == ('인천광역시|동구', '동구')


def test_same_name_in_other_sido_not_confused():
    assert to_census2020('', '서울특별시 중구') == ('서울특별시|중구', '중구')
    assert to_census2020('', '대구광역시 중구')[0] == '대구광역시|중구'
    # 시도 없이 이름만 오면 법정동코드 앞 2자리로 가른다
    assert to_census2020('28110', '중구')[0] == '인천광역시|중구'
    assert to_census2020('11140', '중구')[0] == '서울특별시|중구'
    # 시도 표기 변경(강원·전북 특별자치도)
    assert to_census2020('', '강원특별자치도 춘천시')[0] == '강원도|춘천시'
    assert to_census2020('', '전북특별자치도 전주시 완산구')[0] == '전라북도|전주시'
    assert to_census2020('', '세종특별자치시')[0] == '세종특별자치시|세종시'


def test_unmappable_raises():
    with pytest.raises(KeyError):
        to_census2020('', '중구')  # 시도도 코드도 없어 모호
    with pytest.raises(KeyError):
        to_census2020('', '없는시')


def test_sgg_type_covers_229_census_units():
    assert len(SGG_TYPE) == 229
    assert SGG_TYPE['경기도|화성시'] == '시'
    assert SGG_TYPE['경기도|수원시'] == '시'
    assert SGG_TYPE['경상북도|군위군'] == '군'
    assert SGG_TYPE['서울특별시|중구'] == '구'
    assert set(SGG_TYPE.values()) == {'시', '군', '구'}
