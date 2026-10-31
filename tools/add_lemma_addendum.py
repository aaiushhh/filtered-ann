with open("notes/rangefilters2026.md", "r", encoding="utf-8") as f:
    content = f.read()

# Prepare addendum text
addendum_text = """
## Addendum 2: Analysis of Lemma 1 and Lemma 2 (Cost, Space, Recall vs. Alpha)
1. **Lemma 1 Analysis (§3.3, p. 7)**:
   - *Statement & Algorithm*: Bounds the worst-case time complexity of an in-range query execution in DLH (Algorithm 5).
   - *Assumptions*: Distance-aware labeling sets partitioned by threshold parameter $T$; labeling sets with size at most $T$ are stored explicitly as sets ($D^<(v)$), while labeling sets with size exceeding $T$ are compressed into Bloom filters ($B(v)$). Bloom filters use $t$ hash functions. Query node $v_q$ and candidate node $v_o$ are compared across graph range hops $0 \\le i \\le r$. Total elements in explicit sets of $v$ is $d^<_v$; number of heavy sets exceeding $T$ is $c^>_v$. For range $r$, $d^<_{v_q}, d^<_v < rT$ and $c^>_{v_q}, c^>_v \\le r$.
   - *What is bounded*: Time complexity of in-range intersection testing between query node $v_q$ and candidate node $v_o$.
   - *Variables in bound*: Bounded as $O(d^<_{v_q} \\cdot t + d^<_v \\cdot t + c^>_{v_q} \\cdot c^>_v \\cdot t)$, which simplifies under range parameter $r$ to $O(r t T + r^2 t)$.
   - *Dependence on $\\alpha$*: Does not bound cost, space, or recall as a function of false-positive probability $\\alpha$. The variable $\\alpha$ does not appear anywhere in the statement or proof of Lemma 1; time is bounded strictly as a function of set cardinalities, heavy set counts, range $r$, threshold $T$, and hash function count $t$.

2. **Lemma 2 Analysis (§4, p. 8)**:
   - *Statement & Algorithm*: Bounds the average time complexity of an in-range query in DLH-M with memoization (Algorithms 6 and 7).
   - *Assumptions*: $n_c$ total candidates evaluated during traversal; hash evaluations $preh(D(v_q))$ on explicit sets of query node $v_q$ take $O(d^<_{v_q} \\cdot t)$ time and are memoized prior to search; each candidate query requires $O(d^<_{v_q} \\cdot t)$ time; total time for $n_c$ candidates is $O(d^<_{v_q} \\cdot t + n_c \\cdot d^<_{v_q} \\cdot t)$, yielding average time $O(d^<_{v_q} \\cdot t / n_c + d^<_{v_q} \\cdot t)$; candidate count $n_c$ is assumed much larger than fixed hash count $t$ ($n_c \\gg t$), making the first term negligible.
   - *What is bounded*: Average time complexity of an individual in-range query during graph exploration.
   - *Variables in bound*: Bounded as $O(d^<_{v_q} \\cdot t + d^<_v \\cdot t + c^>_{v_q} \\cdot c^>_v \\cdot t)$, simplifying to $O(d^<_{v_q} \\cdot t)$ for the memoized intersection component.
   - *Dependence on $\\alpha$*: Does not bound cost, space, or recall as a function of false-positive probability $\\alpha$. The variable $\\alpha$ does not appear in the statement or proof of Lemma 2.

3. **Synthesis Regarding Cost Model & Selectivity**:
   - Neither Lemma 1 nor Lemma 2 bounds search cost, space consumption, or search recall as a function of Bloom filter false positive rate $\\alpha$ or query selectivity $\\sigma$.
   - $\\alpha$ is defined solely in background §2.4 (p. 4) as the theoretical Bloom filter false positive formula $\\alpha = (1/2)^{(m/r)\\ln 2}$, and investigated empirically in §5.3 (p. 10, Fig. 10) by varying FPP from 0.001 to 0.015.
   - Therefore, the paper contains no formal analytical cost or complexity model as a function of selectivity $\\sigma$ or error rate $\\alpha$. Selectivity cost model remains `no`.
"""

# Insert before '## Useful references to snowball'
target = "## Useful references to snowball"
if target in content:
    idx = content.find(target)
    new_content = content[:idx] + addendum_text.strip() + "\n\n" + content[idx:]
else:
    new_content = content + "\n\n" + addendum_text.strip()

with open("notes/rangefilters2026.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated notes/rangefilters2026.md successfully.")
