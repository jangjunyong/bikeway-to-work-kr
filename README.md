# 자전거길은 일터까지 닿는가

전국 시군구별로 자전거 통행망이 일터까지 닿는 정도(일터 도달률)를 계산하고, 이것이 자전거 출퇴근과 승용차 출퇴근 탄소를 설명하는지 살피는 분석 코드다. 2026 AI 교통문제 해결 데이터 분석 공모전 출품작의 공개 레포다.

> 골격 단계다. 분석 단계는 `run_all.py`의 `STAGES`에 하나씩 등록한다.

## 구성

```
common/      경로 상수(paths), 통행망 그래프·접근성 계산(graph), 2020 센서스 시군구 매핑(sgg)
national/    전국 시군구 도달률과 요인 분석
hwaseong/    화성 데모 심층 분석
budget/      지자체 예산과 정책 연결
feedback/    데모 결과를 전국 추정에 되먹이기
results/     집계 결과 CSV
figures/     그림
tests/       pytest
run_all.py   전 단계 실행 (--from <단계>로 중간부터)
```

## 실행

```
pip install -r requirements.txt
python -m pytest tests -q
python run_all.py --from <단계>
```

경로는 환경변수로 바꾼다. 기본값은 다음과 같다.

| 변수 | 기본값 | 용도 |
|---|---|---|
| `BW_RAW` | `C:/wk/raw` | 내려받은 공개 원자료 캐시 (커밋하지 않음) |
| `BW_PRIVATE` | `C:/wk` | 비공개 입력 작업 폴더 |
| `BW_OUT` | `<레포>/results` | 집계 결과 |
| `BW_FIG` | `<레포>/figures` | 그림 |

## 데이터

공개 원자료는 내려받는 방법만 적고 레포에 넣지 않는다. 출처와 이용 조건은 [DATA_LICENSES.md](DATA_LICENSES.md)에 있다. 공장 좌표, 공식 GIS 원본, 국민연금 원본 행, 단절 지점 좌표 목록은 공개하지 않으며 이 레포에는 코드와 집계 결과만 있다.
