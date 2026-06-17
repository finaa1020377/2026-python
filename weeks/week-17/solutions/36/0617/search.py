"""0617 任務二 — 搜尋(輕量評估)。

提供 linear_search 與 binary_search 兩個函式,兩者都不可修改傳入的 data。
"""


def linear_search(data: list, target) -> int:
    """線性搜尋:從頭逐一比對,回傳第一個相等元素的 index,找不到回 -1。

    不會修改傳入的 data。時間複雜度 O(n)。
    """
    for index, value in enumerate(data):
        if value == target:
            return index
    return -1


def binary_search(data: list, target) -> int:
    """二分搜尋:前提 data 已由小到大排序,回傳 target 的 index,找不到回 -1。

    不會修改傳入的 data,時間複雜度 O(log n)。

    未排序行為(自訂):本函式「不會」幫你排序,也不會檢查或拋出例外。
    若傳入未排序的 data,二分法的前提被破壞,回傳值未定義
    (可能回傳 -1,也可能回傳某個剛好命中的 index)。
    呼叫端有責任先確保 data 已排序——刻意不在此偷偷排序,
    因為排序會改變/複製資料,且會把 O(log n) 的成本悄悄變成 O(n log n)。
    """
    lo = 0
    hi = len(data) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if data[mid] == target:
            return mid
        if data[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
