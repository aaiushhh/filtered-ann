# Grid structure in run_e1_benchmarks.cpp:
# N in [1e6, 1e7, 1e8, 1e9] (4)
# sigma in [0.001, 0.01, 0.1, 0.5] (4)
# 18 structures:
# 0: attribute_array uint32
# 1: bitmap 1-bit
# 2: hash_set open_addressing
# 3..7: bloom_standard b6, b8, b10, b12, b16
# 8..12: bloom_blocked b6, b8, b10, b12, b16
# 13..15: cuckoo 8bit, 12bit, 16bit
# 16..17: xor 8bit, 16bit

structures = [
    ("attribute_array", "uint32"),
    ("bitmap", "1-bit"),
    ("hash_set", "open_addressing"),
    ("bloom_standard", "b6"),
    ("bloom_standard", "b8"),
    ("bloom_standard", "b10"),
    ("bloom_standard", "b12"),
    ("bloom_standard", "b16"),
    ("bloom_blocked", "b6"),
    ("bloom_blocked", "b8"),
    ("bloom_blocked", "b10"),
    ("bloom_blocked", "b12"),
    ("bloom_blocked", "b16"),
    ("cuckoo", "8bit"),
    ("cuckoo", "12bit"),
    ("cuckoo", "16bit"),
    ("xor", "8bit"),
    ("xor", "16bit")
]

Ns = [1000000, 10000000, 100000000, 1000000000]
sigmas = [0.001, 0.01, 0.1, 0.5]

cell_id = 0
for n in Ns:
    for sig in sigmas:
        for s, v in structures:
            cell_id += 1
            if 240 <= cell_id <= 255:
                print(f"Cell {cell_id}: N={n}, sigma={sig}, struct={s}, variant={v}")
