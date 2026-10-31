# bridgerag2026 — Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm
Authors / Year / Venue / DOI: Li, Zihang, Liu, Wenjun, Zong, Yikun, Tao, Jiawen, Dai, Siying, Ren, Songcheng, Liu, Zirui, Wang, Yuhang, Jiang, Yanbing, Yang, Tong / 2026 / not stated / none
Status: PRE
PDF: papers/bridgerag2026.pdf   Read fully: yes

## Problem addressed (p.)
Two challenges in RAG systems: retrieval accuracy degradation from flat chunk similarity search returning fragmented or noisy evidence, and computational inefficiency in structured Tree-RAG where traversing deep hierarchical trees to locate entity mentions dominates the response time budget (p. 1, §1).

## Method (core idea in <=5 sentences) (p.)
Bridge-RAG constructs an offline hierarchical abstract bridge tree by grouping fixed windows of $n=5$ consecutive document chunks into intermediate summary abstracts arranged in parent-child levels (p. 1-3, §3.1). It integrates the Cuckoo Filter component from CFT-RAG to perform $O(1)$ constant-time lookup mapping extracted query entities directly to abstract-node addresses (p. 1, 3-4, §3.2). Retrieved target abstracts are expanded through hierarchical tree traversal to collect ancestor and descendant abstracts up to depth $d \le 3$ (p. 3-4, §3.1, §3.3). The system then computes cosine similarity between query embeddings and only the candidate document chunks associated with the expanded abstracts, returning the top-$k$ chunks to assemble prompts for LLM generation (p. 4, §3.3, Algorithm 1).

## Relevance to our project
Novelty check: no; the Cuckoo Filter is queried once before traversal as an external dictionary to resolve entities to abstract tree addresses, and cosine similarity ranking is performed after hierarchical abstract tree expansion over candidate chunks (p. 3-4, §3.2-§3.3, Algorithm 1).

## Flags
- Similar to CFT-RAG, the "Cuckoo Filter" is utilized as an associative address-mapping index (storing pointers in bucket slots) rather than purely as a probabilistic set-membership filter (p. 4, §3.2, Fig. 2).
- The references list in the preprint cites CFT-RAG as "Li et al., 2026" published in ICLR 2026 (p. 9, [921]), whereas CFT-RAG exists in our seed manifest as an arXiv preprint (`cftrag2025` / arXiv:2501.15098).
