"""What the tools answer in an episode: a small document corpus and a file
tree, rendered exactly as the real servers render them.

The formats are the servers' own (checked against filesystem-mcp in
tests/test_episodes.py; crag-mcp's are copied from its source, main.c):

  fs_list    one line per entry, "<type:<5><size:>12>  <name>", sorted by name
  fs_read    the file's text
  fs_stat    path / type / size / modified / mode, one per line
  fs_write   "wrote <n> bytes to <path>"
  crag_stats db / chunks / files / dim
  crag_search  one item per chunk, "[cos …  bm25 …  fusion …] <path>" then the body

A tool-level error is shown to the model as "error: <message>".
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

# Topic phrase (as in data.POOLS) -> (chunk body, the fact a grounded answer
# must repeat). Train and test topics are disjoint, like the pools.
CORPUS: dict[str, tuple[str, str]] = {
    "BM25 parameters": ("BM25 uses k1 = 1.2 and b = 0.75; both are fixed when the index "
                        "is built.", "k1 = 1.2"),
    "reciprocal rank fusion": ("Rank fusion adds 1/(60 + rank) from each ranked list; the "
                               "constant 60 damps the top ranks.", "60 + rank"),
    "the relevance gate": ("The relevance gate drops chunks whose cosine is below 0.35.",
                           "0.35"),
    "embedding dimension": ("The index stores 1024-dimensional float32 embeddings.",
                            "1024-dimensional"),
    "the stdio transport": ("The stdio transport frames each message as one line of JSON "
                            "ended by a newline.", "one line of JSON"),
    "JSON-RPC error codes": ("Unknown methods return -32601 and malformed params return "
                             "-32602.", "-32601"),
    "schema validation": ("Arguments are validated against the tool's inputSchema before "
                          "the handler runs.", "before the handler runs"),
    "the worker thread pool": ("The worker pool starts four threads unless CMCP_WORKERS "
                               "says otherwise.", "four threads"),
    "fuzzing harnesses": ("Each parser has a libFuzzer harness that runs nightly for ten "
                          "minutes.", "ten minutes"),
    "SSE resumption": ("A client resumes an SSE stream by sending the Last-Event-ID header.",
                       "Last-Event-ID"),
    "chunking strategy": ("Documents are split into 800-character chunks with a "
                          "100-character overlap.", "800-character"),
    "cosine similarity": ("Vectors are normalised at insert, so cosine similarity is a "
                          "plain dot product.", "dot product"),
    "the HTTP origin check": ("Requests whose Origin header is not on the allow list get "
                              "a 403.", "403"),
    "protocol version negotiation": ("The server answers initialize with the newest "
                                     "protocol version both sides support.",
                                     "newest protocol version"),
    "handler timeouts": ("A handler that runs longer than 30 seconds is cancelled.",
                         "30 seconds"),
    "the replay gate": ("The replay gate fails CI if any recorded response changes byte "
                        "for byte.", "byte for byte"),
    "WAL mode in SQLite": ("The store opens SQLite in WAL mode so readers never block the "
                           "writer.", "readers never block"),
    "the Python binding": ("The Python binding wraps the C library in a CPython extension "
                           "module.", "CPython extension"),
    # test topics
    "the SSRF egress guard": ("The egress guard refuses private, loopback and link-local "
                              "addresses.", "link-local"),
    "log redaction": ("Log redaction replaces bearer tokens with [REDACTED] before a line "
                      "is written.", "[REDACTED]"),
    "cancellation of requests": ("A notifications/cancelled message stops the handler at "
                                 "its next check.", "notifications/cancelled"),
    "the HNSW index": ("HNSW is not implemented; the exact scan takes 11.9 ms at 100k "
                       "chunks.", "11.9 ms"),
    "nDCG evaluation": ("On SciFact the hybrid retriever reaches an nDCG@10 of 0.742.",
                        "0.742"),
    "rate limiting at accept": ("Connections beyond 64 per second are closed at accept.",
                                "64 per second"),
    "subscriptions": ("resources/subscribe registers a client for updates on one URI.",
                      "one URI"),
    "structured tool output": ("Tools can return structuredContent alongside the text "
                               "content.", "structuredContent"),
    "the soak test": ("The soak test runs the server for six hours under steady load.",
                      "six hours"),
}
STOPWORDS = {"the", "of", "in", "at"}
DIM = 1024


def chunk_path(topic: str) -> str:
    words = [w.lower() for w in topic.replace("-", " ").split() if w.lower() not in STOPWORDS]
    return "docs/" + "-".join(words) + ".md"


def search_result(rng: random.Random, topic: str, pool_topics: list[str]) -> str:
    """The topic's chunk first, then two same-domain chunks that rank lower."""
    others = rng.sample([t for t in pool_topics if t != topic], 2)
    cos = [rng.uniform(0.68, 0.82), rng.uniform(0.48, 0.60), rng.uniform(0.42, 0.50)]
    items = []
    for rank, (t, c) in enumerate(zip([topic, *others], cos, strict=True)):
        bm25, fusion = rng.uniform(3.0, 9.0) / (rank + 1), 2 / (61 + rank)
        items.append(f"[cos {c:.3f}  bm25 {bm25:.2f}  fusion {fusion:.3f}] "
                     f"{chunk_path(t)}\n{CORPUS[t][0]}")
    return "\n\n".join(items)


def stats_result(chunks: int, files: int) -> str:
    return f"db:     data/docs.db\nchunks: {chunks}\nfiles:  {files}\ndim:    {DIM}"


def error(message: str) -> str:
    return f"error: {message}"


NO_SUCH_FILE = error("no such file or directory")


@dataclass
class Tree:
    """The sandbox an episode runs in: files with their text and mtime."""
    rng: random.Random
    files: dict[str, dict] = field(default_factory=dict)

    def add(self, path: str, content: str) -> None:
        m, d = self.rng.randint(1, 10), self.rng.randint(1, 28)
        h, mi, sec = self.rng.randint(0, 23), self.rng.randint(0, 59), self.rng.randint(0, 59)
        self.files[path] = {"content": content,
                            "modified": f"2026-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{sec:02d}Z"}

    def size(self, path: str) -> int:
        return len(self.files[path]["content"].encode())

    def entries(self, d: str) -> list[str]:
        return sorted(p.removeprefix(d + "/") for p in self.files
                      if p.startswith(d + "/") and "/" not in p.removeprefix(d + "/"))

    def listing(self, d: str) -> str:
        return "\n".join(f"{'file':<5}{self.size(f'{d}/{n}'):>12}  {n}" for n in self.entries(d))

    def read(self, path: str) -> str:
        return self.files[path]["content"]

    def stat(self, path: str) -> str:
        if path not in self.files:
            return NO_SUCH_FILE
        return (f"path:     {path}\ntype:     file\nsize:     {self.size(path)}\n"
                f"modified: {self.files[path]['modified']}\nmode:     0644")

    @staticmethod
    def write(path: str, content: str) -> str:
        """The server's reply. `files` stays the episode's starting tree:
        writes come last in every episode and nothing reads them back."""
        return f"wrote {len(content.encode())} bytes to {path}"
