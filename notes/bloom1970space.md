# bloom1970space — Space/Time Trade-offs in Hash Coding with Allowable Errors
Authors / Year / Venue / DOI: Burton H. Bloom / 1970 / Communications of the ACM / 10.1145/362686.362692
Status: PUB
PDF: papers/bloom1970space.pdf   Read fully: yes

## Problem addressed (p.)
Testing messages one-by-one for membership in a given set when the vast majority of test queries are non-members, without requiring large core memory storage for an exact error-free hash table (p. 422). It formally analyzes trade-offs among hash area size (space), average time required to identify non-members (reject time), and allowable false-positive error frequency (p. 422).

## Method (core idea in ≤5 sentences) (p.)
The paper proposes two approximate hash-coding methods that trade a small allowable fraction of false-positive errors for substantial reductions in hash area size (p. 422–423). Method 1 organizes memory into cells storing compact c-bit hash codes instead of full messages, resolving collisions by sequential probing until an empty cell or matching code is found (p. 423). Method 2 (the classical Bloom filter) treats the hash area as an unpartitioned bit array of $N$ bits initialized to zero (p. 423). Each stored message is mapped by $d$ distinct hash functions to $d$ bit addresses, setting all $d$ bits to 1 (p. 423). Membership testing evaluates the $d$ bit addresses; the query is rejected immediately if any bit is 0, and accepted (with false-positive probability $P$) if all $d$ bits are 1 (p. 423).

## Complexity / theoretical claims
- Method 1: Normalized reject time $T' = (3/\phi') - 2$ (eq. 11, p. 425), hash area size $N' = n \cdot c \cdot (T' + 2) / (T' - 1)$ (eq. 12, p. 425), error rate $P' = (1/2)^{c-1} / \phi'$ (eq. 13, p. 425).
- Method 2: Fraction of remaining 0 bits $\phi'' = (1 - d/N'')^n \approx e^{-n d / N''}$ (eq. 16, p. 425).
- False-positive probability $P'' = (1 - \phi'')^d$ (eq. 17, p. 425).
- Normalized reject time $T'' = \sum_{x=1}^\infty x \cdot \phi'' (1 - \phi'')^{x-1} = 1/\phi''$ (eq. 20, p. 425).
- Space/time trade-off relation: $N'' = n \cdot (-\log_2 P'') \cdot \frac{\log_2 e}{\log_2(1/T'') \cdot \log_2(1 - 1/T'')}$ (eq. 21, p. 425).
- Minimum normalized space occurs at $T'' = 2$ ($\phi'' = 1/2$, half 1s and half 0s), yielding $S'' = \log_2 e \approx 1.4427$ bits per element per factor of $-\log_2 P$ (p. 425).
- Statement, assumptions, theorem number, page: none stated as formal numbered theorems; derived via closed-form probability equations assuming independent uniform hashing and single-bit address testing units (eq. 1–25, p. 423–425).

## Filter type and selectivity regime handled (p.)
- Filter type: Standard Bloom filter (Method 2: unpartitioned bit vector with $d$ hash functions) and hashed-cell filter (Method 1: compact hash codes in open-addressing cells) (p. 423).
- Selectivity regime handled: Designed for membership testing where "the great majority of messages to be tested will not belong to the given set" (p. 422), corresponding to low query selectivity / sparse target sets (e.g., 10% minority dictionary set among 500,000 words, p. 425–426).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (flat bit array or open-addressed hash table; no vector index, tree, or graph index) (p. 422–423).

## Datasets, baselines, metrics (Table N)
- Datasets: Synthetic hyphenation dictionary scenario with 50,000 exception words out of 500,000 total candidate English words, where 450,000 follow simple hyphenation rules (p. 425–426).
- Baselines: Conventional error-free open-addressing hash table storing $(b+1)$-bit message entries ($b \ge 19$ bits) (p. 423–424, 426); Method 1 vs Method 2 comparison (p. 425).
- Metrics: Normalized reject time $T$, normalized space measure $S = N / (-n \log_2 P)$ (eq. 22, p. 425), hash area size $N$ (bits), allowable error fraction $P$, disk accesses saved (%) (un-numbered table, p. 426).

## Key results (numbers exactly as reported, with Table/Fig locator)
- In the hyphenation example ($n = 50{,}000$, $b=19$), conventional hash table requires 2,000,000 bits for $T=4$ (p. 426).
- Method 2 with $P = 1/16$ and $T=2$ reduces required space to less than 300,000 bits ($N = 291{,}200$ bits), achieving an 84.4% reduction in disk accesses (un-numbered table, p. 426).
- Un-numbered table values:
  - $P = 1/2 \implies N = 72{,}800$ bits, 45.0% disk accesses saved (un-numbered table, p. 426).
  - $P = 1/4 \implies N = 145{,}600$ bits, 67.5% disk accesses saved (un-numbered table, p. 426).
  - $P = 1/8 \implies N = 218{,}400$ bits, 78.7% disk accesses saved (un-numbered table, p. 426).
  - $P = 1/16 \implies N = 291{,}200$ bits, 84.4% disk accesses saved (un-numbered table, p. 426).
  - $P = 1/32 \implies N = 364{,}000$ bits, 87.2% disk accesses saved (un-numbered table, p. 426).
  - $P = 1/64 \implies N = 509{,}800$ bits, 88.5% disk accesses saved (un-numbered table, p. 426).
- Optimal operating point of Method 2 attains minimum normalized space $S'' = \log_2 e \approx 1.47$ at $T'' = 2$ when $\phi'' = 0.5$ (p. 425, Fig. 1).

## Limitations (author-stated vs. observed)
- Author-stated: Method 2 inherently permits false-positive errors and cannot achieve error-free operation (p. 423); analysis assumes uniform single-bit address calculation and access time, which may not hold on word- or byte-oriented architectures (p. 424, footnote 1); does not support deletions (not stated / inherent to standard Bloom filter).
- Observed: Purely 1D set-membership model with no notion of metric spaces, high-dimensional vectors, similarity distances, or graph traversal.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides the seminal theoretical formulation of probabilistic approximate membership filters and false-positive cost trade-offs. Directly informs our analytical cost model balancing filter check latency against downstream exact distance evaluations during search. Serves as the classic baseline filter structure to compare against Cuckoo and Xor filters.
Novelty check: Novelty check: no (deals strictly with standalone set membership for dictionary hyphenation, with no graph traversal or vector search; §A Sample Application, p. 422–423).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Page 425 states that $S'' = \log_2 e = 1.47$ for $T'' = 2$, whereas $\log_2 e \approx 1.442695$.
- The un-numbered table on page 426 lists $N = 509{,}800$ for $P = 1/64$; however, for $P = 1/2, 1/4, 1/8, 1/16, 1/32$, $N$ increases by exactly $72{,}800$ per step ($72{,}800 \times 5 = 364{,}000$), so $P = 1/64$ would be expected to be $436{,}800$, while $509{,}800 \approx 7 \times 72{,}800$.

## Useful references to snowball (bibkeys or titles from its reference list)
- Batson, A. (1965). The organization of symbol tables. Comm. ACM 8(2), 111–112.
- Maurer, W. D. (1968). An improved hash code for scatter storage. Comm. ACM 11(1), 35–38.
- Morris, R. (1968). Scatter storage techniques. Comm. ACM 11(1), 38–44.
