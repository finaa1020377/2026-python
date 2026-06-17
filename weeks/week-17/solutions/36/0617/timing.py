"""0617 任務一 — timeit 計時裝飾器。

規格:
  1. 不改變被裝飾函式的回傳值。
  2. 用 functools.wraps 保留 __name__ / __doc__。
  3. 每次呼叫實際跑 repeat 次(預設 3),每次耗時(秒,float)append 到
     wrapper.records;wrapper.last_elapsed = 本次 repeat 的平均耗時。
  4. 裝飾器內不准 print。
  5. repeat < 1 → raise ValueError(用 raise,不准 assert)。

records / last_elapsed 掛在 wrapper 上(而非全域變數),這樣每個被裝飾的函式
各自擁有獨立的計時紀錄,彼此不互相污染,也不需要管理全域狀態。
"""

import functools
import time


def timeit(func=None, *, repeat=3):
    """計時裝飾器,可用 @timeit 或 @timeit(repeat=n) 兩種寫法。

    參數:
        func: 被裝飾的函式(裸用 @timeit 時自動帶入)。
        repeat: 每次呼叫實際執行的次數,預設 3,必須 >= 1。

    回傳:
        包裝後的函式;其回傳值與原函式相同。包裝函式額外帶有:
            - records: list[float],累積每一次執行的耗時(秒)。
            - last_elapsed: float,最近一次呼叫的 repeat 次平均耗時(秒)。

    例外:
        ValueError: 當 repeat < 1 時拋出(刻意用 raise 而非 assert,
        因為 assert 在 -O 最佳化模式會被移除,驗證會失效)。
    """
    if repeat < 1:
        raise ValueError(f"repeat 必須 >= 1,收到 {repeat}")

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(repeat):
                start = time.perf_counter()
                result = f(*args, **kwargs)
                elapsed = time.perf_counter() - start
                wrapper.records.append(elapsed)
            wrapper.last_elapsed = sum(wrapper.records[-repeat:]) / repeat
            return result

        wrapper.records = []
        wrapper.last_elapsed = 0.0
        return wrapper

    # @timeit(repeat=n) → func 為 None,回傳 decorator 等待套用
    if func is None:
        return decorator
    # @timeit → func 為被裝飾函式,直接套用
    return decorator(func)
