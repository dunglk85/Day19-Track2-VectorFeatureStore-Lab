import sys
import os
from pathlib import Path
sys.path.append(os.getcwd())
from app.search import Searcher
import time
import statistics

ROOT = Path('.').resolve()
CORPUS_PATH = ROOT / "data" / "corpus_vn.jsonl"

def test_keyword_latency():
    s = Searcher.from_corpus(CORPUS_PATH)
    
    latencies = []
    for i in range(100):
        t0 = time.perf_counter()
        s._search_keyword("cloud computing", 50)
        ms = (time.perf_counter() - t0) * 1000
        latencies.append(ms)
    
    print(f"Keyword Stats (1000 docs, depth=50):")
    print(f"P50: {statistics.median(latencies):.2f}ms")
    print(f"P99: {sorted(latencies)[-1]:.2f}ms")

if __name__ == "__main__":
    test_keyword_latency()
