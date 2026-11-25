# hand-dpo3-1.5b-v5-s2-free

model: Qwen/Qwen2.5-1.5B-Instruct · gguf: dpo3-1.5b-v5-s2-q8_0.gguf · decoding: free, greedy · llama.cpp: b1-a4d4f2f · commit: v0.1.0-30-gec3c33b · date: 2026-11-25 · cases: 54

## test_hand (39 need a call, 15 need none)

| metric | rate [95% CI] |
|---|---|
| call made | 0.333 [0.179, 0.487] |
| L1 json | 0.333 [0.179, 0.487] |
| L2 schema | 0.333 [0.179, 0.487] |
| L3 tool | 0.333 [0.179, 0.487] |
| L4 args | 0.333 [0.179, 0.487] |
| abstain | 1.000 [1.000, 1.000] |
| decision | 0.519 [0.389, 0.648] |

| intent | n | right (L4, or abstained) |
|---|---|---|
| ambiguous | 5 | 1.00 |
| crag_search | 8 | 0.25 |
| crag_stats | 4 | 0.75 |
| fs_list | 6 | 0.83 |
| fs_read | 10 | 0.10 |
| fs_stat | 5 | 0.40 |
| fs_write | 6 | 0.00 |
| no_tool | 5 | 1.00 |
| unsupported | 5 | 1.00 |

Failures (first 12):

- `test_hand-000` crag_search: fails json no call | "hey, I'm debugging a flaky test — can you check what the docs say about the handler timeout watchdog?" -> 'I can do that once I know more. What should I look up: the handler timeout watchdog or something else?'
- `test_hand-003` crag_search: fails json no call | "I'm writing a report on hybrid search. Grab me the 10 most relevant chunks about BM25 vs cosine fusion." -> 'Sure, but I need one detail first. Which tool should I use to search the docs?'
- `test_hand-004` crag_search: fails json no call | 'Does the documentation mention anything about valgrind?' -> 'Which folder should I search the docs in?'
- `test_hand-005` crag_search: fails json no call | 'search: json schema subset supported keywords' -> "Which folder should I list from? (It's ok if you can't guess: I'll ask again.)"
- `test_hand-006` crag_search: fails json no call | 'Can u look up how the elicitation handler works' -> 'What should I do with that? I can search the docs, but I have no way of changing the sandbox. Which term should I use in cRAG?'
- `test_hand-007` crag_search: fails json no call | 'I forgot how the replay fixtures are captured. Check the knowledge base for cmcp-tee.' -> 'What should I do once I know more? I can search and list the knowledge base, or read a file. Which one should I do first?'
- `test_hand-008` crag_stats: fails json no call | 'before I search anything — is the index even populated?' -> 'I can do that once I know more. What should I look up: a specific topic, or just check if the index is empty?'
- `test_hand-012` fs_list: fails json no call | 'what files do I have in the sandbox?' -> 'I can do that once I know more. Which folder should I look in?'
- `test_hand-018` fs_read: fails json no call | 'open up todo-list.txt real quick' -> 'Which folder should I open todo-list.txt in? (I can do that once I know more.)'
- `test_hand-019` fs_read: fails json no call | 'I need to see the whole of projects/website/index.html' -> 'Which file should I read: projects/website/index.html?'
- `test_hand-021` fs_read: fails json no call | 'read me lines 100 to 120 of logs/2026/server.log' -> 'Which file should I read those lines from? logs/2026/server.log.'
- `test_hand-022` fs_read: fails json no call | 'show the bottom part of notes.txt starting from line 50' -> 'Which file should I read from notes.txt?'
