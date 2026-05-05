import sys
import os
from pathlib import Path
sys.path.append(os.getcwd())
from app.search import Searcher
import time
import statistics

ROOT = Path('.').resolve()
CORPUS_PATH = ROOT / "data" / "corpus_vn.jsonl"

def test_search_latency():
    print("Loading searcher...")
    s = Searcher.from_corpus(CORPUS_PATH)
    print("Searcher ready.")
    
    # Warmup
    for _ in range(5):
        s.search("warmup", mode="hybrid")
    
    latencies = []
    for i in range(20):
        t0 = time.perf_counter()
        s.search("cloud computing", mode="hybrid")
        ms = (time.perf_counter() - t0) * 1000
        latencies.append(ms)
        print(f"Hybrid search {i+1}: {ms:.2f}ms")
    
    print(f"\nStats:")
    print(f"P50: {statistics.median(latencies):.2f}ms")
    print(f"P99: {sorted(latencies)[-1]:.2f}ms")

if __name__ == "__main__":
    test_search_latency()
