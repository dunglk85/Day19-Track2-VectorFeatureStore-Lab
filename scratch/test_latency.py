import httpx
import time
import statistics

URL = "http://localhost:8000"

def test_latency():
    try:
        r = httpx.get(f"{URL}/healthz", timeout=5.0)
        print(f"Health check: {r.json()}")
    except Exception as e:
        print(f"Server not ready: {e}")
        return

    latencies = []
    for i in range(10):
        t0 = time.perf_counter()
        r = httpx.get(f"{URL}/search", params={"q": "cloud computing", "mode": "hybrid"})
        wall_ms = (time.perf_counter() - t0) * 1000
        server_ms = r.json()["latency_ms"]
        latencies.append(server_ms)
        print(f"Query {i+1}: server={server_ms:.2f}ms, wall={wall_ms:.2f}ms")
    
    print(f"\nStats (server-side):")
    print(f"P50: {statistics.median(latencies):.2f}ms")
    print(f"P99: {sorted(latencies)[-1]:.2f}ms")

if __name__ == "__main__":
    test_latency()
