"""Stage 2 — 用自製的 timeit 量三種搜尋。

量測方式：固定 seed 產生「已排序、無重複」的整數 list，對每個 size 隨機抽
`queries` 個 target（一半存在、一半不存在），用 timing.timeit 量「跑完
queries 次查詢」的耗時，repeat 取平均。

set / binary 的優勢要查很多次才顯現，所以量的是「查 queries 次」的總時。
results.json 是 Stage 4 雷達圖的輸入。
"""

import json
import random
from pathlib import Path

from search import binary_search, linear_search, set_search
from timing import timeit

RESULTS_PATH = Path(__file__).with_name("results.json")


def make_data(n: int, seed: int = 42) -> list:
    """產生已排序、無重複的整數 list，固定 seed 以便重現。"""
    if n < 0:
        raise ValueError(f"n 必須 >= 0，收到 {n}")
    rng = random.Random(seed)
    # 從較大的範圍取樣以保證無重複，再排序滿足 binary_search 的前提
    return sorted(rng.sample(range(n * 3 + 1), n))


def _make_queries(data: list, n: int, queries: int, seed: int = 7) -> list:
    """產生查詢目標：一半取自 data（存在）、一半取 data 外的值（不存在）。"""
    rng = random.Random(seed)
    present = [rng.choice(data) for _ in range(queries // 2)] if data else []
    absent = [-(i + 1) for i in range(queries - len(present))]  # 負數一定不在
    targets = present + absent
    rng.shuffle(targets)
    return targets


def _time_over_queries(func, data, targets, repeat=3) -> float:
    @timeit(repeat=repeat)
    def run_all():
        for t in targets:
            func(data, t)

    run_all()
    return run_all.last_elapsed


def run_benchmark(sizes=(1000, 5000, 20000, 80000), queries=100) -> dict:
    """對每個 size 量三種搜尋查 queries 次的耗時，回傳結果 dict。"""
    methods = {
        "linear_search": linear_search,
        "binary_search": binary_search,
        "set_search": set_search,
    }
    results = {}
    for n in sizes:
        data = make_data(n)
        targets = _make_queries(data, n, queries)
        results[str(n)] = {
            name: _time_over_queries(func, data, targets)
            for name, func in methods.items()
        }
    return {"queries": queries, "sizes": list(sizes), "results": results}


def main():
    report = run_benchmark()
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"queries = {report['queries']}（每個 size 查這麼多次）")
    header = f"{'n':>8} | {'linear':>10} | {'binary':>10} | {'set':>10}"
    print(header)
    print("-" * len(header))
    for n_str in report["results"]:
        r = report["results"][n_str]
        print(
            f"{n_str:>8} | {r['linear_search']:>10.6f} | "
            f"{r['binary_search']:>10.6f} | {r['set_search']:>10.6f}"
        )
    print(f"\n結果已寫入 {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
