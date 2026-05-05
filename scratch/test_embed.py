from fastembed import TextEmbedding
import time
import statistics

model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def test_embed():
    # Warmup
    list(model.embed(["warmup"]))
    
    latencies = []
    for i in range(20):
        t0 = time.perf_counter()
        list(model.embed(["cloud computing is a great technology for scaling"]))
        ms = (time.perf_counter() - t0) * 1000
        latencies.append(ms)
        print(f"Embed {i+1}: {ms:.2f}ms")
    
    print(f"\nStats:")
    print(f"P50: {statistics.median(latencies):.2f}ms")
    print(f"P99: {sorted(latencies)[-1]:.2f}ms")

if __name__ == "__main__":
    test_embed()
