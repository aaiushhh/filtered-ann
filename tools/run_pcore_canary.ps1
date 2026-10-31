$proc = Start-Process -FilePath "wsl.exe" -ArgumentList "-d", "Ubuntu", "--", "/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/harness/run_canary_loop", "600", "/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1b/canary_pcore_affinity.csv", "0" -PassThru
$proc.ProcessorAffinity = [IntPtr]0x0FFF
Write-Host "Started WSL with host-side P-core affinity: $($proc.ProcessorAffinity.ToInt64())"
Wait-Process -Id $proc.Id
Write-Host "Setting 2 finished."
