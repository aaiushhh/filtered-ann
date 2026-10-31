#include <iostream>
#include <vector>
#include <cassert>
#include "experiments/harness/filters.hpp"
#include "experiments/harness/cuckoo_filter.hpp"
#include "experiments/harness/xorfilter_singleheader.h"

using namespace filtered_ann;

int main() {
    // 1. Bitmap
    BitmapFilter bm(1000000);
    bm.set(42);
    assert(bm.contains(42));
    assert(!bm.contains(43));
    std::cout << "Bitmap bytes for 1M: " << bm.size_in_bytes() << "\n";

    // 2. OpenAddressingHashSet
    OpenAddressingHashSet hs(1000);
    hs.insert(12345);
    assert(hs.contains(12345));
    assert(!hs.contains(12346));
    std::cout << "OpenAddressingHashSet bytes for 1000 items: " << hs.size_in_bytes() << "\n";

    // 3. Bloom standard
    BloomFilter bf(1000, 8.0);
    bf.insert(999);
    assert(bf.contains(999));
    std::cout << "Standard Bloom (8bpe, 1000 items) bytes: " << bf.size_in_bytes() << "\n";

    // 4. Blocked Bloom
    BlockedBloomFilter bbf(1000, 8.0);
    bbf.insert(888);
    assert(bbf.contains(888));
    std::cout << "Blocked Bloom (8bpe, 1000 items) bytes: " << bbf.size_in_bytes() << "\n";

    // 5. Cuckoo 8, 12, 16
    CuckooFilter8 cf8(1000);
    cf8.insert(777);
    assert(cf8.contains(777));
    std::cout << "Cuckoo8 bytes: " << cf8.size_in_bytes() << "\n";

    CuckooFilter12 cf12(1000);
    cf12.insert(777);
    assert(cf12.contains(777));
    std::cout << "Cuckoo12 bytes: " << cf12.size_in_bytes() << "\n";

    CuckooFilter16 cf16(1000);
    cf16.insert(777);
    assert(cf16.contains(777));
    std::cout << "Cuckoo16 bytes: " << cf16.size_in_bytes() << "\n";

    // 6. Xor 8, 16
    xor8_t xf8;
    std::vector<uint64_t> keys = {1, 2, 3, 4, 5, 100, 200};
    xor8_allocate(keys.size(), &xf8);
    xor8_populate(keys.data(), keys.size(), &xf8);
    assert(xor8_contain(100, &xf8));
    std::cout << "Xor8 bytes: " << xor8_size_in_bytes(&xf8) << "\n";
    xor8_free(&xf8);

    std::cout << "ALL STRUCTURE TESTS PASSED!\n";
    return 0;
}
