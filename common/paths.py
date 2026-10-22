"""경로 상수. 비공개·대용량 입력은 레포 밖에 두고 환경변수로 바꿀 수 있다.

BW_RAW      공개 원자료 캐시 (기본 C:/wk/raw, 커밋 안 함)
BW_PRIVATE  비공개 입력 작업 폴더 (기본 C:/wk; 공장 좌표·공식 GIS 원본 등)
BW_OUT      집계 결과 CSV (기본 <레포>/results)
BW_FIG      그림 (기본 <레포>/figures)
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(os.environ.get('BW_RAW', 'C:/wk/raw'))
PRIVATE = Path(os.environ.get('BW_PRIVATE', 'C:/wk'))
OUT = Path(os.environ.get('BW_OUT', ROOT / 'results'))
FIG = Path(os.environ.get('BW_FIG', ROOT / 'figures'))
