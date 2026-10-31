#!/bin/bash
for c in 0 2 4 6 8 10; do
    echo "=== CPU $c ==="
    /tmp/timer_noise_cpp $c 500000000
done
