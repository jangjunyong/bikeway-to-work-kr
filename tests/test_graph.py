import numpy as np
from shapely.geometry import LineString

from common.graph import bridge_components, build_graph, reach_weights

LINE = LineString([(0, 0), (1000, 0), (2000, 0)])  # 간선 1000m씩, 노드 0-1-2


def test_reach_weights_toy():
    # 출발 0, 목적 1(가중 5)·2(가중 7), cutoff 1500 -> 1번만 닿는다
    G, xy = build_graph([LINE])
    r = reach_weights(G, xy, np.array([[0, 0]]), np.array([[1000, 0], [2000, 0]]), np.array([5.0, 7.0]), cutoff=1500)
    assert r.tolist() == [5.0]


def test_dest_snap_max_extends_destination_only():
    # 목적지가 망에서 250m 떨어짐: dest_snap_max=150이면 0, 300이면 도달
    G, xy = build_graph([LINE])
    o, d, w = np.array([[0, 0]]), np.array([[1000, 250]]), np.array([5.0])
    assert reach_weights(G, xy, o, d, w, cutoff=1500, snap_max=150, dest_snap_max=150).tolist() == [0.0]
    assert reach_weights(G, xy, o, d, w, cutoff=1500, snap_max=150, dest_snap_max=300).tolist() == [5.0]
    # 기본값(None)은 snap_max를 그대로 따른다
    assert reach_weights(G, xy, o, d, w, cutoff=1500, snap_max=150).tolist() == [0.0]
    assert reach_weights(G, xy, o, d, w, cutoff=1500, snap_max=300).tolist() == [5.0]
    # 출발점은 dest_snap_max의 영향을 받지 않는다: 출발점이 250m 밖이면 여전히 0
    far_o = np.array([[0, 250]])
    assert reach_weights(G, xy, far_o, np.array([[1000, 0]]), w, cutoff=1500, snap_max=150, dest_snap_max=300).tolist() == [0.0]


def test_chunk_does_not_change_result():
    G, xy = build_graph([LINE])
    o = np.array([[0, 0], [1000, 0], [2000, 0], [0, 400]])  # 마지막은 접속 반경 밖
    d, w = np.array([[0, 0], [2000, 0]]), np.array([1.0, 10.0])
    full = reach_weights(G, xy, o, d, w, cutoff=1500)
    assert full.tolist() == [1.0, 11.0, 10.0, 0.0]
    for c in (1, 2, 3):
        assert reach_weights(G, xy, o, d, w, cutoff=1500, chunk=c).tolist() == full.tolist()


def test_bridge_components_links_small_gap():
    # 3m 떨어진 두 조각 -> 다리 1개, 길이 3m
    G, xy = build_graph([LineString([(0, 0), (100, 0)]), LineString([(103, 0), (200, 0)])])
    Gb, n, length = bridge_components(G, xy, tol=10.0)
    assert n == 1 and abs(length - 3.0) < 1e-9
    r = reach_weights(Gb, xy, np.array([[0, 0]]), np.array([[200, 0]]), np.array([1.0]), cutoff=250)
    assert r.tolist() == [1.0]
    assert bridge_components(G, xy, tol=2.0)[1] == 0
