"""Stage 5 — 安全性規則測試（對照 OpenSSF Secure Coding Guide for Python）。

挑三條「適用」本專案的條目，各寫一個（先紅後綠）測試：

  1. 03 Numbers（CWE-20 輸入驗證）：make_data 應拒絕非整數 / 負數的 n，
     用明確 ValueError，而不是讓 range()/random 拋出語意不清的 TypeError。
  2. 04 Neutralization（CWE-502 不安全的反序列化）：results 一律用 json 讀寫，
     不得用 pickle——pickle.load 會執行任意程式碼。
  3. 05 Exception Handling（CWE-396 過廣的例外處理）：load_results 對不存在的
     檔案應讓 FileNotFoundError 自然傳出，不可被 bare except 吞掉。

不適用而刻意不改的項目，在 README.md 的安全掃描段落逐一說明判斷。
"""

import inspect
import json
import tempfile
import unittest
from pathlib import Path

import benchmark


class TestNumbersInputValidation(unittest.TestCase):
    def test_make_data_rejects_negative(self):
        with self.assertRaises(ValueError):
            benchmark.make_data(-1)

    def test_make_data_rejects_non_int(self):
        with self.assertRaises(ValueError):
            benchmark.make_data(3.5)
        with self.assertRaises(ValueError):
            benchmark.make_data(True)  # bool 是 int 子類，但語意上不是長度


class TestNeutralization(unittest.TestCase):
    def test_no_pickle_used(self):
        source = inspect.getsource(benchmark)
        self.assertNotIn("import pickle", source, "不得 import pickle")
        self.assertNotIn("pickle.load", source, "不得用 pickle.load 反序列化")

    def test_load_results_round_trips_json(self):
        payload = {"queries": 1, "sizes": [1], "results": {}}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "r.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
            self.assertEqual(benchmark.load_results(path), payload)


class TestExceptionHandling(unittest.TestCase):
    def test_load_results_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            benchmark.load_results(Path("does-not-exist-12345.json"))


if __name__ == "__main__":
    unittest.main()
