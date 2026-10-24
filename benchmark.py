import time
import os
import sys

# setup path
sys.path.insert(0, os.path.abspath("."))

# mock oracle connection and cursor
class FakeCursor:
    def execute(self, sql, params=None):
        pass
    def fetchall(self):
        return [
            ("id1", "title1", "tag1", "ws1", "work", 0.9),
            ("id2", "title2", "tag2", "ws1", "work", 0.8),
        ]

class FakeOracle:
    def cursor(self):
        return FakeCursor()

import mcp_memory.server
mcp_memory.server.get_oracle = lambda: FakeOracle()

# mock get_embedding
original_get_embedding = mcp_memory.server._get_embedding

def fake_get_embedding(text):
    time.sleep(0.5) # simulate API latency
    return [0.1] * 1536

mcp_memory.server._get_embedding = fake_get_embedding

from mcp_memory.server import memory_search

def run_benchmark():
    print("Starting benchmark...")

    # query 1
    t0 = time.time()
    memory_search("hello world", "all", 10)
    t1 = time.time()
    print(f"Query 1 (uncached): {t1 - t0:.4f}s")

    # query 2
    t0 = time.time()
    memory_search("hello world", "all", 10)
    t1 = time.time()
    print(f"Query 2 (cached): {t1 - t0:.4f}s")

if __name__ == "__main__":
    run_benchmark()
