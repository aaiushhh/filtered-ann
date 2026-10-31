# Coverage Gaps and Candidate Systems Analysis (Phase 2)

This document tracks all candidate papers checked for Group D (filtered/predicate-constrained ANN search in graph indexes), including accepted additions and rejected/unverifiable candidates with explicit reasons.

## Accepted Additions (Group D, Gate 0.5, Status: ADDED-PENDING-USER-REVIEW)

1. **gollapudi2023filtereddiskann**
   - Title: Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters
   - Authors: Siddharth Gollapudi, Neel Karia, Varun Sivashankar, Ravishankar Krishnaswamy, Nikit Begwani, Swapnil Raz, Yiyong Lin, Yin Zhang, Neelam Mahapatro, Premkumar Srinivasan, Amit Singh, Harsha Vardhan Simhadri
   - Venue: Proceedings of the ACM Web Conference 2023 (WWW 2023)
   - Year: 2023
   - DOI: 10.1145/3543507.3583552
   - Verification Method: Crossref API confirmed
   - Relevance: Canonical graph-based filtered ANN system introducing Filtered-Vamana and Stitched-Vamana. Crucial baseline for filtered graph traversal.

2. **patel2024acorn**
   - Title: ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data
   - Authors: Liana Patel, Peter Kraft, Carlos Guestrin, Matei Zaharia
   - Venue: Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)
   - Year: 2024
   - DOI: 10.1145/3654923
   - Verification Method: Crossref API confirmed
   - Relevance: Introduces predicate-agnostic filtered graph traversal by replacing post-filtering / disconnected graphs with multi-hop extension in HNSW.

3. **luo2025tagfiltered**
   - Title: Tag-Filtered Approximate Nearest Neighbor Search
   - Authors: Jiarui Luo, Miao Qiao, Chaoji Zuo, Dong Deng
   - Venue: 2025 IEEE 41st International Conference on Data Engineering (ICDE 2025)
   - Year: 2025
   - DOI: 10.1109/icde65448.2025.00272
   - Verification Method: Crossref API confirmed
   - Relevance: Directly investigates graph-based tag-filtered similarity search; addresses low-selectivity filter challenges.

4. **wu2022hqann**
   - Title: HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints
   - Authors: Wei Wu, Junlin He, Yu Qiao, Guoheng Fu, Li Liu, Jin Yu
   - Venue: Proceedings of the 31st ACM International Conference on Information & Knowledge Management (CIKM 2022)
   - Year: 2022
   - DOI: 10.1145/3511808.3557610
   - Verification Method: Crossref API confirmed
   - Relevance: Early and influential hybrid query ANN system combining structured filters with graph-based vector search.

5. **cai2024navigating**
   - Title: Navigating Labels and Vectors: A Unified Approach to Filtered Approximate Nearest Neighbor Search
   - Authors: Yuzheng Cai, Jiayang Shi, Yizhuo Chen, Weiguo Zheng
   - Venue: Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)
   - Year: 2024
   - DOI: 10.1145/3698822
   - Verification Method: Crossref API confirmed
   - Relevance: Unifies label/metadata navigation with proximity graph traversal (NHQ lineage); directly pertinent to graph traversal with filters.

6. **zuo2024serf**
   - Title: SeRF: Segment Graph for Range-Filtering Approximate Nearest Neighbor Search
   - Authors: Chaoji Zuo, Miao Qiao, Wenchao Zhou, Feifei Li, Dong Deng
   - Venue: Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)
   - Year: 2024
   - DOI: 10.1145/3639324
   - Verification Method: Crossref API confirmed
   - Relevance: Segment graph index specifically designed for range-filtering during graph ANN search.

7. **zhang2025dynamic**
   - Title: Efficient Dynamic Indexing for Range Filtered Approximate Nearest Neighbor Search
   - Authors: Fangyuan Zhang, Mengxu Jiang, Guanhao Hou, Jieming Shi, Hua Fan, Wenchao Zhou, Feifei Li, Sibo Wang
   - Venue: Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2025)
   - Year: 2025
   - DOI: 10.1145/3725401
   - Verification Method: Crossref API confirmed
   - Relevance: Dynamic indexing for range-filtered vector search over graphs; handles dynamic updates with filters.

8. **zou2026rnsg**
   - Title: RNSG: A Range-Aware Graph Index for Efficient Range-Filtered Approximate Nearest Neighbor Search
   - Authors: Zhiqiu Zou, Ziqi Yin, Rong-Hua Li, Hongchao Qin, Qiangqiang Dai, Guoren Wang
   - Venue: Proceedings of the VLDB Endowment (PVLDB 2026)
   - Year: 2026
   - DOI: 10.14778/3828612.3828636
   - Verification Method: Crossref API confirmed
   - Relevance: Range-aware navigable small-world graph index optimizing search under range filters.

9. **wang2021milvus**
   - Title: Milvus: A Purpose-Built Vector Data Management System
   - Authors: Jianguo Wang, Xiaomeng Yi, Rentong Guo, Hai Jin, Peng Xu, Shengjun Li, Xiangyu Wang, Xiangzhou Guo, Chengming Li, Xiaohai Xu, Kun Yu, Yuxing Yuan, Yinghao Zou, Jiquan Long, Yudong Cai, Zhenxiang Li, Zhifeng Zhang, Yihua Mo, Jun Gu, Ruiyi Jiang, Yi Wei, Charles Xie
   - Venue: Proceedings of the 2021 International Conference on Management of Data (SIGMOD 2021)
   - Year: 2021
   - DOI: 10.1145/3448016.3457550
   - Verification Method: Crossref API confirmed
   - Relevance: Landmark vector database architecture detailing practical integration of scalar filtering with vector index execution engines.

10. **shaikh2026annex**
    - Title: ANNex: Efficient Filtered Approximate Nearest Neighbor Search via Graph-Traversal Metadata Filtering
    - Authors: Danish Nasir Shaikh
    - Venue: IgMin Research
    - Year: 2026
    - DOI: 10.61927/igmin365
    - Verification Method: Crossref API confirmed
    - Relevance: Explicitly addresses in-traversal metadata filtering on proximity graphs.

---

## Rejected or Unverifiable Candidates

1. **CAPS: A Partition-based Index for Filtered Similarity Search**
   - Reason: Could not verify an exact published conference/journal DOI or stable arXiv eprint ID matching this specific title and author list via Crossref/arXiv APIs at this time. Note: Cited in `routing2026query` as arXiv:2308.15014.
2. **VBase: Unifying High-Dimensional Vector Similarity Search and Relational Queries (OSDI/SOSP)**
   - Reason: While VBase is known in systems literature, an official DOI via Crossref could not be resolved reliably during automated API querying; excluded to avoid any unverified metadata.
3. **MultiFilterANN**
   - Reason: No distinct publication record with registered DOI found via automated Crossref API search.
4. **DIGRA (PACMMOD 2025)**
   - Reason: Querying by acronym / title variant resolved to Zhang et al. (DOI 10.1145/3725401) and Luo et al. (DOI 10.1109/icde65448.2025.00272). Handled via Zhang et al. entry.

---

## Discovered Gaps in Gate 1 Batch 1 (Cited in Notes, Missing from Manifest)

The following works were cited by the 5 papers read in Batch 1 (`curator2026`, `filteraware2025`, `filtered2026system`, `rangefilters2026`, `routing2026query`) and are candidates for Phase 4 snowballing:

1. **shi2025benchmark**
   - Citation: Jiayang Shi, Yuzheng Cai, Weiguo Zheng. "Filtered Approximate Nearest Neighbor Search on High-Dimensional Data: A Benchmark." arXiv:2509.07789 (2025).
   - Cited by: `routing2026query`
   - Relevance: Comprehensive experimental benchmark covering Pre-filter, Post-filter, UNG, ACORN, Vamana across multiple datasets and predicates.

2. **li2025sieve**
   - Citation: Zhaoheng Li, Silu Huang, Wei Ding, Yongjoo Park, Jianjun Chen. "SIEVE: A Workload-Adaptive Sub-Index Framework for Filtered Vector Search." (2025).
   - Cited by: `routing2026query`
   - Relevance: Workload-adaptive sub-index selection for filtered ANN queries; major baseline in router benchmark.

3. **gan2026efficient**
   - Citation: Zhuocheng Gan, Yifan Wang. "Efficient Filtered-ANN via Learning-based Execution Planning." (2026).
   - Cited by: `routing2026query`
   - Relevance: Learning-based execution planner deciding between Pre-filtering and Post-filtering per query; directly relevant to crossover selectivity $\sigma^*$ analysis.

4. **zuo2023arkgraph**
   - Citation: Chaoji Zuo, Dong Deng. "ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph." PVLDB 16(11): 3034-3047 (2023).
   - Cited by: `routing2026query`, `curator2026`
   - Relevance: Foundational range-filtered proximity graph construction.

