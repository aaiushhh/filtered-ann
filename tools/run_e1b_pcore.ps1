$proc = Start-Process -FilePath "wsl.exe" -ArgumentList "-d", "Ubuntu", "-u", "root", "--", "nice", "-n", "-20", "/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/harness/run_e1b_benchmarks", "0" -PassThru
$proc.ProcessorAffinity = [IntPtr]0x0FFF
Write-Host "Started run_e1b_benchmarks with host-side P-core affinity: $($proc.ProcessorAffinity.ToInt64())"
Wait-Process -Id $proc.Id
Write-Host "run_e1b_benchmarks finished."
