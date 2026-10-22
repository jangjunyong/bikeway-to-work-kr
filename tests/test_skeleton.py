import importlib

import pytest

import run_all


def test_paths_env_override(monkeypatch, tmp_path):
    import common.paths as p
    for k, v in {'BW_RAW': 'raw', 'BW_PRIVATE': 'priv', 'BW_OUT': 'out', 'BW_FIG': 'fig'}.items():
        monkeypatch.setenv(k, str(tmp_path / v))
    p = importlib.reload(p)
    assert (p.RAW, p.PRIVATE, p.OUT, p.FIG) == tuple(tmp_path / v for v in ('raw', 'priv', 'out', 'fig'))
    for k in ('BW_RAW', 'BW_PRIVATE', 'BW_OUT', 'BW_FIG'):
        monkeypatch.delenv(k)
    p = importlib.reload(p)
    assert p.OUT == p.ROOT / 'results' and p.FIG == p.ROOT / 'figures'


def test_run_all_from_stage(monkeypatch):
    ran = []
    monkeypatch.setattr(run_all, 'STAGES', [('a', 'a.py'), ('b', 'b.py'), ('c', 'c.py')])
    monkeypatch.setattr(run_all, 'run_stage', lambda name, script: ran.append(name))
    assert run_all.main(['--from', 'b']) == 0
    assert ran == ['b', 'c']
    with pytest.raises(SystemExit):
        run_all.main(['--from', 'zzz'])
