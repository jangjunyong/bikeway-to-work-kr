"""전 단계를 순서대로 돌린다. `python run_all.py --from <단계>`로 중간부터 이어 돌릴 수 있다.

STAGES에 (단계 이름, 스크립트 경로)를 순서대로 등록한다. 각 태스크가 자기 단계를 추가한다.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES: list[tuple[str, str]] = []


def run_stage(name, script):
    print(f'== {name}: {script}', flush=True)
    subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / script)], check=True, cwd=ROOT)


def main(argv=None):
    names = [n for n, _ in STAGES]
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--from', dest='start', metavar='STAGE', help='이 단계부터 실행: ' + ', '.join(names or ['(등록된 단계 없음)']))
    args = ap.parse_args(argv)
    if args.start and args.start not in names:
        ap.error(f'알 수 없는 단계: {args.start!r}')
    for name, script in STAGES[names.index(args.start) if args.start else 0:]:
        run_stage(name, script)
    return 0


if __name__ == '__main__':
    sys.exit(main())
