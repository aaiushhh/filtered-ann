#include <iostream>
#include <cstdint>
#include <cstring>
#include <cassert>

struct Bucket12 {
    uint8_t raw[6];
    Bucket12() {
        std::memset(raw, 0, 6);
    }
    uint16_t get_slot(size_t s) const {
        if (s == 0) return raw[0] | ((raw[1] & 0x0F) << 8);
        if (s == 1) return (raw[1] >> 4) | (raw[2] << 4);
        if (s == 2) return raw[3] | ((raw[4] & 0x0F) << 8);
        return (raw[4] >> 4) | (raw[5] << 4);
    }
    void set_slot(size_t s, uint16_t fp) {
        fp &= 0x0FFF;
        if (s == 0) {
            raw[0] = fp & 0xFF;
            raw[1] = (raw[1] & 0xF0) | ((fp >> 8) & 0x0F);
        } else if (s == 1) {
            raw[1] = (raw[1] & 0x0F) | ((fp & 0x0F) << 4);
            raw[2] = (fp >> 4) & 0xFF;
        } else if (s == 2) {
            raw[3] = fp & 0xFF;
            raw[4] = (raw[4] & 0xF0) | ((fp >> 8) & 0x0F);
        } else {
            raw[4] = (raw[4] & 0x0F) | ((fp & 0x0F) << 4);
            raw[5] = (fp >> 4) & 0xFF;
        }
    }
};

int main() {
    Bucket12 b;
    b.set_slot(0, 0x123);
    b.set_slot(1, 0x456);
    b.set_slot(2, 0x789);
    b.set_slot(3, 0xABC);

    assert(b.get_slot(0) == 0x123);
    assert(b.get_slot(1) == 0x456);
    assert(b.get_slot(2) == 0x789);
    assert(b.get_slot(3) == 0xABC);

    // Overwrite slot 1
    b.set_slot(1, 0xDEF);
    assert(b.get_slot(0) == 0x123);
    assert(b.get_slot(1) == 0xDEF);
    assert(b.get_slot(2) == 0x789);
    assert(b.get_slot(3) == 0xABC);

    std::cout << "Bucket12 test PASSED! sizeof(Bucket12) = " << sizeof(Bucket12) << " bytes\n";
    return 0;
}
