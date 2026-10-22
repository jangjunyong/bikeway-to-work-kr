import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ['geocode', 'nps_', '공장등록', '.tif', 'gap_points', '.pbf', '.parquet']


def test_no_private_files_tracked():
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', check=True).stdout
    bad = [f for f in out.splitlines() if any(p in f for p in FORBIDDEN)]
    assert not bad, f'비공개·대용량 파일이 추적 중: {bad}'
