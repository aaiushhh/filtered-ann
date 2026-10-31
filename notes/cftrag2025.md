# cftrag2025 — CFT-RAG: An Entity Tree Based Retrieval Augmented Generation Algorithm With Cuckoo Filter
Authors / Year / Venue / DOI: Li, Zihang, Ruan, Yangdong, Liu, Wenjun, Wang, Zhengyang, Yang, Tong / 2025 / not stated / none
Status: PRE
PDF: papers/cftrag2025.pdf   Read fully: yes

## Problem addressed (p.)
Computational inefficiency and high retrieval latency in Tree-RAG during entity localization over large-scale hierarchical knowledge trees, where naive breadth-first search (BFS) traversing deep forests to locate entity mentions is slow (p. 1-2, §1).

## Method (core idea in <=5 sentences) (p.)
CFT-RAG introduces an in-memory Cuckoo Filter augmented with Cuckoo Hashing to store entity fingerprints and direct pointers to block linked lists of entity tree locations, achieving $O(1)$ lookup time (p. 2, 4-6, §3.1-§3.4). Each bucket entry stores a 12-bit fingerprint, a "temperature" variable recording access frequency, and the head pointer of a block linked list containing the entity's tree addresses (p. 2, 4, §3.1). Entries within each bucket are dynamically sorted by temperature so frequently queried entities are placed first to accelerate linear bucket scans (p. 2, 4, §3.1). Once entity locations are retrieved, multi-level parent and child nodes across forest trees are gathered to construct an augmented contextual prompt for the LLM (p. 4-6, §3.4, Fig. 1, Fig. 4).

## Relevance to our project
Novelty check: no; the Cuckoo Filter is used as a standalone pre-traversal key-value lookup index to locate entities in tree structures prior to prompt generation, rather than pruning edges during vector similarity graph traversal (p. 2, 4-6, §3.1-§3.4). However, as a baseline, Section 4.1 (p. 6) describes "Bloom Filter T-RAG", which places a Bloom filter at each tree node to prune tree search paths during hierarchical tree traversal.

## Flags
- The proposed structure deviates from a standard Approximate Membership Query (AMQ) Cuckoo filter: it attaches memory pointers and temperature counters to each slot, functioning essentially as a Cuckoo Hash table (p. 2, 4, 6, §3.1, §4.2).
- The vector similarity search step depicted in Fig. 1 (p. 3) is treated as a black-box pre-step and is not experimentally evaluated or integrated with the filter.
